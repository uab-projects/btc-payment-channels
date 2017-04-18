"""
Methods to help calculate ECDSA operations

Source:
https://github.com/vbuterin/pybitcointools/blob/master/bitcoin/main.py
"""
# Libraries
from .defaults import DEFAULT_CURVE


# Methods
def inv(a, n):
    """ Extended Euclidean Algorithm """
    if a == 0:
        return 0
    lm, hm = 1, 0
    low, high = a % n, n
    while low > 1:
        r = high//low
        nm, new = hm-lm*r, high-low*r
        lm, low, hm, high = nm, new, lm, low
    return lm % n


def to_jacobian(p):
    o = (p[0], p[1], 1)
    return o


def jacobian_double(p, curve=DEFAULT_CURVE):
    if not p[1]:
        return (0, 0, 0)
    ysq = (p[1] ** 2) % curve.p
    S = (4 * p[0] * ysq) % curve.p
    M = (3 * p[0] ** 2 + curve.a * p[2] ** 4) % curve.p
    nx = (M**2 - 2 * S) % curve.p
    ny = (M * (S - nx) - 8 * ysq ** 2) % curve.p
    nz = (2 * p[1] * p[2]) % curve.p
    return (nx, ny, nz)


def jacobian_add(p, q, curve=DEFAULT_CURVE):
    if not p[1]:
        return q
    if not q[1]:
        return p
    U1 = (p[0] * q[2] ** 2) % curve.p
    U2 = (q[0] * p[2] ** 2) % curve.p
    S1 = (p[1] * q[2] ** 3) % curve.p
    S2 = (q[1] * p[2] ** 3) % curve.p
    if U1 == U2:
        if S1 != S2:
            return (0, 0, 1)
        return jacobian_double(p)
    H = U2 - U1
    R = S2 - S1
    H2 = (H * H) % curve.p
    H3 = (H * H2) % curve.p
    U1H2 = (U1 * H2) % curve.p
    nx = (R ** 2 - H3 - 2 * U1H2) % curve.p
    ny = (R * (U1H2 - nx) - S1 * H3) % curve.p
    nz = (H * p[2] * q[2]) % curve.p
    return (nx, ny, nz)


def from_jacobian(p, curve=DEFAULT_CURVE):
    z = inv(p[2], curve.p)
    return ((p[0] * z**2) % curve.p, (p[1] * z**3) % curve.p)


def jacobian_multiply(a, n, curve=DEFAULT_CURVE):
    if a[1] == 0 or n == 0:
        return (0, 0, 1)
    if n == 1:
        return a
    if n < 0 or n >= curve.n:
        return jacobian_multiply(a, n % curve.n)
    if (n % 2) == 0:
        return jacobian_double(jacobian_multiply(a, n//2))
    if (n % 2) == 1:
        return jacobian_add(jacobian_double(jacobian_multiply(a, n//2)), a)


def fast_multiply(a, n, curve=DEFAULT_CURVE):
    return from_jacobian(jacobian_multiply(to_jacobian(a), n))


def fast_add(a, b, curve=DEFAULT_CURVE):
    return from_jacobian(jacobian_add(to_jacobian(a), to_jacobian(b)))
