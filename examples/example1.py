# Copyright 2012 Canonical Ltd.
# Written by:
#   Zygmunt Krynicki <zygmunt.krynicki@canonical.com>
# See COPYING for license
"""
example 1
=========

Example application of call.bind() to implement type checking decorator using
python 3 function annotations. The decorator is meant to be simple, not
particularly efficient or one that produces excellent error messages, or one
that illustratively updates the function docstring.
"""

from functools import wraps

from call import PythonCall


def check_types(func):
    """
    Check if annotated function arguments are of the correct type
    """
    call = PythonCall(func)

    @wraps(func)
    def decorator(*args, **kwargs):
        parameters = call.bind(args, kwargs)
        for arg_name, expected_type in func.__annotations__.items():
            if not isinstance(parameters[arg_name], expected_type):
                raise TypeError("{} must be a {}".format(
                    arg_name, expected_type))
        return call.apply(args, kwargs)
    return decorator


@check_types
def example_func(a: int, b: str="text"):
    print("I was called with {!r} and {!r}".format(a, b))


def main():
    args_variants = [
        (1, "other text"),
        (1,),
        ("text", "text"),
        (1, 1),
    ]
    for args in args_variants:
        print("Calling function with {}".format(args))
        try:
            example_func(*args)
        except TypeError as exc:
            print("TypeError raised: {}".format(exc))


if __name__ == "__main__":
    main()
