PYTHON_TYPES = {
    "int": int,
    "float": float,
    "str": str,
}
DEFAULT_SEPARATOR = "space"


def size_of(item: str | int | float) -> int:
    """Return size of any values"""
    if item is None:
        return 0
    if isinstance(item, int):
        return len(str(item))
    if isinstance(item, float):
        return len(f"{item:.2f}")
    return len(item)


def is_equal(value: str | int | float, length) -> bool:
    return not bool(size_of(value) > length)
