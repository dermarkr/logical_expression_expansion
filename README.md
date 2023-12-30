# logical_expression_expansion

Takes a logical expression which has nested brackets and expands it out so all terms are outside brackets.

The input logical expression should have spaces between symbols and operates (eg "A && B")

A more complex example is "A && (B || C) || A && (E || F && (I || J)) && (G || H)"

Does not support NOT terms.

## Usage

Used by importing expand_expression and passing the expression to be expanded into it.

expand_expression returns the expanded as a string

```python
from expandexpression import expand_expression

original_expr = "A && (B || C)"

expanded_expr = expand_expression(original_expr)

print(expanded_expr)
# Should output "A && B || A && C
```

### Required Expression Formatting Rules

- No leading space on expression
- Space leading and tailing '&&' and '||'
- Space leading '('
- No Space trailing '('
- No space leading ')'
- Space trailing ')'
- Expression identifiers most be letters only but can be multiple characters
    - EG:
        - Allowed = 'A', 'AB', 'first'
        - Not Allowed = '1', 'A1'

 