import solve
import pytest
import numpy

class TestSolve:
    def test_solve(self):
        assert(type(solve.solve([[3,-2,-6],[5,1,3]]))==type(numpy.array([0., 3.])))
