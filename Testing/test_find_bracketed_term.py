import pytest

from src.find_bracketed_term import find_bracket_bounds, find_max_depth


@pytest.mark.parametrize("expr, start_index, end_index", [
    ("A && (B || C)", 5, 12),
    ("A && (B && (C && (D || E)))", 5, 26),
    ("A && (B && (C && (D || E))) && F", 5, 26),
    ("A && (B && (C && (D || E))) && (F && G)", 5, 26)

])
def test_find_bracket_bounds(expr, start_index, end_index):
    found_index = find_bracket_bounds(expr, start_index)

    assert end_index == found_index


@pytest.mark.parametrize("expr, expected_depth", [
    ("A && (B || C)", 1),
    ("A && (B && (C && (D || E)))", 3),
    ("A && (B && (C && (D || E))) && F", 3),
    ("A && (B && (C && (D || E))) && (F && G)", 3),
    ("A && (B && (C && (D || E))) && (F && (G && (A || (B || C))))", 4)
])
def test_find_max_depth(expr, expected_depth):
    found_depth = find_max_depth(expr)

    assert expected_depth == found_depth
