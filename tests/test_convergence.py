import pytest
from benchmarks import zebra, murder
from quacq.core import  Target_Network
from quacq.acquisition import QuAcq, Solve
import warnings
import sys

# we run the convergence tests multiple times to reduce the flakiness due to the random nature of the learning algorithm and 
# check the convergence of our implimentation

@pytest.mark.parametrize("iteration", range(20))
def test_murder_convergence(iteration):
    murder_puzzle=murder.Model()
    target_network=Target_Network(murder_puzzle.constraints)
    L=QuAcq(murder_puzzle.bais,variables=murder_puzzle.variables,target_network=target_network)
    sol=Solve(L,murder_puzzle.variables)
    
    assert len(sol)>0


@pytest.mark.parametrize("iteration", range(20))
def test_zebra_convergence(iteration):
    zebra_puzzle=zebra.Model()
    target_network=Target_Network(zebra_puzzle.constraints)
    L=QuAcq(zebra_puzzle.bais,variables=zebra_puzzle.variables,target_network=target_network)
    sol=Solve(L,zebra_puzzle.variables)

    assert len(sol)>0


if __name__ == "__main__":
    print("WARNING: These tests may take significant time to complete.")
    response = input("Do you want to continue? (y/n): ").strip().lower()
    if response == "y":
        pytest.main([__file__])
    else:
        print("Tests aborted by user.")
        sys.exit(0)
