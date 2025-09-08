# Imports functions from the hello module to be tested.
from hello import say_hello, add


# Unit test for the say_hello function.
# Checks if the greeting message is correctly formatted for the given name.
def test_say_hello():
    assert (
        say_hello("Annie")
        == "Hello, Annie, welcome to Data Engineering Systems (IDS 706)!"
    )


# Unit test for the add function.
# Checks if the sum of 2 and 3 is correctly returned as 5.
def test_add():
    assert add(2, 3) == 5
