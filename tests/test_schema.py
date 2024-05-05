import json

from py2flat.schemas import Schema

json_schema = {
    "name": "test",
    "collection": "test",
    "version": "1.0",
    "method": "first_3_letters",
    "raise_if_unknown_segment": False,
    "skip_null_value": True,
    "separator": "space",
    "segments": [
        {
            "name": "Header",
            "required": False,
            "multiple": False,
            "elements": [
                {
                    "name": "ID",
                    "string": "Identifier",
                    "position": 1,
                    "length": 3,
                    "number": 1,
                    "justify": "left",
                    "required": True,
                    "default": "ENT",
                    "ttype": "str",
                },
                {
                    "name": "Name",
                    "string": "Name",
                    "position": 4,
                    "length": 20,
                    "number": 2,
                    "justify": "left",
                    "required": True,
                    "ttype": "str",
                },
            ],
        }
    ],
}


def test_create_schema():
    schema = Schema(
        name="test",
        collection="test",
        version="1.0",
        segments=[
            dict(
                name="Header",
                elements=[
                    dict(
                        name="ID",
                        string="Identifier",
                        position=1,
                        length=3,
                        required=True,
                        default="ENT",
                    ),
                    dict(
                        name="Name",
                        string="Name",
                        position=4,
                        length=20,
                        required=True,
                    ),
                ],
            )
        ],
    )
    assert schema.json() == json.dumps(json_schema, indent=4)
