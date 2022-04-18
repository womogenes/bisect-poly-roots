# Test some random polynomials!
import numpy as np
from numpy.polynomial.polynomial import Polynomial
from random import randrange
import time
from tqdm import tqdm

from bisect_poly_roots import roots, poly_to_str

TEST_ERROR = 0.01
N = 1000
DEGREE = 10


def test_one(deg=100):
    while True:
        poly = list(np.random.randint(-10, 10, size=(deg + 1)))
        if poly[-1] != 0:
            break

    try:
        test_roots = roots(poly, error=0.00000001)
    except AssertionError as e:
        print(f"AssertionError for {poly}")
        return False

    np_poly = Polynomial(poly)
    real_roots = list(
        set([x.real for x in np_poly.roots() if abs(x.imag) < 0.0000001]))

    if len(test_roots) != len(real_roots):
        print(f"Test failed for {poly}")
        print("Test roots:", test_roots)
        print("Real roots:", real_roots)
        return False

    test_roots.sort()
    real_roots.sort()

    for i in range(len(test_roots)):
        if abs(real_roots[i] - test_roots[i]) > TEST_ERROR:
            print(f"Test failed for {poly}")
            print("Test roots:", test_roots)
            print("Real roots:", real_roots)
            return False

    return True


start_time = time.time()
passed = True

print(f"Running {N} tests")
for _ in tqdm(range(N)):
    if not test_one(DEGREE):
        passed = False
        break

if passed:
    elapsed = time.time() - start_time
    print(
        f"{N} tests passed in {round(elapsed, 2)} seconds (average of {round(elapsed / N, 2)} sec per run).")
