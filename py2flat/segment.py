# pylint: disable=R0902
import logging
import struct
from dataclasses import dataclass, field

from py2flat.element import Element
from py2flat.exceptions import ElementsNumberIncorrect
from py2flat.utils import DEFAULT_SEPARATOR

_logger = logging.getLogger(__name__)


@dataclass(kw_only=True)
class Segment:
    name: str
    elements: list[Element]
    by_name: dict = field(default_factory=dict)
    required: bool = False
    multiple: bool = False
    parent: str = None

    __exclude__ = ["elements", "by_name"]

    def __post_init__(self) -> None:
        self.elements = [
            Element(start=index, **vals) for index, vals in enumerate(self.elements)
        ]
        self.by_name = {element.name: element for element in self.elements}

    @property
    def identifier(self) -> str:
        return self.elements[0].default

    @property
    def total(self) -> int:
        return len(self.elements)

    @property
    def size(self) -> int:
        return sum([element.size for element in self.elements])

    @property
    def fieldwidths(self) -> str:
        # lengths = [element.size for element in self.elements]
        # fieldwidths = " ".join(
        #     "{}{}".format(abs(fw), "x" if fw < 0 else "s") for fw in lengths
        # )
        return " ".join([f"{element.size}s" for element in self.elements])

    def unpack(self, buffer: bytes) -> list[str]:
        """Split"""
        return [
            item.decode()
            for item in struct.Struct(self.fieldwidths).unpack_from(buffer)
        ]

    def parse(self, values: list) -> list | ElementsNumberIncorrect:
        if len(values) != len(self.elements):
            raise ElementsNumberIncorrect()

        return [element.parse(value) for element, value in zip(self.elements, values)]

    def check(self, values: list) -> bool:
        return [
            element.name
            for element, value in zip(self.elements, values)
            if element.required and not value
        ]

    def asdict(self, values: list[dict], skip: bool = False) -> dict:
        if skip:
            return {
                element.name: value
                for element, value in zip(self.elements, values)
                if value
            }
        return {element.name: value for element, value in zip(self.elements, values)}

    def set_values(self, **vals: dict) -> None:
        for key, value in vals.items():
            self.by_name[key].set_value(value)

    def dump(self, fill: str = DEFAULT_SEPARATOR) -> str:
        return "".join([element.dump(fill) for element in self.elements])

    def json(self):
        vals = dict(
            filter(lambda item: item[0] not in self.__exclude__, vars(self).items())
        )
        vals["elements"] = [element.json() for element in self.elements]

        return vals
