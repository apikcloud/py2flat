# pylint: disable=R0902
import copy
import json
import logging
import os
import struct
from dataclasses import dataclass, field

from py2flat.segment import Segment
from py2flat.utils import DEFAULT_SEPARATOR

_logger = logging.getLogger(__name__)


@dataclass(kw_only=True)
class Schema:
    name: str
    collection: str
    version: str
    segments: list[Segment]
    by_identifier: dict = field(default_factory=dict)
    by_name: dict = field(default_factory=dict)
    method: str = "first_3_letters"
    raise_if_unknown_segment: bool = False
    skip_null_value: bool = True
    separator: str = DEFAULT_SEPARATOR

    __exclude__ = ["segments", "by_identifier", "by_name"]

    # def __repr__(self) -> str:
    #     return f"<Schema:{self.collection}> name='{self.name}' version='{self.version}'"

    def __post_init__(self):
        self.segments = [Segment(**vals) for vals in self.segments]
        self.by_identifier = {seg.identifier: seg for seg in self.segments}
        self.by_name = {seg.name: seg for seg in self.segments}

    def struct(self):
        return {seg.name: seg.struct() for seg in self.segments}

    def _compare_identifiers(self, identifiers, required_only=False):
        if required_only:
            seg_identifiers = [seg.identifier for seg in self.segments if seg.required]
            return list(set(seg_identifiers).difference(set(identifiers)))

        seg_identifiers = [seg.identifier for seg in self.segments]
        return list(set(identifiers).difference(set(seg_identifiers)))

    def _unpack_identifier(self, lines):
        # TODO: Maybe there is another method ?
        if self.method != "first_3_letters":
            raise ValueError(f"Unknow method '{self.method}'")

        fformat = "3s"
        unpack = struct.Struct(fformat).unpack_from
        return list(map(lambda s: s[0].decode(), map(unpack, lines)))

    def _parse(self, content: bytes) -> dict:
        data = {}

        # TODO: Find a better way to check and clean endline
        lines = list(filter(bool, content.splitlines()))

        # Before parsing the content, get all identifiers (first 3 letters in this case)
        identifiers = self._unpack_identifier(lines)

        # Compare identifiers
        #   1. required segments
        diff = self._compare_identifiers(identifiers, required_only=True)
        if diff:
            raise ValueError(f"Missing required segments: {diff}")

        #   2. unknow segments
        diff = self._compare_identifiers(identifiers)

        if self.raise_if_unknown_segment and diff:
            raise ValueError(f"Unknow segments: {diff}")

        # Unpack values and parse
        for identifier, line in zip(identifiers, lines):
            if identifier not in self.by_identifier:
                # TODO: add a warning: skip line
                continue

            # Get segment according to its identifier
            seg = self.by_identifier[identifier]

            # Compare line and segment length
            if len(line) < seg.size:
                raise ValueError(
                    f"Line length is incorrect (actual:{len(line)} vs needed:{seg.size})."
                )

            values = seg.unpack(line)
            values = seg.parse(values)

            # TODO: Is additional control really necessary?
            # if not all(seg.check(values)):
            #     raise ValueError("Missing required values.")

            values = seg.asdict(values, skip=self.skip_null_value)

            data.setdefault(seg.name, [] if seg.multiple else {})
            if seg.multiple:
                data[seg.name].append(values)
            else:
                data[seg.name].update(values)

            print(values)

        return data

    def read_file(self, filepath: str) -> dict:
        """Public method te parse content from filepath"""
        if not os.path.isfile(filepath):
            raise FileNotFoundError()

        with open(filepath, "rb") as file:
            content = file.read()

        return self._parse(content)

    def read_str(self, content: str) -> dict:
        """Public method te parse content from string"""
        if isinstance(content, str):
            content = bytes(content, "utf-8")

        return self._parse(content)

    def read_bytes(self, content: bytes) -> dict:
        """Public method te parse content from bytes"""
        if not isinstance(content, bytes):
            raise TypeError("Bytes needed.")

        return self._parse(content)

    # def create_exchange(self) -> "Exchange":
    #     return Exchange(schema=self)

    def create_segment(self, identifier: str, vals: dict) -> "Segment":
        seg = self.by_name[identifier]
        new_seg = copy.deepcopy(seg)
        new_seg.set_values(**vals)
        return new_seg

    def json(self):
        vals = dict(
            filter(lambda item: item[0] not in self.__exclude__, vars(self).items())
        )
        vals["segments"] = [seg.json() for seg in self.segments]

        return json.dumps(vals, indent=4)
