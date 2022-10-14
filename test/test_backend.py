"""
Test functionality from backend module
"""

from backend import TEST_EXAMPLE

def test_add():
    """
    should be 3
    """
    # Arrange
    one = 1
    two = 2
    EXPECTED = 3

    # Act
    actual = TEST_EXAMPLE.add(one, two)

    # Assert
    assert actual == EXPECTED, "Hello world"