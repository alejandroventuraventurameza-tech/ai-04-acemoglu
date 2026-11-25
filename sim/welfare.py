"""
Block 2 — welfare, the week's trap, and our extension Delta_I > 0.
Run from the repository root:  python sim/welfare.py   -> figures/fig4..fig7 + printed table

fig4  steady-state welfare U+(tau_A) in the paper's model: hump (eps<4) and hump + cliff (eps>4)
fig5  extension Delta_I > 0: the tau_A -> infinity limit becomes Delta_I; numerical examples retain an interior maximum
fig6  extension Delta_I > 0: F(0) > 0, so complete knowledge collapse is impossible
fig7  transition after an AI shock: short-run gain vs long-run loss, and the role of discounting
fig8  planner benchmark: with the learning externality internalised, welfare is monotone in tau_A
"""
import os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(__file__))
from model import BASE, G, g, e_br, e_m, F, steady_states, welfare

OUT = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
C = ["#1f4e79", "#c55a11", "#548235", "#7030a0", "#bf9000"]


def high_state(tA, p):
    r = steady_states(tA, p, n=700)
    return max(r) if r else 0.0


def U_plus(tA, p):
    X = high_state(tA, p)
    return welfare(X, tA, p) if X > 0 else welfare(0.0, tA, p)


taus = np.concatenate([np.linspace(0, 3, 61), np.linspace(3.25, 12, 36)])

# ---------------------------------------------------------------- fig4
fig, ax = plt.subplots(1, 2, figsize=(9, 3.4))
summary = {}
for k, eps in enumerate([2.0, 6.0]):
    p = dict(BASE, eps=eps)
    W = np.array([U_plus(t, p) for t in taus])
    i = int(np.argmax(W))
    summary[eps] = (taus[i], W[i], W[0])
    ax[k].plot(taus, W, color=C[0])
    ax[k].axvline(taus[i], color="grey", ls=":", lw=1)
    ax[k].annotate(r"$\tau_A^\star$", (taus[i], W[i]), textcoords="offset points", xytext=(4, 4))
    if eps > 4:
        pos = np.where(W > 1e-9)[0]
        tc = taus[pos[-1] + 1] if pos[-1] + 1 < len(taus) else np.nan
        summary[eps] += (tc,)
        ax[k].axvline(tc, color=C[1], ls="--", lw=1)
        ax[k].annotate(r"$\tau_A^c$: cliff", (tc, W.max() * 0.5), textcoords="offset points", xytext=(4, 0), color=C[1])
    ax[k].set_title(rf"$\varepsilon={eps:g}$" + (" (unique steady state)" if eps < 4 else " (collapse regime)"))
    ax[k].set_xlabel(r"agentic AI accuracy $\tau_A$")
ax[0].set_ylabel(r"steady-state welfare $\bar U^+$")
fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig4_welfare_hump.pdf")); plt.close(fig)

# ---------------------------------------------------------------- fig5
DIs = [0.0, 0.05, 0.15, 0.3, 0.5]
fig, ax = plt.subplots(1, 2, figsize=(9, 3.4), sharey=True)
ext = {}
for k, eps in enumerate([2.0, 6.0]):
    for j, DI in enumerate(DIs):
        p = dict(BASE, eps=eps, DI=DI, DX=1 - BASE["DG"] - DI)
        W = np.array([U_plus(t, p) for t in taus])
        i = int(np.argmax(W))
        ext[(eps, DI)] = (taus[i], W[i], W[-1])
        ax[k].plot(taus, W, color=C[j], label=rf"$\Delta_I={DI:g}$")
        if DI > 0:
            ax[k].axhline(DI, color=C[j], ls=":", lw=0.8)
    ax[k].set_title(rf"$\varepsilon={eps:g}$, $\Delta_G={BASE['DG']:g}$, $\Delta_X=0.8-\Delta_I$")
    ax[k].set_xlabel(r"$\tau_A$")
ax[0].set_ylabel(r"$\bar U^+$ (dotted: limit $\Delta_I$)")
ax[1].legend(fontsize=7, frameon=False)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig5_extension_DI_welfare.pdf")); plt.close(fig)

# ---------------------------------------------------------------- fig6
fig, ax = plt.subplots(figsize=(4.8, 3.6))
xs = np.geomspace(1e-7, 9.99, 300)
for j, DI in enumerate([0.0, 0.1]):
    p = dict(BASE, eps=6.0, DI=DI, DX=1 - BASE["DG"] - DI)
    ax.loglog(xs, [F(x, 3.0, p) for x in xs], color=C[j], label=rf"$F(X)$, $\Delta_I={DI:g}$")
ax.loglog(xs, xs, "k:", lw=1, label="45°")
ax.set_xlabel(r"$X_t$"); ax.set_ylabel(r"$X_{t+1}$")
ax.set_title(r"$\varepsilon=6$, $\tau_A=3>\tau_A^c$: floor when $\Delta_I>0$")
ax.legend(fontsize=7, frameon=False)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig6_extension_DI_floor.pdf")); plt.close(fig)

