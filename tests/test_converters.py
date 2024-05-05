from datetime import datetime

from py2flat.converters import Converter


def test_converters():
    assert Converter.list() == ["X 1 000", "X 10 000", "SSAAMMJJ", "13v2"]


def test_13v2():
    assert Converter.by_name("13v2").input("00000123,45") == 123.45
    assert Converter.by_name("13v2").output(123.45) == "0000000000123,45"


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
