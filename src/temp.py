import re

from find_bracketed_term import find_bracket_bounds
from prime_conversion import replace_terms_with_prime


def drill_down(expr: str) -> list:
    """

    :param expr:
    :return:
    """

    i = 0

    primes = re.findall(r"[0-9]+", expr)

    brackets = list()

    current_bracket_index = 0

    while i < len(expr):

        if expr[i] == "(":
            end_index = find_bracket_bounds(expr=expr, start_index=i)

            if end_index == i:
                end_index = None

            if end_index:
                bracket_list = drill_down(expr=expr[i + 1: end_index])


if __name__ == "__main__":
    original_expression = "A && (B && (C || D))"
    # original_expression = "A && B"
    primed_expression = replace_terms_with_prime(expr=original_expression)

    drill_down(primed_expression)

    print(primed_expression)
