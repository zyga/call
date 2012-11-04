About call
==========

You call python functions a million times every day.
Did you ever wonder how this actually happens?

Well, I did.

I was interested in writing some decorators for my functions but I quickly
realized I needed to know how passed arguments are bound to function
parameters. This involves positional arguments, keyword arguments, defaults
values, variable argument lists and variable keyword arguments. Python 3 also
brings in the rather exotic keyword-only arguments. All in all it seemed to be
something more than a quick hack if I wanted to do it properly.

I've started with simple functions and some tests and quickly discovered that,
python actually changes quite a lot between versions (and we're still talking
about function calls!) and the call semantics, specially reported errors,
differ from version to version.

So I set out to use the weekend in bed (I'm having a bad flu now) to write pure
python implementation of python function call semantics that correctly mimics
python 3.1, python 3.2 and python 3.3.

Usage
=====

The one thing this library does is allows one to see how a given function
_would_ bind positional and keyword argument to the declared parameters without
actually calling it.

This is useful for constructing decorators that take action on value or type of
each argument and they don't want to reimplement the same (rather lengthy if
you want to check the code) logic. If you're interested in just that then skip
to the 'Applications' section below.

Here's a simple example that illustrates this. We'll start with a simple
function that takes two arguments, including one with a default value. 

``` python
>>> def foo(a, b=2):
>>>     return a, b
```

The call module really exports just one class, PythonCall. You need to
instantiate it with a function or any other callable object.

``` python
>>> from call import PythonCall
>>> c = PythonCall(foo)
```

Then we can call the bind() method to see how python would have reacted to the
very same function call. The method takes two arguments, a list of positional
arguments and a dictionary or any other mapping of keyword arguments. The
return value is a dictionary with argument names and their actual values.

``` python
>>> c.bind([1, 2], {})
>>> {'a': 1, 'b': 2}
>>> c.bind([1], {})
>>> {'a': 1, 'b': 2}
>>> c.bind([1], {'b': 3})
>>> {'a': 1, 'b': 3}
>>> c.bind([], {'a': 4, 'b': 5})
>>> {'a': 4, 'b': 5}
```

Note that any incorrect arguments raise the same exception that python would.

Applications
============

As mentioned earlier this library is intended for developing decorators. That
need to inspect function arguments before calling it. Here's a simple example
of how this can be done to enforce simple type checking

``` python
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
```

Here's another example allows us to define arbitrary validators to any
argument. 

``` python
from functools import wraps

from call import PythonCall

def validate(func):
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
```

It's possible to extend this decorator pattern to implement arbitrary
validation system, multi-method call dispatching and other constructs known
from various languages.

Testing
=======

To really test the code you want to have 'tox' installed (pip install it if you
don't have it already). Tox will read the configuration file and run tests for
all supported versions of python in a correct and fully automatic way.

It is usually hard to get all the required python versions on Ubuntu so if
you're using that I can recommend the 'deadsnakes' ppa that carries all the
versions available. See: https://launchpad.net/~fkrull/+archive/deadsnakes

Patches and issues
==================

Feel free to send patches and to report issues via github
at https://github.com/zyga/call/issues
