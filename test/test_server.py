"""
Test functionality from server module
"""

from server.add import add

def test_add():
    """
    should be 3
    """

    one = 1
    two = 2
    EXPECTED = 3

    actual = add(one, two)

    assert actual == EXPECTED