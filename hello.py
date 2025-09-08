# This module includes a greeting function and a basic addition function.


def say_hello(name: str) -> str:
    """Return a greeting message to students in the IDS class."""
    # Format and return a personalized greeting message for the given name.
    return f"Hello, {name}, welcome to Data Engineering Systems (IDS 706)!"


def add(a: int, b: int) -> int:
    """Return the sum of two numbers."""
    # Return the result of adding two integers.
    return a + b
