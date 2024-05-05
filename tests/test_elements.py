import pytest

from py2flat.element import Element
from py2flat.exceptions import ExceededSize


@pytest.fixture
def element_1():
    return Element(
        name="ID",
        string="Identifier",
        size=3,
        required=True,
        default="IDX",
    )


@pytest.fixture
def element_2():
    return Element(
        name="Name",
        string="Name",
        size=10,
        required=True,
    )


@pytest.fixture
def element_3():
    return Element(
        name="Description",
        string="Description",
        size=10,
    )


@pytest.fixture
def element_4():
    return Element(
        name="Number",
        string="Number",
        size=20,
        required=True,
        ttype="int",
        converter="X 1 000",
        justify="right",
    )


def test_dump_element_1(element_1):
    assert element_1.dump() == "IDX"


def test_dump_element_2(element_2):
    element_2.set_value("Name A")
    element_2.justify = "right"
    assert element_2.dump() == "    Name A"


def test_parse_element_3(element_3):
    assert element_3.parse("   Lorem ") == "Lorem"

    with pytest.raises(ExceededSize) as excinfo:
        element_3.parse("Lorem ipsum dolor sit amet.")
        assert str(excinfo.value) == ""

    assert element_3.parse("Lorem ipsum dolor sit amet.", truncate=True) == "Lorem ipsu"


def test_dump_element_3(element_3):
    element_3.set_value("Lorem")
    assert element_3._value == "Lorem"
    assert element_3.dump() == "Lorem     "

    element_3.justify = "right"
    assert element_3.dump() == "     Lorem"


def test_dump_element_4(element_4):
    assert element_4.parse("123450") == 123.45
    element_4.set_value(123.45)
    assert element_4.dump() == "              123450"

    # assert element_4.parse("XXX")


@pytest.mark.parametrize(
    "value, result",
    [
        ("123456789000", 1234567.890),  # truncate
        ("12345678900", 1234567.890),  # truncate
        ("1234567890", 1234567.890),
        (" 123456789", 123456.789),
        ("  12345678", 12345.678),
        ("   1234567", 1234.567),
        ("    123456", 123.456),
        ("     12345", 12.345),
        ("      1234", 1.234),
        ("       123", 0.123),
        ("        12", 0.012),
        ("         1", 0.001),
        ("       1  ", 0.001),
        ("     1    ", 0.001),
        ("1", 0.001),
        ("          ", None),
        ("", None),
    ],
)
def test_parse_element_with_converter(value, result):
    element = Element(
        name="Number",
        string="Number",
        size=10,
        ttype="int",
        converter="X 1 000",
        justify="right",
    )
    assert element.parse(value, truncate=True) == result


@pytest.mark.parametrize(
    "value, result",
    [
        (1234567.89, "1234567890"),
        (123456.789, " 123456789"),
        (12345.6789, "  12345678"),
        (1234.56789, "   1234567"),
        (1234.50000, "   1234500"),
        (123.450000, "    123450"),
        (0.99900000, "       999"),
        (0.09900000, "        99"),
        (0.00900000, "         9"),
        (None, 10 * " "),
    ],
)
def test_dump_element_with_converter(value, result):
    element = Element(
        name="Number",
        string="Number",
        size=10,
        ttype="int",
        converter="X 1 000",
        justify="right",
    )
    element.set_value(value)
    assert element.dump() == result
