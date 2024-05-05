from datetime import datetime


class Converter:
    _name = None
    _subclasses = {}

    @classmethod
    def list(cls):
        return list(cls._subclasses.keys())

    @classmethod
    def by_name(cls, name):
        return cls._subclasses[name]

    def __init_subclass__(cls):
        Converter._subclasses[cls._name] = cls

    @staticmethod
    def input(item):
        raise NotImplementedError()

    @staticmethod
    def output(item):
        raise NotImplementedError()


class ConverterFloatToInteger1(Converter):
    _name = "X 1 000"

    @staticmethod
    def input(item: int) -> float:
        return float(item / 1000)

    @staticmethod
    def output(item: float) -> int:
        return int(item * 1000)


class ConverterFloatToInteger2(Converter):
    _name = "X 10 000"

    @staticmethod
    def input(item: int) -> float:
        return float(item / 10000)

    @staticmethod
    def output(item: float) -> int:
        return int(item * 10000)


class ConverterDate8(Converter):
    """Convert YYYYMMDD to datetime object"""

    _name = "SSAAMMJJ"

    @staticmethod
    def input(item: str) -> datetime:
        return datetime.strptime(item, "%Y%m%d")

    @staticmethod
    def output(item: datetime) -> str:
        return item.strftime("%Y%m%d")


class Converter13v2(Converter):
    """eg. 0000000000000,00"""

    _name = "13v2"

    @staticmethod
    def input(item: str) -> float:
        return float(item.replace(",", "."))

    @staticmethod
    def output(item: float) -> str:
        return f"{item:.2f}".replace(".", ",").rjust(16, "0")
