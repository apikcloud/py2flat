from datetime import datetime

import pytest

from py2flat.converters import Converter


def test_converter_methods():
    with pytest.raises(NotImplementedError):
        Converter.input("input")

    with pytest.raises(NotImplementedError):
        Converter.output("output")


def test_converters():
    assert Converter.list() == [
        "X 1 000",
        "X 10 000",
        "9v5",
        "12v2",
        "13v2",
        "17v2",
        "SSAAMMJJ",
        "AAAAMMJJ",
    ]


def test_9v5():
    assert Converter.by_name("9v5").input("000000123,99999") == 123.99999
    assert Converter.by_name("9v5").output(123.45) == "000000123,45000"


def test_12v2():
    assert Converter.by_name("12v2").input("000000000123,45") == 123.45
    assert Converter.by_name("12v2").output(123.45) == "000000000123,45"


def test_13v2():
    assert Converter.by_name("13v2").input("00000123,45") == 123.45
    assert Converter.by_name("13v2").output(123.45) == "0000000000123,45"


def test_17v2():
    assert Converter.by_name("17v2").input("00000123,45") == 123.45
    assert Converter.by_name("17v2").output(123.45) == "00000000000000123,45"


def test_float_to_int_1():
    assert Converter.by_name("X 1 000").input(1250) == 1.25
    assert Converter.by_name("X 1 000").output(1.25) == 1250

    assert isinstance(Converter.by_name("X 1 000").input(1000), float)


def test_float_to_int_2():
    assert Converter.by_name("X 10 000").input(99900) == 9.99
    assert Converter.by_name("X 10 000").output(1.25) == 12500


def test_date():
    assert Converter.by_name("SSAAMMJJ").input("20240501") == datetime(2024, 5, 1)
    assert Converter.by_name("SSAAMMJJ").output(datetime(2024, 5, 1)) == "20240501"
