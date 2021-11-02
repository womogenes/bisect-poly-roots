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
        result += f"{poly[i]}*x^{i} + "
    return result[:-2]


def peval(poly, x):
    """
    poly: list
    x: float
    Evaluate the given polynomial at a given input.
    """
    ans = 0
    for i in range(len(poly)):
        #print(x, i)
        ans += poly[i] * pow(x, i)
    return ans


def roots(poly, error=0.0001):
    """
    poly: list of integers. poly[i] is coefficient of x^i.
    Find the roots of poly.
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
    d_roots = roots(deriv, error=error)

    ans = []

    """
    print("poly:", poly)
    print("deriv:", deriv)
    print("d_roots:", d_roots)
    print()
    """

    # What if the derivative has no roots?
    if len(d_roots) == 0:
        assert deg % 2 == 1  # This is probably true
        y_int = peval(poly, 0)

        if abs(y_int) <= error:
            return [y_int]

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
        while hi - lo > error:
            mid = (lo + hi) / 2
            f_mid = peval(poly, mid)
            if abs(f_mid) < error:
                return [f_mid]
            if sign(f_mid) != sign(peval(poly, lo)):
                hi = mid
            else:
                lo = mid

        return [(lo + hi) / 2]

    # Analyze left endpoint
    f_left = peval(poly, d_roots[0])

    if abs(f_left) < error:
        ans.append(f_left)
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
            ans.append((lo + hi) / 2)

    # Analyize right endpoint (this can probably be made less redundant)
    f_right = peval(poly, d_roots[-1])
    if f_right == 0:
        ans.append(f_right)
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
            ans.append((lo + hi) / 2)

    # Do stuff in between the roots
    for i in range(0, len(d_roots) - 1):
        lo = d_roots[i]
        hi = d_roots[i + 1]

        if abs(lo) <= error:
            ans.append(lo)
            continue
        if abs(hi) <= error:
            ans.append(hi)
            continue

        f_lo = peval(poly, lo)
        f_hi = peval(poly, hi)

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

        ans.append((lo + hi) / 2)

    return ans


# Test stuff out
if __name__ == "__main__":
    P = [1, 1, 3, 3]
    r = roots(P, error=0.00000001)

    print(poly_to_str(P))
    print(r)
