# pylint: disable=R0902
import json
import logging

from py2flat.exchange import Exchange
from py2flat.schemas import Schema

_logger = logging.getLogger(__name__)


class Parser(Schema):
    @classmethod
    def from_str(cls, content: str) -> "Schema":
        """Load JSON Schema from string."""

        return Schema(**content)

    @classmethod
    def from_file(cls, filepath: str) -> "Schema":
        """Load JSON Schema from filepath."""

        with open(filepath) as file:
            content = json.load(file)

        return Schema(**content)

    def create_exchange(self) -> "Exchange":
        return Exchange(schema=self)