# ---------------------------------------------------------------- fig7
p = dict(BASE, eps=2.0)
tau_new, T = 8.0, 400
X = high_state(0.0, p)
U0 = welfare(X, 0.0, p)
path = []
for t in range(T):
    path.append(welfare(X, tau_new, p) - U0)   # cohort t payoff given inherited X_t
    X = F(X, tau_new, p)
path = np.array(path)
betas = np.linspace(0.5, 0.999, 200)
PV = np.array([(1 - b) * np.sum(b ** np.arange(T) * path) + b**T * path[-1] for b in betas])
fig, ax = plt.subplots(1, 2, figsize=(9, 3.3))
ax[0].plot(np.arange(T), path, color=C[0]); ax[0].axhline(0, color="k", lw=0.6)
ax[0].set_xlabel("cohort $t$ after the shock"); ax[0].set_ylabel(r"$U_t-\bar U^+(0)$")
ax[0].set_title(rf"$\tau_A$: $0\to{tau_new:g}$ at $t=0$ ($\varepsilon=2$)")
ax[1].plot(betas, PV, color=C[1]); ax[1].axhline(0, color="k", lw=0.6)
cross = betas[np.argmax(PV < 0)] if (PV < 0).any() else np.nan
ax[1].axvline(cross, color="grey", ls=":")
ax[1].set_xlabel(r"discount factor $\beta$"); ax[1].set_ylabel("normalised discounted gain")
ax[1].set_title(rf"AI shock pays off iff $\beta<{cross:.3f}$")
fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig7_transition_discounting.pdf")); plt.close(fig)

# ---------------------------------------------------------------- printed summary
print("Paper's model (Delta_I = 0), base parameters:")
print(f"  eps=2: tau* ~ {summary[2.0][0]:.2f}, U+(tau*) = {summary[2.0][1]:.4f}, U+(0) = {summary[2.0][2]:.4f}")
print(f"  eps=6: tau* ~ {summary[6.0][0]:.2f}, U+(tau*) = {summary[6.0][1]:.4f}, tau^c ~ {summary[6.0][3]:.2f} (cliff)")
print("Extension Delta_I > 0 (argmax on grid, max welfare, welfare at tau=12):")
for (eps, DI), v in ext.items():
    flag = "  <- monotone on grid" if v[0] >= taus[-1] - 1e-9 else ""
    print(f"  eps={eps:g} DI={DI:<5g} tau*={v[0]:6.2f}  maxU={v[1]:.4f}  U(12)={v[2]:.4f}{flag}")
# ---------------------------------------------------------------- fig8 planner (golden-rule steady state)
from scipy.optimize import minimize_scalar
import math


def X_ss_const_effort(e, p):
    """Steady state of X' = [S2 + (X + lG I e)^-1]^-1 under a constant effort e (closed form)."""
    k = p["lG"] * p["I"] * e
    return 0.5 * (-k + math.sqrt(k * k + 4 * k / p["S2"])) if k > 0 else 0.0


def w_given(e, X, tA, p):
    Y = p["s2i"] + p["lI"] * e + tA
    GX, GY = float(G(X)), float(G(Y))
    return p["DG"] * GX + p["DI"] * GY + p["DX"] * GX * GY - p["eps"] / (p["eps"] + 1) * e ** ((p["eps"] + 1) / p["eps"])


def planner(tA, p):
    obj = lambda le: -w_given(math.exp(le), X_ss_const_effort(math.exp(le), p), tA, p)
    r = minimize_scalar(obj, bounds=(-25, 3), method="bounded")
    return -r.fun, math.exp(r.x)


fig, ax = plt.subplots(1, 2, figsize=(9, 3.4))
plan_rows = []
for k, eps in enumerate([2.0, 6.0]):
    p = dict(BASE, eps=eps)
    Weq = np.array([U_plus(t, p) for t in taus])
    PL = [planner(t, p) for t in taus]
    Wpl = np.array([v for v, _ in PL])
    ax[k].plot(taus, Wpl, color=C[2], label="planner (externality internalised)")
    ax[k].plot(taus, Weq, color=C[0], label="equilibrium (paper)")
    ax[k].set_title(rf"$\varepsilon={eps:g}$"); ax[k].set_xlabel(r"$\tau_A$")
    plan_rows.append((eps, bool(np.all(np.diff(Wpl) >= -1e-9)), float(np.max(Wpl - Weq)), float(np.min(Wpl - Weq))))
ax[0].set_ylabel("long-run welfare"); ax[0].legend(fontsize=7, frameon=False)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig8_planner_vs_equilibrium.pdf")); plt.close(fig)

print(f"Transition (eps=2, tau 0->{tau_new}): first-cohort gain {path[0]:+.4f}, long-run change {path[-1]:+.4f}, "
      f"discounted gain turns negative at beta ~ {cross:.3f}")
for eps, mono, gmax, gmin in plan_rows:
    print(f"Planner eps={eps:g}: monotone in tau_A = {mono}; planner - equilibrium: min {gmin:+.5f}, max {gmax:+.4f}")
