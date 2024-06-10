import json
from datetime import date, datetime
from json import JSONEncoder
from typing import Any

PYTHON_TYPES = {
    "int": int,
    "float": float,
    "str": str,
}
DEFAULT_SEPARATOR = "space"


class DateTimeEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            # return obj.isoformat()
            return str(obj)


def size_of(item: Any) -> int:
    """Return size of any values"""
    if item is None:
        return 0
    if isinstance(item, int):
        return len(str(item))
    if isinstance(item, float):
        return len(f"{item:.2f}")
    return len(item)


def is_equal(value: Any, length) -> bool:
    if isinstance(value, datetime):
        return True
    return not bool(size_of(value) > length)


def json_dump(data):
    """Shortcut to json.dumps with custom encoder"""
    return json.dumps(data, indent=4, cls=DateTimeEncoder)
