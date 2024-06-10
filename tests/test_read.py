import datetime

import pytest

from py2flat.parser import Parser


@pytest.fixture
def schema_1():
    return Parser.from_file("./test_1/schema.json")


def test_read_1(schema_1):
    res = schema_1.read_file("./test_1/in/1.edi")
    assert res == {
        "Header": {
            "Field1": "E",
            "Field2": "FR00",
            "Field3": datetime.datetime(2024, 5, 31, 0, 0),
            "Field5": "T009999",
            "Field6": "EUR",
        },
        "Lines": [
            {
                "LinesHeader": "L",
                "Field1": "POFR10-058040",
                "Field2": 1000,
                "Field3": "CJ57219",
                "Field4": "UN",
                "Field5": 1,
                "Field6": "2",
                "Field7": "CORE-M5  4 64GO                SMD",
                "Field9": "GR965125287FR",
                "Field10": "CHRONOPOST",
            }
        ],
    }


def test_read_2(schema_1):
    res = schema_1.read_file("./test_1/in/2.edi")
    assert res == {
        "Header": {
            "Field1": "E",
            "Field2": "FR00",
            "Field3": datetime.datetime(2024, 5, 31, 0, 0),
            "Field5": "T009999",
            "Field6": "EUR",
        },
        "Lines": [
            {
                "LinesHeader": "L",
                "Field1": "POFR10-XXXXXX",
                "Field2": 1000,
                "Field3": "CJ09425",
                "Field4": "UN",
                "Field5": 10,
                "Field6": "2",
                "Field7": "TEMPERED GLASS DESIGNED FOR    ACCS",
                "Field8": "GALAXY A54 5G",
                "Field9": "AA965112840FR",
                "Field10": "CHRONOPOST",
            },
            {
                "LinesHeader": "L",
                "Field1": "POFR10-XXXXXX",
                "Field2": 2000,
                "Field3": "CJ69831",
                "Field4": "UN",
                "Field5": 1,
                "Field6": "2",
                "Field7": "ROG CETRA TRUE WIRELESS-       ACCS",
                "Field9": "AA965112840FR",
                "Field10": "CHRONOPOST",
                "LotNumber": [{"LotNumberHeader": "N", "Field1": "R8YHNB209318"}],
            },
        ],
    }


