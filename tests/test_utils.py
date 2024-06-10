from datetime import datetime

import pytest

from py2flat.utils import is_equal, size_of


@pytest.mark.parametrize(
    "value, result",
    [
        ("1000", 4),
        (1000, 4),
        (1.2, 4),
        (None, 0),
    ],
)
def test_size_of(value, result):
    assert size_of(value) == result


@pytest.mark.parametrize(
    "value, length",
    [
        ("1000", 4),
        (1000, 4),
        (1.2, 4),
        (None, 0),
        (datetime.now(), 1),
        (datetime.now(), 99),
    ],
)
def test_is_equal(value, length):
    assert is_equal(value, length)
