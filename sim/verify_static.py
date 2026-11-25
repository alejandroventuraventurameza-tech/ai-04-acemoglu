"""
Symbolic verification of the static block of Acemoglu, Kong & Ozdaglar (2026), Section 3.4.

Checks, with SymPy, every algebraic step used in extra/tutorial-ako.pdf, Part I:
  (1) g = G'  and  g' = -g (1+tau)/(2 tau)  < 0           (Claim 3.2)
  (2) G(tau) ~ sqrt(2 tau / pi) as tau -> 0                (Claim 3.2c)
  (3) multilinear form of f on {0,1}^2                     (Claim 2.1)
  (4) Observation 1: U_eX > 0 and U_e,tauA < 0             (with and without Delta_I)
  (5) IFT: dY/dtau_A = 1 + lambda_I de/dtau_A in (0,1)     (Result 1)
  (6) F(X) > X  <=>  e > e_m(X)                            (Claim 8.1, maintenance effort)
Every check prints OK or raises AssertionError.

Run:  python sim/verify_static.py
"""
import sympy as sp

tau, X, e, tA, lI, lG, I, S2 = sp.symbols("tau X e tau_A lambda_I lambda_G I Sigma2", positive=True)
s2i, eps, DX, DG, DI = sp.symbols("sigma2inv epsilon Delta_X Delta_G Delta_I", positive=True)


def ok(msg):
    print(f"OK  {msg}")


# (1)-(2) The accuracy function -------------------------------------------------
Phi = lambda z: (1 + sp.erf(z / sp.sqrt(2))) / 2
G = 2 * Phi(sp.sqrt(tau)) - 1
g = sp.simplify(sp.diff(G, tau))
g_claim = sp.exp(-tau / 2) / sp.sqrt(2 * sp.pi * tau)
assert sp.simplify(g - g_claim) == 0
ok(f"g(tau) = {g_claim}")

gp = sp.diff(g_claim, tau)
assert sp.simplify(gp + g_claim * (1 + tau) / (2 * tau)) == 0
ok("g'(tau) = -g(tau)(1+tau)/(2 tau)  -> negative for tau > 0 (G strictly concave)")

lead = sp.limit(G / sp.sqrt(tau), tau, 0, "+")
assert sp.simplify(lead - sp.sqrt(2 / sp.pi)) == 0
ok("G(tau)/sqrt(tau) -> sqrt(2/pi) as tau -> 0+")

# (3) Multilinear representation of f -------------------------------------------
f00, f10, f01, f11 = sp.symbols("f00 f10 f01 f11")
dG_, dI_, dX_ = f10 - f00, f01 - f00, f11 - f10 - f01 + f00
rep = lambda a, b: f00 + dG_ * a + dI_ * b + dX_ * a * b
assert all(sp.simplify(rep(a, b) - v) == 0 for (a, b, v) in [(0, 0, f00), (1, 0, f10), (0, 1, f01), (1, 1, f11)])
ok("f(a,b) = f00 + Delta_G a + Delta_I b + Delta_X ab on {0,1}^2")

# (4) Observation 1 ----------------------------------------------------------------
GX = G.subs(tau, X)
Y = s2i + lI * e + tA
GY = G.subs(tau, Y)
cost = eps / (eps + 1) * e ** ((eps + 1) / eps)
for label, U in [("Delta_I = 0 (paper)", DG * GX + DX * GX * GY - cost),
                 ("Delta_I > 0 (our extension)", DG * GX + DI * GY + DX * GX * GY - cost)]:
    Ue = sp.diff(U, e)
    UeX = sp.simplify(sp.diff(U, e, X))
    Uet = sp.simplify(sp.diff(U, e, tA))
    gX, gY, gpY = g_claim.subs(tau, X), g_claim.subs(tau, Y), gp.subs(tau, Y)
    assert sp.simplify(UeX - DX * lI * gX * gY) == 0
    A = DX * GX + (DI if "extension" in label else 0)
    assert sp.simplify(Uet - A * lI * gpY) == 0
    ok(f"Observation 1 [{label}]: U_eX = Delta_X lambda_I g(X) g(Y) > 0;  U_e,tauA = A(X) lambda_I g'(Y) < 0")

# (5) Partial crowding-out -----------------------------------------------------------
a, b = sp.symbols("a b", positive=True)  # a = (1/eps) e^{1/eps - 1},  b = Delta_X G(X) lambda_I^2 |g'(Y)|
de_dtau = -(b / lI) / (a + b)  # from the IFT, eq. (detau) in the tutorial
dY_dtau = sp.simplify(1 + lI * de_dtau)
assert sp.simplify(dY_dtau - a / (a + b)) == 0
ok("dY/dtau_A = a/(a+b) in (0,1): crowding-out is partial at fixed X")

# (6) Maintenance effort ---------------------------------------------------------------
z = X + lG * I * e
F = 1 / (S2 + 1 / z)
e_m = S2 * X**2 / (lG * I * (1 - S2 * X))
# F(X) - X has the sign of (e - e_m) when 0 < X < 1/Sigma^2: check the exact factorisation
target = lG * I * (1 - S2 * X) * (e - e_m) / (1 + S2 * z)
assert sp.simplify((F - X) - target) == 0
ok("F(X) - X = lambda_G I (1 - Sigma^2 X)(e - e_m(X)) / (1 + Sigma^2 z)  ->  F(X) > X  <=>  e > e_m(X)")
print("\nAll static-block checks passed.")
