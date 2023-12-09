import pytest

from src.expandexpression import ExpandExpression


@pytest.fixture
def ee():
    prime_map = [["A", 11], ["B", 13], ["C", 17], ["D", 19], ["E", 23], ["F", 29], ["G", 31]]

    ee = ExpandExpression(prime_map=prime_map)
    return ee


@pytest.mark.parametrize("value, used_primes, expected_primes", [
    [15, [2, 3, 5, 7, 11, 13], [3, 5]],
    [11 * 13, [11, 13, 17, 19], [11, 13]],
    [13 * 17 * 37, [11, 13, 17, 19, 29, 37], [13, 17, 37]],
    [14, [11, 13, 17, 19, 29, 37], []],
    [99, [11, 13, 17, 19, 29, 37], [11]],

])
def test_get_component_primes(ee, value, used_primes, expected_primes):
    ee.used_primes = used_primes
    primes = ee.get_component_primes(value=value)
    assert expected_primes == primes


@pytest.mark.parametrize("value, expected_expr", [
    [11 * 13, "A && B"],
    [13 * 19 * 31, "B && D && G"],
    [11 * 11, "A"]
])
def test_expand_value_to_components(ee, value, expected_expr):
    expr = ee.expand_value_to_components(value)
    assert expected_expr == expr


@pytest.mark.parametrize("value_list, expected_expr", [
    [[11 * 13], "A && B"],
    [[13 * 19 * 31, 11 * 13], "B && D && G || A && B"],
    [[11 * 11], "A"]
])
def test_expand_expr_list(ee, value_list, expected_expr):
    expr = ee.expand_expr_list(value_list)
    assert expected_expr == expr
