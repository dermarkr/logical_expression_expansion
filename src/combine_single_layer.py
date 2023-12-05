import re


def combine_single_layer(expr: str) -> list:
    combined = list()

    primes = re.findall(r"[0-9]+", string=expr)
    operators = re.findall(r"&&|\|\|", string=expr)

    current_prime = int(primes[0])

    for i, operator in enumerate(operators):
        if operator == "&&":
            current_prime = current_prime * int(primes[i + 1])
        else:
            combined.append(current_prime)
            current_prime = 1

    if not combined:
        combined.append(current_prime)

    return combined
