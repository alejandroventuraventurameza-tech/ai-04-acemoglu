"""Figures for the static block (Section 3.4) and the bridge to Lemma 2.
Run from the repository root:  python sim/fig_static.py   -> writes figures/*.pdf"""
import os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(__file__))
from model import BASE, G, g, e_br, e_m, F, steady_states

OUT = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
C = ["#1f4e79", "#c55a11", "#548235"]

# 1. G and g ---------------------------------------------------------------
t = np.linspace(1e-3, 8, 600)
fig, ax = plt.subplots(1, 2, figsize=(8, 3))
ax[0].plot(t, G(t), color=C[0]); ax[0].set_title(r"$G(\tau)=2\Phi(\sqrt{\tau})-1$ (concave)")
ax[0].set_xlabel(r"precision $\tau$")
ax[1].plot(t, g(t), color=C[1]); ax[1].set_ylim(0, 1.5)
ax[1].set_title(r"$g(\tau)=G'(\tau)=\phi(\sqrt{\tau})/\sqrt{\tau}$ (decreasing)")
ax[1].set_xlabel(r"precision $\tau$")
fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig1_G_g.pdf")); plt.close(fig)

# 2. Best response vs maintenance effort, log-log --------------------------
fig, ax = plt.subplots(1, 2, figsize=(8.5, 3.4), sharey=True)
xs = np.geomspace(1e-6, 9.99, 400)
for k, eps in enumerate([2.0, 6.0]):
    p = dict(BASE, eps=eps)
    for j, tA in enumerate([0.0, 1.0, 3.0]):
        ax[k].loglog(xs, [e_br(x, tA, p) for x in xs], color=C[j], label=rf"$e(X,\tau_A)$, $\tau_A={tA:g}$")
    ax[k].loglog(xs, e_m(xs, p), "k--", label=r"maintenance $e_m(X)$")
    ax[k].set_title(rf"$\varepsilon={eps:g}$: slope of $e$ near 0 is $\varepsilon/2={eps/2:g}$ vs. 2")
    ax[k].set_xlabel(r"general knowledge $X$ (log)")
    ax[k].set_ylim(1e-14, 1e2)
ax[0].set_ylabel("effort (log)")
ax[1].legend(fontsize=7, loc="lower right", frameon=False)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig2_effort_vs_maintenance.pdf")); plt.close(fig)

# 3. 45-degree diagram for eps > 4 ------------------------------------------
p = dict(BASE, eps=6.0)
xs = np.linspace(0, 9.99, 400)
fig, ax = plt.subplots(figsize=(4.6, 3.6))
ax.plot(xs, xs, "k:", lw=1, label="45°")
for j, tA in enumerate([0.0, 1.0, 3.0]):
    ax.plot(xs, [F(x, tA, p) for x in xs], color=C[j], label=rf"$F(X)$, $\tau_A={tA:g}$")
    for r in steady_states(tA, p):
        ax.plot(r, r, "o", color=C[j], ms=4)
ax.plot(0, 0, "ko", ms=4)
ax.set_xlabel(r"$X_t$"); ax.set_ylabel(r"$X_{t+1}$"); ax.legend(fontsize=7, frameon=False)
ax.set_title(r"$\varepsilon=6$: collapse, threshold, high state")
fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig3_45degree_eps6.pdf")); plt.close(fig)

for eps in [2.0, 6.0]:
    p = dict(BASE, eps=eps)
    for tA in [0.0, 1.0, 3.0]:
        print(f"eps={eps:g} tau_A={tA:g}  positive steady states:", [round(r, 5) for r in steady_states(tA, p)])
