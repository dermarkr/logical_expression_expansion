def get_bracketed_terms(expr) -> list:
    """
    Gets a list of bracketed terms which are anded together
    :param expr:
    :return:
    """

    if "(" not in expr:
        return [expr]

    bracketed = []

    i = 0

    while i < len(expr):

        temp_bracketed = ""

        if expr[i] == "(":
            temp_bracketed = inner_bracket(expr[i + 1:])

            i += len(temp_bracketed)

        if temp_bracketed:
            bracketed.append(temp_bracketed)
            temp_bracketed = ""

        i += 1

    return bracketed


def inner_bracket(expr) -> str:
    bracketed = ""
    open_bracket_count = 0

    for char in expr:
        if char == ")":
            if open_bracket_count == 0:
                break
            else:
                open_bracket_count -= 1
        elif char == "(":
            open_bracket_count += 1

        bracketed += char

    return bracketed
