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

        data = json.loads(content)
        return Schema(**data)

    @classmethod
    def from_dict(cls, content: dict) -> "Schema":
        """Load JSON Schema from Python dict."""

        return Schema(**content)

    @classmethod
    def from_file(cls, filepath: str) -> "Schema":
        """Load JSON Schema from filepath."""

        with open(filepath) as file:
            data = json.load(file)

        return Schema(**data)

    def create_exchange(self) -> "Exchange":
        return Exchange(schema=self)
