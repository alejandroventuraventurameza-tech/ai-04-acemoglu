# Extensions: what could be relaxed, what is already taken, what we did

*Version read: MIT author version, 5 May 2026.*

We sort ideas by status and apply the course's three filters in order. Is it already in the paper?
Does one equation change, or all of them? Can we say what we expect before computing?

---

## Dead ends: already done by the authors (Section 5)

| Idea an LLM will propose | Where it already is | Equation that changes |
|---|---|---|
| "Let AI also improve the aggregation of general knowledge" | **§5.1**, Prop. 14 | $I\mapsto I(\tau_A)=I_0+e^{\eta\tau_A}$. Results survive if $\eta<\varepsilon/2$ |
| "Let AI generate synthetic data that adds to general knowledge" | **§5.2**, Prop. 15 | $X_{t+1}^{-1}=(X_t+\lambda_G E_t+\tau_{syn})^{-1}+\Sigma^2$. The collapse trap becomes a positive low state |
| "Decouple private and public learning" | **§5.3**, Prop. 16 | Public input $\lambda_G e^\beta$. The threshold becomes $\varepsilon<4/\beta$ |

All three act on the **information and aggregation side**. The appendix adds no other extension,
and there is no trace of $\Delta_I$ in it (`extra/version-comparison.md`).

## Done here (above the floor)

### 1. $\Delta_I>0$: context knowledge with stand-alone value — *the production-side assumption never relaxed*

- **One equation changes.** The FOC becomes $\lambda_I[\Delta_I+\Delta_X G(X)]\,g(Y)=e^{1/\varepsilon}$.
- **Expected beforehand:** collapse disappears, and the welfare limit rises from 0 to $\Delta_I$.
- **Found:** tutorial §14, Result 5; `sim/welfare.py`; figures 5–6.
  - Observation 1 survives, and now also holds at $X=0$.
  - $F(0)>0$, so there is no complete collapse for any finite $\tau_A$. A tiny "knowledge-poverty"
    floor remains, of order $\gamma^{\varepsilon/2}$.
  - Welfare converges to $\Delta_I$.
  - **Not expected:** the welfare hump survives. For $\varepsilon<4$ we prove the optimal accuracy
    stays finite, and the proof reuses the threshold 4 by comparing $\gamma^{\varepsilon/4}$ with
    $\gamma$. For $\varepsilon>4$ it stays finite in every case we computed. The optimal
    accuracy $\tau_A^\star$ *increases* with $\Delta_I$.
- **Verdict:** the collapse claim is fragile; the regulation claim is robust.

### 2. Who chooses effort: planner vs. equilibrium

- **Equations:** none change. We compare two solution concepts.
- **Found:** a Blackwell-type argument (tutorial §12.2, Result 4). The planner's value is
  nondecreasing in $\tau_A$ under *any* criterion increasing in per-period utilities. Numerically
  (figure 8), the golden-rule planner's welfare is monotone while the equilibrium's is
  hump-shaped.
- **Implication:** the non-monotonicity is entirely an externality phenomenon, and garbling is a
  second-best instrument.

### 3. Discounting vs. long-run average

- **Equations:** only the welfare criterion changes, from $\liminf \frac1T\sum U_t$ to
  $(1-\beta)\sum\beta^tU_t$.
- **Found:** after a rise in $\tau_A$ the first cohorts gain and later cohorts lose (figure 7).
  Raising $\tau_A$ from 0 to 8 lowers steady-state welfare, but it raises discounted welfare for
  $\beta\lesssim0.93$.
- **Implication:** the moratorium in Prop. 13 is costless only because of the criterion.

## Open: what we would do next

### 4. Endogenous AI accuracy: AI is trained on human general knowledge ★

The introduction says community knowledge "is itself an input into the AI models" (p. 4). Yet in
the model $\tau_A$ is **exogenous** and independent of $X$. The natural relaxation is
$\tau_A=\bar\tau\,h(X)$ with $h$ increasing: AI learns from what humans know.

- **Equation that changes:** $Y=\sigma^{-2}+\lambda_I e+\bar\tau h(X)$.
- **Consequence for Observation 1:**
  $$U_{eX}=\Delta_X\lambda_I\bigl[g(X)g(Y)+G(X)\,g'(Y)\,\bar\tau h'(X)\bigr].$$
  The first term is the paper's complementarity. The second is **negative**: more general
  knowledge makes the AI better, which crowds out effort. **The sign of the complementarity
  becomes ambiguous.**
- **What we expect:** dynamics become *self-correcting* near collapse. As $X$ falls, AI worsens
  and the incentive to learn returns. So collapse should be harder, and a Shumailov-style feedback
  enters the model. This collides the paper with the model-collapse literature it cites only in a
  footnote.

### 5. Rewarding contributions (first-best) vs. garbling (second-best)

- **Equation that changes:** add a subsidy $s$ per unit of effort, so the FOC gains $+s$.
- **What we expect:** a constant $s$ can implement the planner's steady state with *no* loss of
  AI accuracy. The question is whether a budget-balanced $s$ beats the optimal cap $\tau^\star$.
  By Result 4 it should, whenever it is feasible.

### 6. Heterogeneous effort elasticity

- **Equation that changes:** two types with $\varepsilon_L<4<\varepsilon_H$ and shares $(\mu,1-\mu)$;
  the public input becomes $I[\mu e_L+(1-\mu)e_H]$.
- **What we expect:** near $X=0$ the least elastic type dominates, since $X^{\varepsilon_L/2}$ decays
  slowest. So any positive mass with $\varepsilon<4$ should make collapse locally unstable. That
  is a sharp, testable prediction.

### 7. Test the May version's robustness claim (p. 8)

- **Equation that changes:** replace the tolerance band by a bounded reward $h$ of the error,
  e.g. $h(z)=e^{-z^2/2}$, so $G_h(\tau)=\sqrt{\tau/(\tau+1)}$.
- **What we expect:** the square-root law near 0 is generic for bounded integrable $h$ (tutorial
  §13), so the threshold 4 should survive. With squared-error loss it should not.
