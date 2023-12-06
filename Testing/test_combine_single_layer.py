import pytest

from src.combine_single_layer import combine_single_layer


@pytest.mark.parametrize("expr, expected", [
    ["11", [11]],
    ["11 && 13", [11 * 13]],
    ["11 || 13", [11, 13]],
    ["11 && 13 || 17", [11 * 13, 17]],
    ["11 || 13 && 17", [11, 13 * 17]],
    ["11 && 13 || 17 || 19 && 23", [11 * 13, 17, 19 * 23]]
])
def test_combine_single_layer(expr, expected):
    combined = combine_single_layer(expr)
    assert combined == expected
