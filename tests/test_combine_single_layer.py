import pytest

from src.combine_single_layer import combine_simple_primed_expr


@pytest.mark.parametrize("expr, expected", [
    ["11", [11]],
    ["11 && 13", [11 * 13]],
    ["11 || 13", [11, 13]],
    ["11 && 13 || 17", [11 * 13, 17]],
    ["11 || 13 && 17", [11, 13 * 17]],
    ["11 && 13 || 17 || 19 && 23", [11 * 13, 17, 19 * 23]]
])
def test_combine_single_layer(expr, expected):
    combined = combine_simple_primed_expr(expr)
    assert combined == expected
