# pylint: disable=R0902
import logging
from dataclasses import dataclass
from typing import Any, Literal

from py2flat.converters import Converter
from py2flat.exceptions import ExceededSize, RequiredElementMissing
from py2flat.utils import DEFAULT_SEPARATOR, PYTHON_TYPES, is_equal

_logger = logging.getLogger(__name__)


@dataclass(kw_only=True)
class Element:
    name: str
    string: str
    position: int
    length: int
    number: int = 0
    justify: Literal["left", "right"] = "left"
    required: bool = False
    default: str = None
    ttype: Literal["str", "int", "float"] = "str"
    converter: str = None
    _value: Any = None

    __exclude__ = ["_value"]

    @property
    def start(self) -> int:
        return self.position - 1

    @property
    def end(self) -> int:
        return self.position - 1 + self.length

    def truncate(self, value: str) -> str:
        return value[: self.length]

    def parse(
        self, value: str, truncate: bool = False
    ) -> str | int | float | ExceededSize:
        """Parse raw value according to element configuration and return the result."""

        if not is_equal(value, self.length):
            if not truncate:
                raise ExceededSize(f"{self.name}: '{value}'")
            value = self.truncate(value)

        # 1. Clean
        value = value.strip()
        if not value:
            return self.default

        # 2. Cast to correct Python format
        try:
            value = PYTHON_TYPES[self.ttype](value)
        except ValueError as error:
            if self.required:
                raise RequiredElementMissing(f"{self.name}: {error}")
            return self.default

        # 3. Apply conversion if needed
        if self.converter:
            try:
                value = Converter.by_name(self.converter).input(value)
            except KeyError as error:
                if self.required:
                    raise ValueError(f"Unknow converter: '{self.converter}'") from error
                return self.default
            except Exception as error:
                if self.required:
                    RequiredElementMissing(f"{self.name}: {error}")
                return self.default

        return value

    def set_value(
        self, value: str | int | float, silent: bool = True
    ) -> None | ExceededSize:
        """Store value, nothing else."""

        if not is_equal(value, self.length):
            # Integer or float can't be truncate...
            if isinstance(value, (int, float)):
                raise ExceededSize(f"{self.name}: '{value}'")
            value = self.truncate(value)

        self._value = value

    def dump(self, separator: str = DEFAULT_SEPARATOR) -> str | RequiredElementMissing:
        """Get value ready for export."""

        sep = " " if separator == "space" else separator
        if self._value is None and self.default:
            value = self.default
        else:
            value = self._value

        if value is None:
            if self.required:
                raise RequiredElementMissing(self.name)
            return sep * self.length

        if self.converter:
            value = Converter.by_name(self.converter).output(value)

        value = str(value)

        diff = self.length - len(value)
        if diff <= 0:
            return value

        if self.justify == "right":
            return value.rjust(self.length, sep)
        return value.ljust(self.length, sep)

    def json(self):
        vals = dict(
            filter(
                lambda item: item[0] not in self.__exclude__ and item[1] is not None,
                vars(self).items(),
            )
        )

        return vals