def test_read_3(schema_1):
    res = schema_1.read_file("./test_1/in/3.edi")
    assert res == {
        "Header": {
            "Field1": "E",
            "Field2": "FR00",
            "Field3": datetime.datetime(2024, 6, 4, 0, 0),
            "Field5": "T001234",
            "Field6": "EUR",
        },
        "Lines": [
            {
                "LinesHeader": "L",
                "Field1": "ZZAA10-007600",
                "Field2": 1000,
                "Field3": "A317722",
                "Field4": "UN",
                "Field5": 30,
                "Field6": "2",
                "Field8": "ALE-30H ESSENTIAL DESKPHONE",
                "Field9": "677258693",
                "LotNumber": [
                    {"LotNumberHeader": "N", "Field1": "XXX223808386"},
                    {"LotNumberHeader": "N", "Field1": "XXX223807642"},
                    {"LotNumberHeader": "N", "Field1": "XXX223808696"},
                    {"LotNumberHeader": "N", "Field1": "XXX224105209"},
                    {"LotNumberHeader": "N", "Field1": "XXX223807893"},
                    {"LotNumberHeader": "N", "Field1": "XXX223810143"},
                    {"LotNumberHeader": "N", "Field1": "XXX223813829"},
                    {"LotNumberHeader": "N", "Field1": "XXX223808458"},
                    {"LotNumberHeader": "N", "Field1": "XXX223807626"},
                    {"LotNumberHeader": "N", "Field1": "XXX224104617"},
                    {"LotNumberHeader": "N", "Field1": "XXX223808348"},
                    {"LotNumberHeader": "N", "Field1": "XXX223811187"},
                    {"LotNumberHeader": "N", "Field1": "XXX223807973"},
                    {"LotNumberHeader": "N", "Field1": "XXX223808507"},
                    {"LotNumberHeader": "N", "Field1": "XXX223809799"},
                    {"LotNumberHeader": "N", "Field1": "XXX223809787"},
                    {"LotNumberHeader": "N", "Field1": "XXX223811123"},
                    {"LotNumberHeader": "N", "Field1": "XXX224101527"},
                    {"LotNumberHeader": "N", "Field1": "XXX223815910"},
                    {"LotNumberHeader": "N", "Field1": "XXX224103411"},
                    {"LotNumberHeader": "N", "Field1": "XXX223810148"},
                    {"LotNumberHeader": "N", "Field1": "XXX223809992"},
                    {"LotNumberHeader": "N", "Field1": "XXX224203779"},
                    {"LotNumberHeader": "N", "Field1": "XXX223810042"},
                    {"LotNumberHeader": "N", "Field1": "XXX223807570"},
                    {"LotNumberHeader": "N", "Field1": "XXX223807596"},
                    {"LotNumberHeader": "N", "Field1": "XXX223807563"},
                    {"LotNumberHeader": "N", "Field1": "XXX223807490"},
                    {"LotNumberHeader": "N", "Field1": "XXX223810507"},
                    {"LotNumberHeader": "N", "Field1": "XXX224203603"},
                ],
            },
            {
                "LinesHeader": "L",
                "Field1": "ZZAA10-007600",
                "Field2": 2000,
                "Field3": "A318087",
                "Field4": "UN",
                "Field5": 30,
                "Field6": "2",
                "Field8": "ALE-10 MAGNETIC ALPHABETIC KEYBOARD",
                "Field9": "677258693",
                "LotNumber": [
                    {"LotNumberHeader": "N", "Field1": "XXX231707847"},
                    {"LotNumberHeader": "N", "Field1": "XXX231707886"},
                    {"LotNumberHeader": "N", "Field1": "XXX231708742"},
                    {"LotNumberHeader": "N", "Field1": "XXX231707906"},
                    {"LotNumberHeader": "N", "Field1": "XXX231707975"},
                    {"LotNumberHeader": "N", "Field1": "XXX231708070"},
                    {"LotNumberHeader": "N", "Field1": "XXX231707912"},
                    {"LotNumberHeader": "N", "Field1": "XXX231707962"},
                    {"LotNumberHeader": "N", "Field1": "XXX231707977"},
                    {"LotNumberHeader": "N", "Field1": "XXX231708174"},
                    {"LotNumberHeader": "N", "Field1": "XXX231707809"},
                    {"LotNumberHeader": "N", "Field1": "XXX231707873"},
                    {"LotNumberHeader": "N", "Field1": "XXX231707959"},
                    {"LotNumberHeader": "N", "Field1": "XXX231707954"},
                    {"LotNumberHeader": "N", "Field1": "XXX231707923"},
                    {"LotNumberHeader": "N", "Field1": "XXX231707783"},
                    {"LotNumberHeader": "N", "Field1": "XXX231707854"},
                    {"LotNumberHeader": "N", "Field1": "XXX231708305"},
                    {"LotNumberHeader": "N", "Field1": "XXX231707860"},
                    {"LotNumberHeader": "N", "Field1": "XXX231707838"},
                    {"LotNumberHeader": "N", "Field1": "XXX231707925"},
                    {"LotNumberHeader": "N", "Field1": "XXX231707849"},
                    {"LotNumberHeader": "N", "Field1": "XXX231707867"},
                    {"LotNumberHeader": "N", "Field1": "XXX231707949"},
                    {"LotNumberHeader": "N", "Field1": "XXX231707815"},
                    {"LotNumberHeader": "N", "Field1": "XXX231707950"},
                    {"LotNumberHeader": "N", "Field1": "XXX231707788"},
                    {"LotNumberHeader": "N", "Field1": "XXX231707905"},
                    {"LotNumberHeader": "N", "Field1": "XXX231707820"},
                    {"LotNumberHeader": "N", "Field1": "XXX231707961"},
                ],
            },
        ],
    }


def test_read_4(schema_1):
    res = schema_1.read_file("./test_1/in/4.edi")
    assert res == {
        "Header": {
            "Field1": "E",
            "Field2": "FR00",
            "Field3": datetime.datetime(2024, 6, 5, 0, 0),
            "Field5": "T001234",
            "Field6": "EUR",
        },
        "Lines": [
            {
                "LinesHeader": "L",
                "Field1": "ZZAA10-007606",
                "Field2": 2000,
                "Field3": "A317722",
                "Field4": "UN",
                "Field5": 1,
                "Field6": "2",
                "Field8": "ALE-30H ESSENTIAL DESKPHONE",
                "Field9": "677258755",
                "LotNumber": [{"LotNumberHeader": "N", "Field1": "XXX223810332"}],
            },
            {
                "LinesHeader": "L",
                "Field1": "ZZAA10-007606",
                "Field2": 3000,
                "Field3": "A305326",
                "Field4": "UN",
                "Field5": 1,
                "Field6": "2",
                "Field8": "EM200 SMART EXPANSION MODULE",
                "Field9": "677258755",
                "LotNumber": [{"LotNumberHeader": "N", "Field1": "TPK231804407"}],
            },
        ],
    }
