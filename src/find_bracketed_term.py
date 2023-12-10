import logging


def find_bracket_bounds(expr: str, start_index: int) -> int:
    """
    :param expr:
    :param start_index:
    returns end_index as int
    """
    logging.info(f"Finding the ")

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

    return end_index


def find_max_depth(expr: str) -> int:
    max_depth = 0

    open_bracket_count = 0

    for i, char in enumerate(expr):
        if char == ")":
            if open_bracket_count > 0:
                open_bracket_count -= 1
        elif char == "(":
            open_bracket_count += 1

            if open_bracket_count > max_depth:
                max_depth = open_bracket_count

    return max_depth
