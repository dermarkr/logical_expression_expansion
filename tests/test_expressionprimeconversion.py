import pytest

from src.expressionprimeconversion.expressionprimeconversion import ExpressionPrimeConversion, expr_list_to_str, \
    get_terms_in_expr, get_next_prime


@pytest.fixture
def ee():
    prime_map = [["A", 11], ["B", 13], ["C", 17], ["D", 19], ["E", 23], ["F", 29], ["G", 31]]

    ee = ExpressionPrimeConversion()
    ee.prime_map = prime_map
    ee.get_used_primes()
    return ee


@pytest.mark.parametrize("value, used_primes, expected_primes", [
    [15, [2, 3, 5, 7, 11, 13], [3, 5]],
    [11 * 13, [11, 13, 17, 19], [11, 13]],
    [13 * 17 * 37, [11, 13, 17, 19, 29, 37], [13, 17, 37]],
    [14, [11, 13, 17, 19, 29, 37], [0]],
    [99, [11, 13, 17, 19, 29, 37], [11]],
])
def test_get_component_primes(ee, value, used_primes, expected_primes):
    if expected_primes[0] == 0:
        expected_primes = list()

    ee.used_primes = used_primes
    primes = ee.get_component_primes(value)
    assert expected_primes == primes


@pytest.mark.parametrize("value, expected_expr", [
    [11 * 13, "11 && 13"],
    [13 * 19 * 31, "13 && 19 && 31"],
    [11 * 11, "11"]
])
def test_expand_value_to_components(ee, value, expected_expr):
    expr = ee.expand_value_to_components(value)
    assert expected_expr == expr


@pytest.mark.parametrize("value_list, expected_expr", [
    [[11 * 13], "143"],
    [[13 * 19 * 31, 11 * 13], f"{13 * 19 * 31} || {11 * 13}"],
    [[11 * 11], "121"]
])
def test_expand_expr_list(value_list, expected_expr):
    expr = expr_list_to_str(value_list)
    assert expected_expr == expr


@pytest.mark.parametrize("primed_expr, expected_expr", [
    ["11 && 13", "A && B"],
    ["13 && 19 && 31 || 11 && 13", "B && D && G || A && B"],
    ["11", "A"]
])
def test_convert_primed_expr_to_chars(ee, primed_expr, expected_expr):
    expr = ee.convert_primed_expr_to_chars(primed_expr)
    assert expected_expr == expr


@pytest.mark.parametrize("org_expr, expected_expr", [
    [f"{11 * 13}", "11 && 13"],
    [f"{11 * 11}", "11"],
    [f"11 || 143", "11 || 11 && 13"]
])
def test_fully_expand_expression(ee, org_expr, expected_expr):
    ret_expr = ee.fully_expand_expression(expr=org_expr)
    assert expected_expr == ret_expr


@pytest.mark.parametrize("lower_bound, next_prime", [[0, 1], [1, 2], [2, 3], [3, 5], [89, 97]])
def test_get_next_prime(lower_bound, next_prime):
    returned_prime = get_next_prime(lower_bound=lower_bound)

    assert next_prime == returned_prime


@pytest.mark.parametrize("terms, expected", [[["A"], [["A", 11]]], [["A", "B"], [["A", 11], ["B", 13]]],
                                             [["A", "B", "C"], [["A", 11], ["B", 13], ["C", 17]]],
                                             [["A", "B", "D"], [["A", 11], ["B", 13], ["D", 17]]],
                                             [["AZF"], [["AZF", 11]]]])
def test_make_prime_map(ee, terms, expected):
    ee.make_prime_map(terms)

    assert expected == ee.prime_map


@pytest.mark.parametrize("expr, expected", [["A", ["A"]], ["A || B", ["A", "B"]], ["A || (B || C)", ["A", "B", "C"]], ])
def test_get_terms_in_expr(ee, expr, expected):
    terms = get_terms_in_expr(expr)

    assert expected == terms


@pytest.mark.parametrize("expr, expected", [
    ["A", "11"],
    ["A || B", "11 || 13"],
    ["A && B || C", "11 && 13 || 17"]
])
def test_replace_terms_with_prime(ee, expr, expected):
    converted = ee.replace_terms_with_prime(expr)
    assert expected == converted


@pytest.mark.parametrize("expr, expected, expected_prime_map", [
    ["A", "11", [["A", 11]]],
    ["A || B", "11 || 13", [["A", 11], ["B", 13]]],
    ["A && B || C", "11 && 13 || 17", [["A", 11], ["B", 13], ["C", 17]]]
])
def test_prime_expression(ee, expr, expected, expected_prime_map):
    converted = ee.prime_expression(expr)
    assert expected == converted
    assert expected_prime_map == ee.prime_map


@pytest.mark.parametrize("prime_map, expect_used", [
    [[["A", 11]], [11]],
    [[["A", 11], ["B", 13]], [11, 13]],
    [[["A", 11], ["B", 13], ["C", 17]], [11, 13, 17]]
])
def test_get_used_primes(ee, prime_map, expect_used):
    ee.prime_map = prime_map
    ee.get_used_primes()
    assert expect_used == ee.used_primes
