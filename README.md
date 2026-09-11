# Repository 4 — Acemoglu, Kong & Ozdaglar (2026)

*AI, Human Cognition and Knowledge Collapse* ·
[NBER WP 34910](https://www.nber.org/papers/w34910) · [doi:10.3386/w34910](https://doi.org/10.3386/w34910)

> **Version read: MIT author version dated 5 May 2026 (69 pp.)** of NBER WP 34910. This is the file
> the course repository distributes. It is an unrefereed working paper that exists in two versions:
> the NBER release is dated February 2026. Page numbers here are the printed pages of the May PDF:
> the model is §3, Observation 1 is §3.4 (p. 14) and Observation 2 is §3.5 (p. 16). What changed
> between the two versions is in [`extra/version-comparison.md`](extra/version-comparison.md).

---

## What question the paper answers

If agentic AI gives each person an accurate answer for *their own case*, do people stop investing
in the *general* understanding that everyone relies on — and can society's stock of general
knowledge collapse as a result?

## The agent's problem

Two kinds of knowledge. The common state $\theta_t$ (general knowledge) is a Gaussian random walk
with innovation variance $\Sigma^2$. The idiosyncratic state $\theta_{i,t}\sim N(0,\sigma^2)$
(context knowledge) is iid over time. Effort $e$ buys a private signal of precision $\lambda_I e$
about $\theta_{i,t}$ and, pooled over an island of mass $I$, a public signal of precision
$\lambda_G E$ about $\theta_t$. Agentic AI adds a signal of precision $\tau_A$ about
$\theta_{i,t}$ only. Precisions add, so

$$Y = \sigma^{-2} + \lambda_I e + \tau_A, \qquad X_{t+1}^{-1} = (X_t+\lambda_G E_t)^{-1} + \Sigma^2 .$$

With $G(\tau)=2\Phi(\sqrt\tau)-1$ the probability that a prediction with posterior precision
$\tau$ lands within 1 of the truth, each agent solves the **static** problem

$$\max_{e\ge 0}\; \Delta_G\,G(X) + \Delta_X\,G(X)\,G(\sigma^{-2}+\lambda_I e+\tau_A) - \tfrac{\varepsilon}{\varepsilon+1}\,e^{\frac{\varepsilon+1}{\varepsilon}},\qquad \varepsilon>0 \text{ (Frisch elasticity of effort).}$$

It is static because the agent is atomistic (her effort does not move $X_{t+1}$) and context
knowledge is worthless tomorrow. That same fact is the **externality**: nobody is paid for adding
to general knowledge.

## The main result, with all its conditions

**Observation 1 (§3.4).** Under Assumption 1 ($\Delta_I=0$, $\Delta_X>0$) and for $X>0$,

$$\frac{\partial^2 U}{\partial e\,\partial X} = \Delta_X\lambda_I\,g(X)\,g(Y) > 0,
\qquad
\frac{\partial^2 U}{\partial e\,\partial \tau_A} = \Delta_X\lambda_I\,G(X)\,g'(Y) < 0 .$$

General knowledge **complements** human effort, and agentic AI **substitutes** for it. The first
sign comes from the production side ($\Delta_X>0$). The second comes from the information side:
precisions add, and $G$ is concave because $g'(\tau) = -g(\tau)\frac{1+\tau}{2\tau}<0$.
**Observation 2** (§3.5) follows (implicit function theorem or Topkis): best-response effort
$e(X,\tau_A)$ is the unique root of $\Delta_X G(X)\lambda_I g(Y)=e^{1/\varepsilon}$, increasing
in $X$ and decreasing in $\tau_A$, strictly for $X>0$.

**Conditions it rests on:** Gaussian states and signals (precisions add); AI informative only
about the idiosyncratic state; Assumption 1; $\sigma^{-2}>0$; isoelastic effort cost
(Frisch elasticity $\varepsilon>0$); atomistic agents.

**What it delivers dynamically (read, not reproduced).** $X_{t+1}=F(X_t)$ with $F(0)=0$
(Prop. 1, Lemma 1). The Frisch elasticity splits two regimes (Lemma 2):
- $\varepsilon<4$: a unique positive steady state, which falls as AI improves (Props. 3–4).
- $\varepsilon>4$: $X=0$ is a locally stable **knowledge-collapse** trap, and above a threshold
  $\tau_A^c$ collapse is global (Prop. 5).

Steady-state welfare is **hump-shaped** in $\tau_A$ (Props. 10–11, which also need Assumption 2:
$\sigma^{-2}\ge\sqrt2-1$).

---

## What is in this repository

| File | What it is |
|---|---|
| `README.md` | This page |
| `prompts.md` | The LLM conversations, raw |
| `hand/` | Handwritten derivation(s) — see `hand/README.md` |
| `presentation.tex` / `.pdf` | The 5-minute Beamer deck *(in progress)* |
| `extra/tutorial-ako.pdf` | Deep-immersion tutorial, Part I: environment, Bayesian updating, static problem, Observations 1–2, the bridge to Lemma 2 |
| `extra/version-comparison.md` | What changed between the February (NBER) and May (MIT) versions |
| `sim/verify_static.py` | SymPy check of every algebraic step in the static block |
| `sim/model.py`, `sim/fig_static.py` | Numerical model and the figures in `figures/` |
| `lean/CHATGPT_CONTEXT.md` | Brief for the Lean 4 formalization (done with ChatGPT; Claude audits it) |
| `paper/` | How to get the PDF (not committed) |

## Reproduce

```bash
pip install -r requirements.txt
python sim/verify_static.py      # symbolic checks — every line should print OK
python sim/fig_static.py         # regenerates figures/
```
