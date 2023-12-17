import logging
import re


def combine_simple_primed_expr(expr: str) -> list:
    """
    Takes a primed expression without brakes, combines &&'d terms.
    Returns a list where each value is ||'d with the others
    :param expr: str
    :return: list
    """
    logging.info(f"Combined Layer {expr}")
    combined = list()

    primes = re.findall(r"[0-9]+", string=expr)
    operators = re.findall(r"&&|\|\|", string=expr)

    current_prime = int(primes[0])

    for i, operator in enumerate(operators):
        if operator == "&&":
            print(f"Multiplying Current Prime {current_prime} by {int(primes[i + 1])}")

            current_prime = current_prime * int(primes[i + 1])
        else:
            combined.append(current_prime)
            print(f"Adding Prime to List: {current_prime}")
            current_prime = int(primes[i + 1])

    combined.append(current_prime)

    logging.info(f"Returning Combined: {combined}")

    return combined
