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


def get_next_prime(lower_bound: int = 10) -> int:
    """
    Takes in an integer and returns the next prime higher than it.

    This is not an efficient function
    :param lower_bound: int

    :return: int
    """

    logging.info(f"Starting to get next prime above value `{lower_bound}`")

    next_prime = lower_bound + 1

    if lower_bound < 1:
        return 1
    elif lower_bound == 1:
        return 2

    while True:

        logging.debug(f"Checking if {next_prime} is prime")

        not_prime = False

        for i in range(2, int(next_prime + 1 / 2)):
            if next_prime % i == 0:
                not_prime = True
                break

        if not not_prime:
            break

        logging.info(f"{next_prime} not prime Checking next")

        next_prime += 1

    logging.info(f"Found next prime is `{next_prime}`")

    return next_prime


def get_terms_in_expr(expr: str) -> list:
    """
    Gets a sorted list of unique terms in the expression
    :param expr: str
    :return: list
    """
    logging.info(f"Getting terms from `{expr}`")
    terms = re.findall(r"[A-Z]+", expr)

    terms = set(terms)
    terms = list(terms)
    terms = sorted(terms)

    logging.info(f"Got terms {terms}")

    return terms


class ExpressionPrimeConversion:
    def __init__(self) -> None:
        """
        Initializes the ExpandExpression Class with the prime map.

        :param None: None

        :return: None
        """
        logging.info(f"Initialising ExpressionPrimeConversion")

        self.prime_map = list()
        self.used_primes = list()

    def get_used_primes(self) -> None:
        """
        Populates the used_primes list module variable with the prime values in the prime_map

        :return: None
        """

        logging.info("Populating used_primes from prime_map")

        self.used_primes = list()

        for _, prime in self.prime_map:
            self.used_primes.append(prime)

        logging.info("Finished populating used_primes list")
        logging.debug(f"used_primes list = `{self.used_primes}`")

    def replace_terms_with_prime(self, expr: str) -> str:
        """
        Goes through the prime_map and replaces all terms in the expression with mapped primes

        :param expr: str

        :return: str
        """

        for term, prime in self.prime_map:
            expr = expr.replace(term, str(prime))

        return expr

    def prime_expression(self, expr: str) -> str:
        """
        Using the expression creates a prime_map, used_prime list and replaces the expression terms with primes

        :param expr: str

        :return: str
        """

        terms = get_terms_in_expr(expr)

        self.make_prime_map(terms)

        self.get_used_primes()

        primed_expr = self.replace_terms_with_prime(expr=expr)

        return primed_expr

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

    def make_prime_map(self, terms: list) -> None:
        """
        Creates a list which maps the terms from the expression to unique prime numbers

        :param terms: list

        :return: None
        """

        logging.info(f"Building prime_map")

        self.prime_map = list()

        next_prime = 10

        for term in terms:
            next_prime = get_next_prime(next_prime)

            logging.debug(f"Adding to prime_map: term = `{term}`, prime = `{next_prime}`")
            self.prime_map.append([term, next_prime])

        logging.info(f"Returning prime_map")
        logging.debug(f"prime_map = `{self.prime_map}`")
