import logging
import re


def expand_expression(expr: str) -> str:
    """

    :param expr: str
    :return: str
    """

    ee = ExpressionPrimeConversion()

    primed_source_expr = ee.prime_expression(expr=expr)

    reduced_expression = combine_layers(expr=primed_source_expr)

    primed_expanded_expression = ee.fully_expand_expression(expr=reduced_expression)

    expanded_expression = ee.convert_primed_expr_to_chars(primed_expanded_expression)

    return expanded_expression


def combine_simple_primed_expr(expr: str) -> list:
    """
    Takes a primed expression without brackets, combines &&'d terms.
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


def find_bracket_bounds(expr: str, start_index: int) -> int:
    """
    :param expr:
    :param start_index:
    returns end_index as int
    """
    logging.info(f"Finding the end index of the bracket starting at index `{start_index}` in expression `{expr}`")

    open_bracket_count = 0
    end_index = start_index

    for i, char in enumerate(expr[start_index + 1:]):
        if char == ")":
            if open_bracket_count == 0:
                end_index = i + start_index + 1
                break
            else:
                open_bracket_count -= 1
        elif char == "(":
            open_bracket_count += 1

    logging.info(f"Found end index is `{end_index}`")
    return end_index


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
