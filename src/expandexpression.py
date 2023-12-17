import logging
import re


def expr_list_to_str(expr_list: list) -> str:
    """
    Converts a list of terms to an ||'d expression
    No value conversions done
    :param expr_list: list
    :return: str
    """
    logging.info(f"Converting expression list: `{expr_list}` to ||'d expression")
    expr = str()

    for value in expr_list:
        expr += f"{value} || "

    if expr:
        expr = expr[:-4]

    logging.info(f"Returning ||'d expression: `{expr}`")

    return expr


class ExpandExpression:
    def __init__(self, prime_map: list) -> None:
        """
        Initializes the ExpandExpression Class with the prime map.
        :param prime_map: list
        :return: None
        """
        logging.info(f"Initialising ExapandExpression with prime_map `{prime_map}`")
        self.prime_map = prime_map

        self.used_primes = list()

        for _, prime in prime_map:
            self.used_primes.append(prime)

        logging.debug(f"ExpandExpressions initialed with: prime_map `{self.prime_map}` "
                      f"and used_primes `{self.used_primes}`")

    def get_component_primes(self, value: int) -> list:
        """
        Gets the primes (from prime list) which the provided value is a product of

        :param value: int
        :return: list
        """

        logging.info(f"Getting list of component primes for value: `{value}`")

        component_primes = list()

        for prime in self.used_primes:
            if value % prime == 0:
                component_primes.append(prime)

        if not component_primes:
            logging.warning(f"The provided Value: `{value}` is not a "
                            f"product of primes. Returning an empty list.")

        logging.info(f"Retuning list of component primes: `{component_primes}`")

        return component_primes

    def get_mapped_term(self, prime: int) -> str:
        """
        Gets the term mapped to provided prime from prime_map
        :param prime: int
        :return: str
        """

        logging.info(f"Getting term mapped to prime: `{prime}`")
        logging.debug(f"Prime Map: `{self.prime_map}`")

        for char, mapped_prime in self.prime_map:
            if mapped_prime == prime:
                logging.info(f"Found that prime `{prime}` in mapped to `{char}`")
                return char

        logging.warning(f"Value `{prime}` is not mapped to a character. Returning an empty string.")
        return str()

    def expand_value_to_components(self, value: int) -> str:
        """
        Expands a value to and &&'d expression of its component primes
        :param value: int
        :return: str
        """
        logging.info(f"Expanding value `{value}` to &&'d expression")
        component_primes = self.get_component_primes(value=value)

        expr = str()

        for component_prime in component_primes:
            expr += f"{str(component_prime)} && "

        if expr:
            expr = expr[:-4]

        logging.info(f"Returning &&'d expression `{expr}`")
        return expr

    def convert_primed_expr_to_chars(self, expr: str) -> str:
        """
        Converts all primes in an expression to their mapped terms

        :param expr: str

        :return: str
        """

        logging.info(f"Converting primes in expr `{expr}` to mapped terms")

        component_primes = re.findall(r"[0-9]+", expr)

        logging.debug(f"Values found in expr are `{component_primes}`")

        expr = f" {expr} "

        for component_prime in component_primes:
            char = self.get_mapped_term(prime=int(component_prime))
            if not char:
                logging.warning(f"No Mapped character found for `{component_prime}`. Skipping it.")
                continue
            expr = expr.replace(f" {str(component_prime)} ", f" {char} ")

        expr = expr[1:-1]

        logging.info(f"Returning converted expression `{expr}`")

        return expr

    def fully_expand_expression(self, expr: str) -> str:
        """
        Fully expands an expression with values made up of component primes.
        Does NOT replace the primes with their mapped terms
        :param expr: str

        :return: str
        """
        logging.info(f"Expanding expression `{expr}`")
        component_values = re.findall(r"[0-9]+", expr)

        expr = f" {expr} "

        for value in component_values:
            expanded_primes = self.expand_value_to_components(value=int(value))

            print(expanded_primes)
            print(value)

            logging.debug(f"Replacing value `{value}` with expanded_primes `{expanded_primes}`")
            expr = expr.replace(f" {str(value)} ", f" {expanded_primes} ")

        expr = expr[1:-1]

        logging.info(f"Returning expanded expression `{expr}`")

        return expr
