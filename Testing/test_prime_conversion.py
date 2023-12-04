import pytest

from src.prime_conversion import get_next_prime, get_terms_in_expr, make_prime_map, replace_terms_with_prime


@pytest.mark.parametrize("lower_bound, next_prime", [[0, 1], [1, 2], [2, 3], [3, 5], [89, 97]])
def test_get_next_prime(lower_bound, next_prime):
    returned_prime = get_next_prime(lower_bound=lower_bound)

    assert next_prime == returned_prime


@pytest.mark.parametrize("terms, expected", [[["A"], [["A", 11]]], [["A", "B"], [["A", 11], ["B", 13]]],
                                             [["A", "B", "C"], [["A", 11], ["B", 13], ["C", 17]]],
                                             [["A", "B", "D"], [["A", 11], ["B", 13], ["D", 17]]],
                                             [["AZF"], ["AZF", 11]]])
def test_make_prime_map(terms, expected):
    prime_map = make_prime_map(terms)

    assert expected, prime_map


@pytest.mark.parametrize("expr, expected", [["A", ["A"]], ["A || B", ["A", "B"]], ["A || (B || C)", ["A", "B", "C"]], ])
def test_get_terms_in_expr(expr, expected):
    terms = get_terms_in_expr(expr)

    assert expected == terms


@pytest.mark.parametrize("expr, expected", [
    ["A", "11"],
    ["A || B", "11 || 13"],
    ["A && B || C", "11 && 13 || 17"],
    ["TRE && ZAS", "11 && 13"]
])
def test_replace_terms_with_prime(expr, expected):
    converted = replace_terms_with_prime(expr)
    assert expected == converted
