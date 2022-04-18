def sign(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


def derivative(poly):
    if poly[-1] == 0:
        raise ValueError("Leading coefficient must be nonzero.")

    ans = []
    for i in range(1, len(poly)):
        ans.append(i * poly[i])

    return ans


def poly_to_str(poly):
    result = ""
    for i in range(len(poly)):
        result += f"{poly[i]}*x^{{{i}}} + "
    return result[:-2]


def peval(poly, x):
    """
    poly: list
    x: float
    Evaluate the given polynomial at a given input.
    """
    ans = 0
    for i in range(len(poly)):
        # print(x, i)
        ans += poly[i] * pow(x, i)
    return ans


def roots(poly, error=0.0001):
    """
    poly: list of integers. poly[i] is coefficient of x^i.
    Returns the roots of poly as a list.
    """
    # Remove 0s from the end
    if poly[-1] == 0:
        raise ValueError("Leading coefficient must be nonzero.")

    deg = len(poly) - 1
    if deg == 0:
        raise ValueError("List cannot be empty")

    # Base case of linear
    if deg == 1:
        return [-poly[0] / poly[1]]

    # For non-linear, we use the fancy process
    deriv = derivative(poly)
    d_roots = sorted(roots(deriv, error=error))

    ans = set()

    """
    print()
    print("poly:", poly)
    print("deriv:", deriv)
    print("d_str:", poly_to_str(deriv))
    print("d_roots:", d_roots)
    """

    # What if the derivative has no roots?
    if len(d_roots) == 0:
        assert deg % 2 == 1  # This is probably true
        y_int = peval(poly, 0)

        if abs(y_int) <= error:
            return [0]

        if sign(poly[-1]) == sign(y_int):
            # Look to the left
            hi = 0
            lo = -1
            while sign(peval(poly, lo)) == sign(y_int):
                lo *= 2
        else:
            # Look to the right
            lo = 0
            hi = 1
            while sign(peval(poly, hi)) == sign(y_int):
                hi *= 2

        # Now we have our bounds
        f_lo = peval(poly, lo)
        while hi - lo > error:
            mid = (lo + hi) / 2
            f_mid = peval(poly, mid)
            if abs(f_mid) < error:
                return [mid]
            if sign(f_mid) != sign(f_lo):
                hi = mid
            else:
                lo = mid
                f_lo = peval(poly, lo)

        return [(lo + hi) / 2]

    # Analyze left endpoint
    f_left = peval(poly, d_roots[0])
    if abs(f_left) < error:
        ans.add(d_roots[0])
    else:
        neg_end_behavior = pow(-1, deg % 2) * sign(poly[-1])
        if neg_end_behavior != sign(f_left):
            lo = d_roots[0] - 1
            d = -2
            while sign(peval(poly, lo)) == sign(f_left):
                lo += d
                d *= 2

            hi = d_roots[0]
            while hi - lo > error:
                mid = (lo + hi) / 2
                f_mid = peval(poly, mid)
                if abs(f_mid) < error:
                    break
                if sign(f_mid) != sign(peval(poly, lo)):
                    hi = mid
                else:
                    lo = mid
            ans.add((lo + hi) / 2)

    # Analyze right endpoint (this can probably be made less redundant)
    f_right = peval(poly, d_roots[-1])
    if abs(f_right) < error:
        ans.add(d_roots[-1])
    else:
        pos_end_behavior = sign(poly[-1])
        if pos_end_behavior != sign(f_right):
            hi = d_roots[-1] + 1
            d = 2
            while sign(peval(poly, hi)) == sign(f_right):
                hi += d
                d *= 2

            lo = d_roots[-1]
            while hi - lo > error:
                mid = (lo + hi) / 2
                f_mid = peval(poly, mid)
                if f_mid == 0:
                    break
                if sign(f_mid) != sign(peval(poly, lo)):
                    hi = mid
                else:
                    lo = mid
            ans.add((lo + hi) / 2)

    # Do stuff in between the roots
    for i in range(0, len(d_roots) - 1):
        lo = d_roots[i]
        hi = d_roots[i + 1]

        f_lo = peval(poly, lo)
        f_hi = peval(poly, hi)

        if abs(f_lo) <= error:
            ans.add(lo)
            continue
        if abs(f_hi) <= error:
            ans.add(hi)
            continue

        if sign(f_lo) == sign(f_hi):
            continue

        while hi - lo > error:
            mid = (lo + hi) / 2
            f_mid = peval(poly, mid)

            if abs(f_mid) <= error:
                break

            if sign(f_mid) != sign(f_lo):
                hi = mid
            else:
                lo = mid
                f_lo = peval(poly, lo)

        ans.add((lo + hi) / 2)

    return list(ans)


# Test stuff out
if __name__ == "__main__":
    P = [-6, -4, -1, -8, -1, 4, 7, 9, 5, 9, 6]
    r = roots(P, error=0.00000001)

    print()
    print(poly_to_str(P))
    print(P)
    print(r)
