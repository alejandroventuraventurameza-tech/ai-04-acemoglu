"""
Acemoglu, Kong & Ozdaglar (2026), "AI, Human Cognition and Knowledge Collapse".
Numerical implementation of the model in Section 3 (author version dated 2026-05-05).
Effort cost eps/(eps+1) e^{(eps+1)/eps}, eps = Frisch elasticity (Feb. NBER version: alpha = 1 + 1/eps).

Notation follows the paper:
    G(tau) = P(|Z| <= 1),  Z ~ N(0, 1/tau)      -> accuracy as a function of precision
    g(tau) = G'(tau)
    X      = public precision (stock of general knowledge)
    Y      = sigma^{-2} + lambda_I * e + tau_A     (idiosyncratic precision, eq. 4)
    e(X, tau_A) solves the FOC  lambda_I * A(X) * g(Y) = e^{1/eps}
        with A(X) = Delta_I + Delta_X * G(X)   (Delta_I = 0 is the paper's Assumption 1;
                                                 Delta_I > 0 is OUR extension)
    F(X) = [Sigma^2 + (X + lambda_G * I * e(X, tau_A))^{-1}]^{-1}   (Proposition 1)
    e_m(X) = Sigma^2 X^2 / (lambda_G I (1 - Sigma^2 X))  -- "maintenance effort":
             F(X) > X  <=>  e(X, tau_A) > e_m(X)   for 0 < X < Sigma^{-2}.
"""
import math
import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq

_SQ2PI = math.sqrt(2.0 * math.pi)


def _G(t):  # scalar, fast
    return math.erf(math.sqrt(t / 2.0)) if t > 0 else 0.0


def _g(t):  # scalar, fast
    return math.exp(-t / 2.0) / (_SQ2PI * math.sqrt(t))

BASE = dict(
    s2i=1.0,     # sigma^{-2}: prior precision of the idiosyncratic state (Assumption 2: >= sqrt(2)-1)
    lI=4.0,      # lambda_I: private-learning technology
    lG=1.0,      # lambda_G: public-learning technology
    I=1e4,       # aggregation capacity (island size)
    S2=0.1,      # Sigma^2: variance of the innovation to the common state
    eps=2.0,     # Frisch elasticity of effort
    DG=0.2,      # Delta_G
    DI=0.0,      # Delta_I  (paper: 0)
    DX=0.8,      # Delta_X  (Delta_G + Delta_I + Delta_X = 1)
)


def G(t):
    t = np.asarray(t, float)
    return 2.0 * norm.cdf(np.sqrt(t)) - 1.0


def g(t):
    t = np.asarray(t, float)
    return norm.pdf(np.sqrt(t)) / np.sqrt(t)


def e_br(X, tA, p):
    """Best-response effort: unique root of the FOC (0 if the marginal benefit is 0)."""
    A = p["DI"] + p["DX"] * _G(X)
    if A <= 0.0:
        return 0.0
    lI, s2i, inv = p["lI"], p["s2i"], 1.0 / p["eps"]
    foc = lambda e: lI * A * _g(s2i + lI * e + tA) - e ** inv
    hi = 1.0
    while foc(hi) > 0:
        hi *= 2.0
    return brentq(foc, 0.0, hi, xtol=1e-300, rtol=1e-14)


def e_m(X, p):
    X = np.asarray(X, float)
    return p["S2"] * X**2 / (p["lG"] * p["I"] * (1.0 - p["S2"] * X))


def F(X, tA, p):
    z = X + p["lG"] * p["I"] * e_br(X, tA, p)
    return 0.0 if z == 0.0 else 1.0 / (p["S2"] + 1.0 / z)


def gap(X, tA, p):
    return e_br(X, tA, p) - float(e_m(X, p))


def steady_states(tA, p, n=400, xmin=1e-10):
    """Positive steady states = sign changes of e(X) - e_m(X) on (0, Sigma^{-2})."""
    xs = np.geomspace(xmin, (1.0 / p["S2"]) * (1 - 1e-9), n)
    v = np.array([gap(x, tA, p) for x in xs])
    roots = []
    for i in range(n - 1):
        if v[i] * v[i + 1] < 0:
            roots.append(brentq(lambda x: gap(x, tA, p), xs[i], xs[i + 1]))
    return roots


def welfare(X, tA, p):
    """Steady-state expected utility net of f(0,0) (Section 4.1), with our Delta_I term."""
    e = e_br(X, tA, p)
    Y = p["s2i"] + p["lI"] * e + tA
    GX, GY = _G(X), _G(Y)
    return p["DG"] * GX + p["DI"] * GY + p["DX"] * GX * GY - p["eps"] / (p["eps"] + 1) * e ** ((p["eps"] + 1) / p["eps"])
