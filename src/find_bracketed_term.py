import logging


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
