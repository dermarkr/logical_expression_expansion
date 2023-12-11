import logging
import re


def expr_list_to_str(expr_list: list) -> str:
    expr = str()

    for value in expr_list:
        expr += f"{value} || "

    if expr:
        expr = expr[:-4]

    return expr


class ExpandExpression:
    def __init__(self, prime_map: list):
        self.prime_map = prime_map

        self.used_primes = list()

        for _, prime in prime_map:
            self.used_primes.append(prime)

    def get_component_primes(self, value: int) -> list:
        """
        Gets the primes (from prime list) which the provided value is a product of

        :param value:
        :return component_primes:
        """

        component_primes = list()

        for prime in self.used_primes:
            if value % prime == 0:
                component_primes.append(prime)

        primes_product = 1

        if not component_primes:
            logging.warning(f"The provided Value: `{value}` is not a "
                            f"product of primes. Returning an empty list.")

        return component_primes

    def get_mapped_character(self, prime: int) -> str:

        for char, mapped_prime in self.prime_map:
            if mapped_prime == prime:
                logging.info(f"Found that prime `{prime}` in mapped to `{char}`")
                return char

        logging.warning(f"Value `{prime}` is not mapped to a character. Returning an empty string.")
        return str()

    def expand_value_to_components(self, value) -> str:
        component_primes = self.get_component_primes(value=value)

        expr = str()

        for component_prime in component_primes:
            expr += f"{str(component_prime)} && "

        if expr:
            expr = expr[:-4]

        return expr

    def convert_primed_expr_to_chars(self, expr: str) -> str:

        component_primes = re.findall(r"[0-9]+", expr)

        expr = f" {expr} "

        for component_prime in component_primes:
            char = self.get_mapped_character(prime=int(component_prime))
            if not char:
                logging.warning(f"No Mapped character found for `{component_prime}`. Skipping it.")
                continue
            expr = expr.replace(f" {str(component_prime)} ", f" {char} ")

        expr = expr[1:-1]

        return expr

    def fully_expand_expression(self, expr: str):
        component_values = re.findall(r"[0-9]+", expr)

        expr = f" {expr} "

        for value in component_values:
            expanded_primes = self.expand_value_to_components(value=int(value))

            print(expanded_primes)
            print(value)

            expr = expr.replace(f" {str(value)} ", f" {expanded_primes} ")

        expr = expr[1:-1]

        return expr
