# Copyright 2012 Canonical Ltd.
# Written by:
#   Zygmunt Krynicki <zygmunt.krynicki@canonical.com>
# See COPYING for license
"""
example 2
=========

Example application of call.bind() to implement argument validation decorator
using python 3 function annotations. The decorator is meant to be simple, not
particularly efficient or one that produces excellent error messages, or one
that illustratively updates the function docstring.
"""

from functools import wraps

from call import PythonCall


def validate(func):
    """
    Check if annotated function arguments validate according to spec
    """
    call = PythonCall(func)

    @wraps(func)
    def decorator(*args, **kwargs):
        parameters = call.bind(args, kwargs)
        for arg_name, validator in func.__annotations__.items():
            if not validator(parameters[arg_name]):
                raise TypeError(
                    "Argument {!r} failed to validate".format(arg_name))
        return call.apply(args, kwargs)
    return decorator


@validate
def example_func(a: lambda a: a > 1, b: lambda b: b.startswith("foo")="foo"):
    print("I was called with {!r} and {!r}".format(a, b))


def main():
    args_variants = [
        (10, "foonction"),
        (10,),
        (0,),
        (5, "quxx"),
    ]
    for args in args_variants:
        print("Calling function with {}".format(args))
        try:
            example_func(*args)
        except TypeError as exc:
            print("TypeError raised: {}".format(exc))


if __name__ == "__main__":
    main()
