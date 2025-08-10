import pytest
from QUACQ.core import *



def test_variable_bounds_only_ok():
    v = Variable("x", [0, 10])
    assert v.domain == [0, 10]




def test_variable_bounds_validation():
    with pytest.raises(AssertionError):
        Variable("x", [0])                   # not 2 elements
    with pytest.raises(AssertionError):
        Variable("x", ["a", 2])              # non-numeric
    with pytest.raises(AssertionError):
        Variable("x", [5, 1])                # lo > hi
    with pytest.raises(AssertionError):
        Variable(123, [0, 1])                # name must be str
    with pytest.raises(AssertionError):
        Variable("x", { "lo": 0, "hi": 1 })  # not list/tuple


def test_relation_equality_hash_and_str():
    r1 = Relation("==", 2, None)
    r2 = Relation("==", 2, False, None)
    # equality ignores arity/directness, compares operator+parameter only
    assert r1 == r2

    r3 = Relation("||==", 2, False,2)
    r4 = Relation("||==", 2, False,4)
    r5 = Relation("||==", 2, False,4)

    assert r3 != r4
    assert r4 == r5
    assert len({r3, r4, r5}) == 2



if __name__ == "__main__":
    pytest.main([__file__])