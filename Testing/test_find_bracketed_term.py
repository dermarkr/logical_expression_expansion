import pytest

from src.find_bracketed_term import get_bracketed_terms

# @pytest.mark.parametrize("expr, bracketed",
#                          [("A", []), ("A && B", []),
#                           ("(A)", ["A"]),
#                           ("A && (B || C)", ["B || C"]),
#                           ("A && (B && (C && (D || E)))", ["B && (C && (D || E))"]),
#                           ("A && (B && (C && (D || E))) && F", ["B && (C && (D || E))"]),
#                           ("A && (B && (C && (D || E))) && (F && G)", ["B && (C && (D || E))", "F && G"])])
# def test_single_level(expr, bracketed):
#     returned = get_bracketed_terms(expr)
#
#     assert returned == bracketed
