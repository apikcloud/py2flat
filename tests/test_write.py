import datetime

import pytest

from py2flat.exchange import Exchange
from py2flat.parser import Parser


@pytest.fixture
def exchange():
    parser = Parser.from_file("./test_3/schema.json")
    return Exchange(parser)


def test_write_1(exchange):
    lines = [
        {
            "POPLIN": 4373,
            "ITMREF": "PR/00002",
            "PRHFCY": "FR11",
            "UOM": "UN",
            "QTYUOM": 1.0,
            "GROPRI": 780.0,
            "TEXTE91": "",
            "YSPESOHFLG": "2",
            "YSPESOHDES": "123",
            "RS_LIVRAISON": "BETOOBE",
            "ADR_LIGNE_1": "19C Av Albert Schweitzer",
            "ADR_LIGNE_2": "",
            "ADR_POSCOD": "13210",
            "ADR_VILLE": "St Rémy De Provence",
            "ADR_PAYS": "France",
            "CodePays": "FR",
            "Nom_Contact_livraison": "BETOOBE",
            "Tel_Contact_livraison": "+33 9 72 19 09 70",
            "Nom_contact_connexing": "Database Support",
            "Tel_contact_connexing": "",
            "Email_contact_connexing": "julien@betoobe.fr",
            "ITMREF_FRNS": "code.noir.32G0",
            "ITMDES": "NOm.code.noir.32GO",
        }
    ]
    exchange.set_header(
        **{
            "POHFCY": "FR11",
            "POHNUM": "PBE02223",
            "ORDDAT": datetime.datetime(2024, 6, 18, 13, 6, 2),
            "BPSNUM": "T00016",
            "ORDREF": "PBE02223",
            "CODE_BY": "T00007",
            "CODE_UD": "T00007",
            "CUR": "EUR",
            "TOTORD": 780.0,
            "EXTRCPDAT1": datetime.datetime(2024, 6, 19, 13, 5, 56),
            "TEXTE71": "123123",
            "TEXTE81": "456456",
            "BK": "  ",
            "CODE_LANGUE": "fr_FR",
        }
    )

    # exchange.set_header(
    #     **{
    #         "POHFCY": "FR11",
    #         "POHNUM": "PBE02223",
    #         "ORDDAT": datetime.datetime(2024, 6, 18, 13, 6, 2),
    #         "BPSNUM": "T00016",
    #         "ORDREF": "PBE02223",
    #         "CODE_BY": "T00007",
    #         "CODE_UD": "T00007",
    #         "CUR": "EUR",
    #         "TOTORD": 780.0,
    #         "EXTRCPDAT1": datetime.datetime(2024, 6, 19, 13, 5, 56),
    #         "TEXTE71": "123123",
    #         "TEXTE81": "456456",
    #         "BK": "  ",
    #         "CODE_LANGUE": "fr_FR",
    #     }
    # )

    for line in lines:
        exchange.add_segment("Lines", line)

    with open("./test_3/out/1.edi", encoding="utf-8") as file:
        output = list(filter(bool, file.read().split("\n")))

    res = exchange.dump().split("\n")

    assert len(res) == len(output)

    assert res[0][:512] == output[0][:512]
    assert len(res[0]) == len(output[0])
    assert len(res[1]) == len(output[1])

    assert res[1][:1000] == output[1][:1000]
