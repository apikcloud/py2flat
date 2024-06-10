import datetime

import pytest

from py2flat.exchange import Exchange
from py2flat.parser import Parser


@pytest.fixture
def parser_1():
    json_schema = {
        "name": "test",
        "collection": "test",
        "version": "1.0",
        "method": "first-1",
        "raise_if_unknown_segment": False,
        "skip_null_value": True,
        "segments": [
            {
                "name": "Header",
                "required": True,
                "elements": [
                    {
                        "name": "ChampEnTete1",
                        "string": "Marqueur d'en-tête 'E'",
                        "size": 1,
                        "required": True,
                        "default": "E",
                    },
                    {
                        "name": "PRHFCY",
                        "string": "Site réception Connexing",
                        "size": 4,
                    },
                    {
                        "name": "RCPDAT",
                        "string": "Date réception",
                        "size": 8,
                        "converter": "AAAAMMJJ",
                    },
                ],
            },
            {
                "name": "Lines",
                "required": True,
                "multiple": True,
                "elements": [
                    {
                        "name": "ChampArt1",
                        "string": "Marqueur d'en-tête 'L'",
                        "size": 1,
                        "required": True,
                        "default": "L",
                    },
                    {
                        "name": "POHNUM",
                        "string": "N° de commande Achat Connexing",
                        "size": 20,
                        "required": True,
                    },
                    {
                        "name": "POPLIN",
                        "string": "N° Ligne de la commande",
                        "size": 8,
                        "ttype": "int",
                        "required": True,
                        "justify": "right",
                    },
                ],
            },
            {
                "name": "LotNumber",
                "required": False,
                "multiple": True,
                "parent": "Lines",
                "elements": [
                    {
                        "name": "ChampLot1",
                        "string": "Marqueur d'en-tête 'N'",
                        "size": 1,
                        "required": True,
                        "default": "N",
                    },
                    {
                        "name": "YTEXTE",
                        "string": "Texte",
                        "size": 28,
                        "justify": "right",
                    },
                ],
            },
        ],
    }

    return Parser.from_dict(json_schema)


def test_read_schema(parser_1):
    data = """
E999920240610
L0000000000000000000100000001
N               Commentaire 1
N               Commentaire 2
"""

    assert parser_1.read_str(data) == {
        "Header": {
            "ChampEnTete1": "E",
            "PRHFCY": "9999",
            "RCPDAT": datetime.datetime(2024, 6, 10, 0, 0),
        },
        "Lines": [
            {
                "ChampArt1": "L",
                "POHNUM": "00000000000000000001",
                "POPLIN": 1,
                "LotNumber": [
                    {
                        "ChampLot1": "N",
                        "YTEXTE": "Commentaire 1",
                    },
                    {
                        "ChampLot1": "N",
                        "YTEXTE": "Commentaire 2",
                    },
                ],
            },
        ],
    }


def test_write_schema(parser_1):
    data = """E999920240610
L00000000000000000001       1
N               Commentaire 1
N               Commentaire 2"""

    exchange = Exchange(parser_1)

    exchange.set_header(
        PRHFCY="9999",
        RCPDAT=datetime.datetime(2024, 6, 10),
    )
    exchange.add_segment(
        "Lines",
        {
            "POHNUM": "00000000000000000001",
            "POPLIN": 1,
            "LotNumber": [
                {
                    "YTEXTE": "Commentaire 1",
                },
                {
                    "YTEXTE": "Commentaire 2",
                },
            ],
        },
    )

    assert exchange.dump() == data
