# pylint: disable=R0902
import copy
import json
import logging
import os
import struct
from dataclasses import dataclass, field
from typing import Any, Generator, List, Literal

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
    method: Literal["first-1", "first-3"] = "first-3"
    raise_if_unknown_segment: bool = False
    skip_null_value: bool = True
    fill: str = DEFAULT_SEPARATOR  # filling character

    __exclude__ = ["segments", "by_identifier", "by_name"]

    # def __repr__(self) -> str:
    #     return f"<Schema:{self.collection}> name='{self.name}' version='{self.version}'"

    def __post_init__(self):
        self.segments = [Segment(**vals) for vals in self.segments]
        self.by_identifier = {seg.identifier: seg for seg in self.segments}
        self.by_name = {seg.name: seg for seg in self.segments}

    @property
    def relations(self):
        res = {}
        for seg in self.segments:
            if seg.parent:
                res.setdefault(seg.parent, [])
                res[seg.parent].append(seg.name)

        return res

    @property
    def count(self):
        return len(self.segments)

    # def struct(self):
    #     return {seg.name: seg.struct() for seg in self.segments}

    def _compare_identifiers(self, identifiers, required_only=False):
        if required_only:
            seg_identifiers = [seg.identifier for seg in self.segments if seg.required]
            return list(set(seg_identifiers).difference(set(identifiers)))

        seg_identifiers = [seg.identifier for seg in self.segments]
        return list(set(identifiers).difference(set(seg_identifiers)))

    def _unpack_identifier(self, lines):
        if self.method == "first-1":
            fformat = "1s"
        elif self.method == "first-3":
            fformat = "3s"
        else:
            raise NotImplementedError(f"Unknow method '{self.method}'")

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

        prev_seg = None
        last_item = None

        # Unpack values and parse
        for identifier, line in zip(identifiers, lines):
            if identifier not in self.by_identifier:
                # TODO: add a warning: skip line
                continue

            # Get segment according to its identifier
            seg = self.by_identifier[identifier]

            # Compare line and segment length
            if len(line) < seg.size:
                _logger.warning(line)
                raise ValueError(
                    f"[{seg.name}] Line length is incorrect (actual:{len(line)} vs needed:{seg.size})."
                )

            values = seg.unpack(line)
            values = seg.parse(values)

            # TODO: Is additional control really necessary?
            # if not all(seg.check(values)):
            #     raise ValueError("Missing required values.")

            values = seg.asdict(values, skip=self.skip_null_value)

            # Nested lines
            if seg.parent:
                if not prev_seg or not last_item:
                    raise ValueError("Orphan line")

                if isinstance(last_item, list):
                    last_item = last_item[-1]

                last_item.setdefault(seg.name, [] if seg.multiple else {})
                if seg.multiple:
                    last_item[seg.name].append(values)
                else:
                    last_item[seg.name].update(values)
            else:
                data.setdefault(seg.name, [] if seg.multiple else {})
                if seg.multiple:
                    data[seg.name].append(values)
                else:
                    data[seg.name].update(values)

                # Define shortcuts to next iteration
                prev_seg = seg
                last_item = data[seg.name]

        return data

    def __parse(self, content: bytes, silent: bool = False) -> dict:
        if not silent:
            return self._parse(content)

        try:
            return self._parse(content)
        except Exception as error:
            return {"error": str(error)}

    def read_file(self, filepath: str, silent: bool = False) -> dict:
        """Public method to parse content from filepath"""
        if not os.path.isfile(filepath):
            raise FileNotFoundError()

        with open(filepath, "rb") as file:
            content = file.read()

        return self.__parse(content, silent=silent)

    def read_str(self, content: str, silent: bool = False) -> dict:
        """Public method to parse content from string"""
        if isinstance(content, str):
            content = bytes(content, "utf-8")

        return self.__parse(content, silent=silent)

    def read_bytes(self, content: bytes, silent: bool = False) -> dict:
        """Public method to parse content from bytes"""
        if not isinstance(content, bytes):
            raise TypeError("Bytes needed.")

        return self.__parse(content, silent=silent)

    def read_dir(self, path: str, silent: bool = False) -> Generator[Any, Any, Any]:
        if not os.path.exists(path):
            raise FileNotFoundError()

        for root, _, files in os.walk(path, topdown=True):
            filepaths = [os.path.join(root, file) for file in files]

        for filepath in filepaths:
            yield os.path.basename(filepath), self.read_file(filepath, silent=silent)

    def create_segment(self, identifier: str, vals: dict) -> List["Segment"]:
        res = []
        seg = self.by_name[identifier]
        new_seg = copy.deepcopy(seg)

        # Exclude children
        relations = self.relations
        if seg.name in relations:
            children = {k: vals.pop(k) for k in relations[seg.name]}

            for child, values in children.items():
                child_seg = self.by_name[child]
                if child_seg.multiple and isinstance(values, list):
                    for child_vals in values:
                        res += self.create_segment(child, child_vals)
                else:
                    res += self.create_segment(child, values)

        new_seg.set_values(**vals)
        res.insert(0, new_seg)
        return res

    def json(self):
        vals = dict(
            filter(lambda item: item[0] not in self.__exclude__, vars(self).items())
        )
        vals["segments"] = [seg.json() for seg in self.segments]

        return json.dumps(vals, indent=4)
