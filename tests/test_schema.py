import json

import pytest

from py2flat.parser import Parser


@pytest.fixture
def schema_1():
    json_schema = {
        "name": "test",
        "collection": "test",
        "version": "1.0",
        "raise_if_unknown_segment": False,
        "skip_null_value": True,
        "segments": [
            {
                "name": "Header",
                "required": False,
                "multiple": False,
                "elements": [
                    {
                        "name": "ID",
                        "string": "Identifier",
                        "size": 3,
                        "justify": "left",
                        "required": True,
                        "default": "ENT",
                        "ttype": "str",
                    },
                    {
                        "name": "Name",
                        "string": "Name",
                        "size": 20,
                        "justify": "left",
                        "required": True,
                        "ttype": "str",
                    },
                ],
            }
        ],
    }
    return json.dumps(json_schema)


def test_read_schema(schema_1):
    schema = Parser.from_str(schema_1)

    assert schema.method == "first-3"
    assert schema.count == 1
    assert list(schema.by_name.keys()) == ["Header"]
