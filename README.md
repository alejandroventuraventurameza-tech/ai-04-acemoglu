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

**Observation 1 (§3.4).** Under Assumption 1 ($\Delta_I=0$, $\Delta_X>0$), positive learning productivity and prior precision, nonnegative effort and AI precision, and for $X>0$,

$$\frac{\partial^2 U}{\partial e\,\partial X} = \Delta_X\lambda_I\,g(X)\,g(Y) > 0,
\qquad
\frac{\partial^2 U}{\partial e\,\partial \tau_A} = \Delta_X\lambda_I\,G(X)\,g'(Y) < 0 .$$

General knowledge **complements** human effort, and agentic AI **substitutes** for it. The first
sign comes from the production side ($\Delta_X>0$). The second comes from the information side:
precisions add, and $G$ is concave because $g'(\tau) = -g(\tau)\frac{1+\tau}{2\tau}<0$.
**Observation 2** (§3.5) follows (implicit function theorem or Topkis): best-response effort
$e(X,\tau_A)$ is the unique root of $\Delta_X G(X)\lambda_I g(Y)=e^{1/\varepsilon}$, increasing
in $X$ and decreasing in $\tau_A$, strictly for $X>0$.

**Conditions it rests on:** positive $\lambda_I$, $X>0$ for strict signs, Gaussian states and signals (precisions add); AI informative only
about the idiosyncratic state; Assumption 1; $\sigma^{-2}>0$; isoelastic effort cost
(Frisch elasticity $\varepsilon>0$); atomistic agents.

**What it delivers dynamically (read, not reproduced).** $X_{t+1}=F(X_t)$ with $F(0)=0$
(Prop. 1, Lemma 1). The Frisch elasticity splits two regimes (Lemma 2):
- $\varepsilon<4$: a unique positive steady state, which falls as AI improves (Props. 3–4).
- $\varepsilon>4$: $X=0$ is a locally stable **knowledge-collapse** trap, and above a threshold
  $\tau_A^c$ collapse is global (Prop. 5).

Under the paper's welfare conditions, decentralised steady-state welfare is **not necessarily increasing** in $\tau_A$ (Props. 10–11, which also need Assumption 2:
$\sigma^{-2}\ge\sqrt2-1$).

## This week's trap — our answers

1. **Is welfare increasing in AI accuracy?** It depends on who chooses effort and on the horizon.
   - *Yes* holding general knowledge fixed (envelope theorem).
   - *Yes, always,* for a planner who prices the learning externality (a Blackwell argument, ours).
   - *No* in the decentralised steady state: welfare is hump-shaped (Props. 10–11), and with
     $\varepsilon>4$ it falls off a cliff at $\tau_A^c$.
   - The paper's long-run-average criterion gives transitions zero weight. Under discounting, the
     same AI improvement can raise welfare.
2. **Which assumptions do the authors relax?** Section 5 relaxes aggregation (§5.1), synthetic data
   (§5.2) and separability (§5.3), all on the information side. **The production-side assumption
   never touched is $\Delta_I=0$** (Assumption 1). We relaxed it. Complete collapse disappears and
   the welfare limit becomes $\Delta_I$, but the interior optimum survives. For $\varepsilon<4$ the tutorial gives an asymptotic argument; the numerical examples illustrate the extension, not a general uniqueness result.
3. **Version.** We read the 5 May 2026 author version. It differs from the February NBER release
   in notation and in three new, unproven robustness claims; see `extra/version-comparison.md`.

---

## What is in this repository

| File | What it is |
|---|---|
| `README.md` | This page |
| `prompts.md` | The LLM conversations, raw |
| `hand/` | Handwritten derivation(s) — see `hand/README.md` |
| `presentation.tex` / `.pdf` | The required 20-minute Beamer deck (source present; PDF and hand evidence pending verification) |
| `extra/tutorial-ako.pdf` | Deep-immersion tutorial (18 pp.). Part I: static problem, Observations 1–2, the bridge to Lemma 2. Part II: welfare, the trap, and the $\Delta_I>0$ extension with proofs |
| `extensions.md` | Dead ends (already in §5), what we relaxed ($\Delta_I>0$, planner, discounting), and four open extensions |
| `extra/five-questions.md` | The question, the answer, the argument, the contribution, and what is unconvincing |
| `extra/version-comparison.md` | What changed between the February (NBER) and May (MIT) versions |
| `sim/verify_static.py` | SymPy check of every algebraic step in the static block |
| `sim/model.py`, `sim/fig_static.py`, `sim/welfare.py` | Numerical model; figures 1–3 (static block) and 4–8 (welfare, extension, transition, planner) |
| `lean/` | Standalone Lean 4 project; T1/T2 compiled and axiom-audited on initial CI. T3/T4/T6/T7 added and awaiting fresh checks. Official AppliedModelingLib folder and paper-scoped check still pending. |
| `lean/FINAL_VALIDATION_REPORT.md` | Exact proof boundary, source version, and CI evidence |
| `paper/` | How to get the PDF (not committed) |

## Delivery status

The student reports the professor authorized late delivery and GPT-6 with xhigh reasoning effort; the presentation has already taken place. Slides remain a required repository artifact. The manuscript photo and the full AppliedModelingLib contribution workflow are not yet complete; this is a candidate, not a final submission. See [PR #1](https://github.com/alejandroventuraventurameza-tech/ai-04-acemoglu/pull/1).

## Reproduce

```bash
pip install -r requirements.txt
python sim/verify_static.py      # symbolic checks — every line should print OK
python sim/fig_static.py         # figures 1-3
python sim/welfare.py            # figures 4-8 and the numbers quoted in the tutorial (~30 s)
```
