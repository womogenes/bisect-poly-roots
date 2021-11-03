# Polynomial Root Finding Algorithm

## Explanation of the math

This algorithm finds all real roots of single-variable polynomials using this key fact:

>  Real roots of a polynomial fall between either a local minima and maxima (or vice versa), OR they fall between a local minima/maxima and +/- infinity. Furthermore, these intervals are monotonically increasing/decreasing.

This is also a method of [real-root isolation](https://en.wikipedia.org/wiki/Real-root_isolation). Then we look at these intervals, see how many cross zero (which we can do by simply seeing if the endpoints are different signs, true because of the monotonically increasing/decreasing fact), and simply binary search to find the roots inside those intervals.

Proving this is for another time.

## What's inside

`bisect_poly_roots.py` contains the core code. The `roots` method is the one that finds roots. It accepts two arguments:

1. `poly`, a list of numbers, not ending with zero, where `poly[i]` corresponds to the coefficient of `x^i`.
2. `error`, a small number which is used as the error threshold for calculations.



## Testing

1. `test.py` contains the tests. It compares against `numpy.polynomial.polynomial.Polynomial.roots`, which is sometimes wrong.
2. If you find errors, please make a pull request!
