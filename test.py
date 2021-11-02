# Test some random polynomials!
import numpy as np
from numpy.polynomial.polynomial import Polynomial
from random import randrange
import timeit

from bisect_poly_roots import roots, poly_to_str

TEST_ERROR = 0.01
N = 1000


def test_one(deg=100):
    while True:
        poly = np.random.randint(-10, 10, size=(deg + 1))
        if poly[-1] != 0:
            break

    try:
        test_roots = roots(poly)
    except AssertionError as e:
        print(f"AssertionError for {poly}")
        return False

    np_poly = Polynomial(poly)
    real_roots = [x.real for x in np_poly.roots() if abs(x.imag) < 0.0000001]

    if len(test_roots) != len(real_roots):
        print(f"Test failed for {poly}")
        return False

    return True


for _ in range(N):
    if not test_one(3):
        break
