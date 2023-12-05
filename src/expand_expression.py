import re

from find_bracketed_term import find_bracket_bounds
from prime_conversion import replace_terms_with_prime


def expand_expression(expr: str) -> str:
    """

    :param expr:
    :return:
    """

    i = 0

    while i < len(expr):
        end_index = None
        if expr[i] == "(":
            end_index = find_bracket_bounds(expr=expr, start_index=i)

            if end_index == i:
                end_index = None

        if end_index:
            temp_expr = expand_expression(expr[i + 1:end_index])
        else:
            temp_expr = ""

        # if temp_expr:
        outside_primes = re.findall(r"[0-9]+", expr[:i])
        bracket_primes = re.findall(r"[0-9]+", temp_expr)
        operators = re.findall(r"&&|\|\|", expr[:i])

        multiplied_outside_primes = ""

        current_prime = int(outside_primes[0])

        for j, operator in enumerate(operators):
            if operator == "&&":
                if j + 1 < len(outside_primes):
                    current_prime = current_prime * int(outside_primes[j + 1])
                else:
                    multiplied_outside_primes += f"{current_prime} && "
                    current_prime = 1
            else:
                multiplied_outside_primes += f"{current_prime} || "

        print(multiplied_outside_primes)

        # temp_expr = multiply_out_primes(expr = temp_expr)

        i += 1

    return expr


if __name__ == "__main__":
    # original_expression = "A && (B && (C || D))"
    original_expression = "A && B"
    primed_expression = replace_terms_with_prime(expr=original_expression)

    expand_expression(primed_expression)

    print(primed_expression)
