import logging
import re
from copy import copy

from src.combine_single_layer import combine_single_layer
from src.find_bracketed_term import find_bracket_bounds, find_max_depth

logging.basicConfig()


def combine_layers(expr: str) -> list:
    max_depth = find_max_depth(expr)

    if max_depth == 0:
        return combine_single_layer(expr)
    # elif max_depth > 1:
    #     expr = combine_layers(expr)

    brackets = list()
    temp_expr = copy(expr)

    i = 0

    while i < len(expr):
        if expr[i] == "(":
            end_index = find_bracket_bounds(expr, i)
            brackets.append((i, expr[i + 1:end_index]))
            temp_expr = temp_expr.replace(f"{expr[i:end_index + 1]}", f"#{str(i)}")

        i += 1

    brackets_simplified = dict()

    for bracket in brackets:
        simplified = combine_single_layer(bracket[1])
        print(bracket, simplified)
        brackets_simplified[str(bracket[0])] = simplified

    values = re.findall(r"#[0-9]+|[0-9]+", temp_expr)
    operators = operators = re.findall(r"&&|\|\|", string=temp_expr)

    print(values)
    print(operators)

    if isinstance(values[0], list):
        current_primes = values[0]
    else:
        current_primes = [int(values[0])]

    new_expr = list()

    print(current_primes)
    print(brackets_simplified)

    for i, operator in enumerate(operators):
        print(current_primes)
        if operator == "&&":
            if "#" in values[i + 1]:
                print(values[i + 1])
                temp_primes = list()

                for v in brackets_simplified[str(values[i + 1][1:])]:
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
            new_expr.extend(current_primes)

            if "#" in values[i + 1]:
                current_primes = brackets_simplified[str(values[i + 1][1:])]
            elif isinstance(values[i + 1], list):
                current_primes = values[i + 1]
            else:
                current_primes = [int(values[i + 1])]
            print(f"Current Prime set to {current_primes}")

    new_expr.extend(current_primes)

    return new_expr


if __name__ == "__main__":
    expres = "11 && (13 || 17) || 23 && 29 && (11 && 13 || 17)"

    r = combine_layers(expres)

    print(r)
