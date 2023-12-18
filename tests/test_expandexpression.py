import pytest

from src.expandexpression.expandexpression import combine_layers, combine_simple_primed_expr, find_bracket_bounds


@pytest.mark.parametrize("expr, expected", [
    ["11", "11"],
    ["11 && 13", f"{11 * 13}"],
    ["11 && (13 || 17)", f"{11 * 13} || {11 * 17}"],
    ["11 && 13 || (17 || 19 && 23)", f"{11 * 13} || 17 || {19 * 23}"],
    ["11 && 13 && (17 || 19 && 23)", f"{11 * 13 * 17} || {11 * 13 * 19 * 23}"],
    ["11 && 13 && (23 && (17 || 19))", f"{11 * 13 * 17 * 23} || {11 * 13 * 19 * 23}"],
    ["((11 || 13) && (19 || 23))", f"{11 * 19} || {13 * 19} || {11 * 23} || {13 * 23}"],
    ["11 && 13 && ((17 || 19) && 23)", f"{11 * 13 * 17 * 23} || {11 * 13 * 19 * 23}"],
    ["11 && (13 && (17 || 31)) || 23 && 29 && (11 && 13 || 19)",
     f"{11 * 13 * 17} || {11 * 13 * 31} || {23 * 29 * 11 * 13} || {23 * 29 * 19}"]
])
def test_combine_layers(expr, expected):
    combined = combine_layers(expr)
    assert expected == combined


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


@pytest.mark.parametrize("expr, start_index, end_index", [
    ("A && (B || C)", 5, 12),
    ("A && (B && (C && (D || E)))", 5, 26),
    ("A && (B && (C && (D || E))) && F", 5, 26),
    ("A && (B && (C && (D || E))) && (F && G)", 5, 26)

])
def test_find_bracket_bounds(expr, start_index, end_index):
    found_index = find_bracket_bounds(expr, start_index)

    assert end_index == found_index
