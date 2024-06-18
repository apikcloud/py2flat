# pylint: disable=R0902
import logging
from dataclasses import dataclass
from typing import Any, Literal

import unidecode

from py2flat.converters import Converter
from py2flat.exceptions import ExceededSize, RequiredElementMissing
from py2flat.utils import DEFAULT_SEPARATOR, PYTHON_TYPES, is_equal

_logger = logging.getLogger(__name__)


@dataclass(kw_only=True)
class Element:
    name: str
    string: str
    start: int
    size: int
    number: int = 0
    justify: Literal["left", "right"] = "left"
    required: bool = False
    default: str = None
    ttype: Literal["str", "int", "float"] = "str"
    converter: str = None
    _value: Any = None

    __exclude__ = ["_value"]

    @property
    def end(self) -> int:
        return self.start + self.size

    def truncate(self, value: str) -> str:
        return value[: self.size]

    def parse(
        self, value: str, truncate: bool = False
    ) -> str | int | float | ExceededSize:
        """Parse raw value according to element configuration and return the result."""

        raw_value = value

        if not is_equal(value, self.size):
            if not truncate:
                raise ExceededSize(f"{self.name}: '{value}'")
            value = self.truncate(value)

        # 1. Clean
        value = value.strip()
        if not value:
            return self.default

        _logger.debug("Step 1: %s", value)

        # 2. Cast to correct Python format
        try:
            value = PYTHON_TYPES[self.ttype](value)
        except ValueError as error:
            if self.required:
                raise RequiredElementMissing(f"{self.name}: {error}")
            return self.default

        _logger.debug("Step 2: %s", value)

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

        _logger.debug("%s -> %s", raw_value, value)
        return value

    def set_value(
        self, value: str | int | float, silent: bool = True
    ) -> None | ExceededSize:
        """Store value, nothing else."""

        if not is_equal(value, self.size):
            # Integer or float can't be truncate...
            if isinstance(value, (int, float)):
                raise ExceededSize(f"{self.name}: '{value}'")
            value = self.truncate(value)

        self._value = value

    def dump(self, fill: str = DEFAULT_SEPARATOR) -> str | RequiredElementMissing:
        """Get value ready for export."""

        sep = " " if fill == "space" else fill
        if self._value is None and self.default:
            value = self.default
        else:
            value = self._value

        if value is None:
            if self.required:
                raise RequiredElementMissing(self.name)
            return sep * self.size

        if self.converter:
            value = Converter.by_name(self.converter).output(value)

        # TODO: add an option to escape accented characters
        if isinstance(value, str):
            value = unidecode.unidecode(value)

        value = str(value)

        diff = self.size - len(value)
        if diff <= 0:
            return value

        if self.justify == "right":
            return value.rjust(self.size, sep)
        return value.ljust(self.size, sep)

    def json(self):
        vals = dict(
            filter(
                lambda item: item[0] not in self.__exclude__ and item[1] is not None,
                vars(self).items(),
            )
        )

        return vals
