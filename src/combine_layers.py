import logging
import re

from src.combine_single_layer import combine_simple_primed_expr
from src.expandexpression import ExpandExpression, expr_list_to_str
from src.find_bracketed_term import find_bracket_bounds
from src.prime_conversion import replace_terms_with_prime


def get_brackets(expr: str) -> dict:
    """
    Gets the first level of brackets and returns the contents in a dict with the start index as the key
    :param expr:
    :return: dict
    """
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
    """
    Replaces bracketed terms in an expression with their starting index prefixed with a '#'
    :param brackets: dict
    :param expr: str

    :return: str
    """
    logging.info(f"Replacing the brackets in expression {expr} with their starting index")
    logging.debug(f"Brackets are `{brackets}`")
    for index, contents in brackets.items():
        expr = expr.replace(f"{contents}", f"#{str(index)}")

    logging.info(f"Returning expression with replaced brackets `{expr}")
    return expr


def combine_layers(expr: str) -> str:
    logging.info(f"Combining layers for expression `{expr}`")

    brackets = get_brackets(expr=expr)

    temp_expr = replace_brackets_with_index(brackets, expr)

    for index in brackets.keys():
        if "(" in brackets[index]:
            brackets[index] = combine_layers(expr=brackets[index])

    values = re.findall(r"#[0-9]+|[0-9]+", temp_expr)
    operators = operators = re.findall(r"&&|\|\|", string=temp_expr)

    logging.info(f"Values in temporary expression {values}")

    if isinstance(values[0], list):
        current_primes = values[0]
    elif "#" in values[0]:
        index = values[0][1:]
        current_primes = combine_simple_primed_expr(brackets[str(index)])
    else:
        current_primes = [int(values[0])]

    expr_value_list = list()

    for i, operator in enumerate(operators):
        print(current_primes)
        if operator == "&&":
            if "#" in values[i + 1]:
                print(values[i + 1])
                temp_primes = list()

                bracket_simplified = combine_simple_primed_expr(brackets[str(values[i + 1][1:])])

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
                bracket_simplified = combine_simple_primed_expr(brackets[str(values[i + 1][1:])])

                current_primes = bracket_simplified
            elif isinstance(values[i + 1], list):
                current_primes = values[i + 1]
            else:
                current_primes = [int(values[i + 1])]
            print(f"Current Prime set to {current_primes}")

    expr_value_list.extend(current_primes)

    ret_expr = expr_list_to_str(expr_list=expr_value_list)

    return ret_expr


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

    # expr_init = "A && (B && (C || F)) || D && E && (A && B || C)"
    expr_init = "((A || B) && (C || D))"


    primed_expr, prime_map = replace_terms_with_prime(expr=expr_init)

    print(primed_expr)

    r = combine_layers(primed_expr)

    print(r)

    ee = ExpandExpression(prime_map=prime_map)

    reduced = ee.fully_expand_expression(r)

    print(reduced)

    final = ee.convert_primed_expr_to_chars(reduced)

    print(final)
