import logging
import re

logging.basicConfig(level=logging.DEBUG)


def replace_terms_with_prime(expr: str) -> str:
    """

    :param expr:
    :return:
    """

    terms = get_terms_in_expr(expr)

    prime_map = make_prime_map(terms)

    for term, prime in prime_map:
        expr = expr.replace(term, str(prime))

    return expr


def get_terms_in_expr(expr) -> list:
    logging.info(f"Getting terms from `{expr}`")
    terms = re.findall(r"[A-Z]+", expr)

    terms = set(terms)
    terms = list(terms)
    terms = sorted(terms)

    logging.info(f"Got terms {terms}")

    return terms


def make_prime_map(terms) -> list:
    """

    :param terms:
    :return:
    """

    prime_map = list()

    next_prime = 10

    for term in terms:
        next_prime = get_next_prime(next_prime)

        prime_map.append([term, next_prime])

    return prime_map


def get_next_prime(lower_bound: int = 10) -> int:
    """
    Takes in an integer and returns the next prime higher than it.
    
    This is not an efficient function
    :param lower_bound:
    :return:
    """

    next_prime = lower_bound + 1

    if lower_bound < 1:
        return 1
    elif lower_bound == 1:
        return 2

    while True:

        logging.info(f"Checking if {next_prime} in prime")

        not_prime = False

        for i in range(2, int(next_prime + 1 / 2)):
            if next_prime % i == 0:
                not_prime = True
                break

        if not not_prime:
            break

        logging.info(f"{next_prime} not prime Checking next")

        next_prime += 1

    return next_prime
