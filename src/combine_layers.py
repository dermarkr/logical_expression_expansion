import logging
import re

from src.combine_single_layer import combine_single_layer
from src.expandexpression import ExpandExpression
from src.find_bracketed_term import find_bracket_bounds, find_max_depth
from src.prime_conversion import replace_terms_with_prime

logging.basicConfig()


def get_brackets(expr: str) -> dict:
    logging.info(f"Finding First level brackets in expression `{expr}`")
    i = 0
    brackets = dict()
    while i < len(expr):
        if expr[i] == "(":
            end_index = find_bracket_bounds(expr, i)
            brackets[str(i)] = expr[i + 1:end_index]
            i = end_index

        i += 1

    logging.info(f"Found and returning brackets `{brackets}`")
    return brackets


def replace_brackets_with_index(brackets: dict, expr: str) -> str:
    logging.info(f"Replacing the brackets in expression {expr} with their starting index")
    logging.debug(f"Brackets are `{brackets}`")
    for index, contents in brackets.items():
        expr = expr.replace(f"{contents}", f"#{str(index)}")

    logging.info(f"Returning expression with replaced brackets `{expr}")
    return expr


def combine_layers(expr: str) -> list:
    max_depth = find_max_depth(expr)

    brackets = get_brackets(expr=expr)

    temp_expr = replace_brackets_with_index(brackets, expr)

    values = re.findall(r"#[0-9]+|[0-9]+", temp_expr)
    operators = operators = re.findall(r"&&|\|\|", string=temp_expr)

    print(values)
    print(operators)

    if isinstance(values[0], list):
        current_primes = values[0]
    else:
        current_primes = [int(values[0])]

    expr_value_list = list()

    print(current_primes)
    print(brackets)

    for i, operator in enumerate(operators):
        print(current_primes)
        if operator == "&&":
            if "#" in values[i + 1]:
                print(values[i + 1])
                temp_primes = list()

                bracket_simplified = combine_single_layer(brackets[str(values[i + 1][1:])])

                for v in bracket_simplified:
                    print(v)
                    for prime in current_primes:
                        temp_primes.append(prime * v)

                current_primes = temp_primes

                print(current_primes)

            else:
                temp_primes = list()
                for prime in current_primes:
                    temp_primes.append(prime * int(values[i + 1]))
                current_primes = temp_primes

        else:
            expr_value_list.extend(current_primes)

            if "#" in values[i + 1]:
                bracket_simplified = combine_single_layer(brackets[str(values[i + 1][1:])])

                current_primes = bracket_simplified
            elif isinstance(values[i + 1], list):
                current_primes = values[i + 1]
            else:
                current_primes = [int(values[i + 1])]
            print(f"Current Prime set to {current_primes}")

    expr_value_list.extend(current_primes)

    return expr_value_list


if __name__ == "__main__":
    expr_init = "A && (B && (C || F)) || D && E && (A && B || C)"

    primed_expr, prime_map = replace_terms_with_prime(expr=expr_init)

    print(primed_expr)

    r = combine_layers(primed_expr)

    print(r)

    ee = ExpandExpression(prime_map=prime_map)

    reduced = ee.expand_expr_list(r)

    print(reduced)
