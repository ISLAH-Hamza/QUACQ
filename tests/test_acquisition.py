import pytest
from quacq.acquisition import *
from quacq.core import Variable, Relation, Constraints, Target_Network




def test_solve():
    # Create variables
    x = Variable("x", [0, 10])
    y = Variable("y", [0, 10])

    # Create constraints: x == 5, y == 7, x < y
    c1 = Constraints([x], Relation("==val", 1, True, 5))
    c2 = Constraints([y], Relation("==val", 1, True, 7))
    c3 = Constraints([x, y], Relation("<", 2, True))

    # L is a list of conjunctions (sets of constraints)
    L = [{c1, c2, c3}]
    vars = [x, y]

    sol = Solve(L, vars)
    assert sol is not None
    assert sol["x"] == 5
    assert sol["y"] == 7
    assert sol["x"] < sol["y"]

def test_generate_example():
    x = Variable("x", [0, 10])
    y = Variable("y", [0, 10])
    c1 = Constraints([x], Relation("==val", 1, True, 5))
    c2 = Constraints([y], Relation("==val", 1, True, 7))
    B = {c1, c2}
    L = []
    vars = [x, y]
    example = GenerateExample(B, L, vars)
    assert example is not None
    assert set(example.keys()) == {"x", "y"}
    # Should not satisfy all constraints in B
    assert not all(c.check(example) for c in B)

def test_findScope():
    x = Variable("x", [0, 10])
    y = Variable("y", [0, 10])
    c1 = Constraints([x], Relation("==val", 1, True, 5))
    c2 = Constraints([y], Relation("==val", 1, True, 7))
    B = {c1, c2}
    vars = [x, y]
    example = {"x": 3, "y": 8}
    target_network = Target_Network(constraints=B)
    scope = findScope(example, set(), {"x", "y"}, B, target_network)
    assert isinstance(scope, set)
    assert scope.issubset({"x", "y"})

def test_findC():
    x = Variable("x", [0, 10])
    y = Variable("y", [0, 10])
    c1 = Constraints([x], Relation("==val", 1, True, 5))
    c2 = Constraints([y], Relation("==val", 1, True, 7))
    B = {c1, c2}
    vars = [x, y]
    example = {"x": 3, "y": 8}
    target_network = Target_Network(constraints=B)
    L = []
    findC(example, {"x", "y"}, L, B, target_network, vars)
    assert isinstance(L, list)

def test_learn():
    x = Variable("x", [0, 10])
    y = Variable("y", [0, 10])
    c1 = Constraints([x], Relation("==val", 1, True, 5))
    c2 = Constraints([y], Relation("==val", 1, True, 7))
    B = {c1, c2}
    vars = [x, y]
    target_network = Target_Network(constraints=B)
    L = QuAcq(B.copy(), vars, target_network)
    assert isinstance(L, list)




if __name__=="__main__":
    pytest.main([__file__])