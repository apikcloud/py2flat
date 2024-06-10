from datetime import datetime


class Converter:
    _name = None
    _subclasses = {}

    @classmethod
    def list(cls):
        """List subclasses"""
        return list(cls._subclasses.keys())

    @classmethod
    def by_name(cls, name):
        """Get subclass by name"""
        return cls._subclasses[name]

    def __init_subclass__(cls):
        """Keeps track of all subclass instantiations"""
        if cls._name:
            Converter._subclasses[cls._name] = cls

    @staticmethod
    def input(item):
        raise NotImplementedError()

    @staticmethod
    def output(item):
        raise NotImplementedError()


# Base converters


class BaseInteger(Converter):
    _multiplier = None

    @classmethod
    def input(cls: Converter, item: int) -> float:
        return float(item / cls._multiplier)

    @classmethod
    def output(cls: Converter, item: float) -> int:
        return int(item * cls._multiplier)


class BaseFloat(Converter):
    """eg. 000000000.00000"""

    _format = None
    _length = None
    _fill = "0"

    @staticmethod
    def input(item: str) -> float:
        return float(item.replace(",", "."))

    @classmethod
    def output(cls: Converter, item: float) -> str:
        return cls._format.format(item).replace(".", ",").rjust(cls._length, cls._fill)


class BaseDate(Converter):
    _format = None

    @classmethod
    def input(cls: Converter, item: str) -> datetime:
        return datetime.strptime(item, cls._format)

    @classmethod
    def output(cls: Converter, item: datetime) -> str:
        return item.strftime(cls._format)


# Converters


class ConverterFloatToInteger1(BaseInteger):
    """x1000 Converter, float to integer"""

    _name = "X 1 000"
    _multiplier = 1000


class ConverterFloatToInteger2(BaseInteger):
    """x10000 Converter, float to integer"""

    _name = "X 10 000"
    _multiplier = 10000


class Converter9v5(BaseFloat):
    """eg. 000000000.00000"""

    _name = "9v5"
    _format = "{:.5f}"
    _length = 15


class Converter12v2(BaseFloat):
    """eg. 000000000000.00"""

    _name = "12v2"
    _format = "{:.2f}"
    _length = 15


class Converter13v2(BaseFloat):
    """eg. 0000000000000,00"""

    _name = "13v2"
    _format = "{:.2f}"
    _length = 16


class Converter17v2(BaseFloat):
    """eg. 00000000000000000.00"""

    _name = "17v2"
    _format = "{:.2f}"
    _length = 20


class ConverterDate1(BaseDate):
    """Convert YYYYMMDD to datetime object"""

    _name = "SSAAMMJJ"
    _format = "%Y%m%d"


class ConverterDate2(ConverterDate1):
    _name = "AAAAMMJJ"
