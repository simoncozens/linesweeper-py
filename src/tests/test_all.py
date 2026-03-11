import pytest
import linesweeper


def test_sum_as_string():
    assert linesweeper.sum_as_string(1, 1) == "2"
