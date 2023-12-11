import pytest

from src.combine_layers import combine_layers


@pytest.mark.parametrize("expr, expected", [
    ["11", "11"],
    ["11 && 13", f"{11 * 13}"],
    ["11 && (13 || 17)", f"{11 * 13} || {11 * 17}"],
    ["11 && 13 || (17 || 19 && 23)", f"{11 * 13} || 17 || {19 * 23}"],
    ["11 && 13 && (17 || 19 && 23)", f"{11 * 13 * 17} || {11 * 13 * 19 * 23}"]
])
def test_combine_layers(expr, expected):
    combined = combine_layers(expr)
    assert expected == combined
