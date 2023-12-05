import pytest

from src.find_bracketed_term import find_bracket_bounds


@pytest.mark.parametrize("expr, start_index, end_index", [
    ("A && (B || C)", 5, 12),
    ("A && (B && (C && (D || E)))", 5, 26),
    ("A && (B && (C && (D || E))) && F", 5, 26),
    ("A && (B && (C && (D || E))) && (F && G)", 5, 26)

])
def test_find_bracket_bounds(expr, start_index, end_index):
    found_index = find_bracket_bounds(expr, start_index)

    assert end_index == found_index
