import logging
import re


def combine_single_layer(expr: str) -> list:
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

    logging.info(f"Returing Combined: {combined}")

    return combined
