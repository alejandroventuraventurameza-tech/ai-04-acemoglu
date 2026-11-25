# Five questions about Acemoglu, Kong & Ozdaglar (2026)

*Version read: MIT author version dated 5 May 2026. Page numbers are its printed pages.*

---

## 1. What is the question asked in the paper?

> **If an AI can give each of us an accurate answer for our own particular case, will we stop
> putting effort into the general understanding that everyone else also relies on, and can
> society's shared knowledge wither away as a result?**

The topic is "AI and learning". The specific question is whether a technology that substitutes
for *private* learning can, through an externality, destroy a *public* stock of knowledge that
complements it.

## 2. What is the answer that the paper provides?

**Yes, under two conditions: effort is elastic enough and the AI is accurate enough.** If the
Frisch elasticity of effort exceeds 4 and AI accuracy exceeds a threshold $\tau_A^c$, general
knowledge collapses to zero from any starting point. Even without collapse, steady-state welfare
is **hump-shaped** in AI accuracy, so there is a finite welfare-maximising accuracy. That
motivates capping or garbling agentic AI. Better pooling of human knowledge (larger $I$) always
helps.

**Where the answer is ambiguous.** With effort elasticity below 4, knowledge only declines as AI
improves. It never vanishes at any finite accuracy. And the whole welfare answer concerns the
decentralised steady state (see Q3–Q5).

## 3. How do the authors reach their conclusion, and does it follow?

**Structure of the argument.**

1. **Model.** Two Gaussian states: a common random walk (general knowledge) and an iid
   idiosyncratic state (context). Output needs both predictions right, with strict
   complementarity ($\Delta_I=0$, $\Delta_X>0$). Effort is a *joint product*: a private signal
   about one's own case and a thin public signal pooled over an island of size $I$. Agentic AI is a
   free signal about the idiosyncratic state only.
2. **Key step: two cross-partials (Observation 1, p. 14).** General knowledge raises the marginal
   return to effort. AI lowers it, because precisions add and accuracy $G$ is concave. Everything
   dynamic follows from these two signs.
3. **Dynamics.** Effort feeds a Kalman recursion $X_{t+1}=F(X_t)$ with $F(0)=0$. Near zero, effort
   decays like $X^{\varepsilon/2}$ while the effort needed to offset depreciation decays like $X^2$.
   So $\varepsilon=4$ decides whether collapse is a trap (Lemma 2). Monotone comparative statics
   in $\tau_A$ and $I$ come from shifting $F$ (Props. 2–8).
4. **Welfare.** The envelope theorem splits $d\bar U^+/d\tau_A$ into a direct gain and a dynamic
   crowd-out loss. The loss dominates at high accuracy (Props. 10–11). The optimal policy is a
   moratorium followed by a cap (Prop. 13).
5. **No data.** It is a pure theory paper. Recent evidence is cited as motivation (e.g. Lei et al.
   2026 on K–12 students, p. 1).

**Stance.** Within the model, the conclusions follow. We re-derived Observation 1, Observation 2 and
the $\varepsilon=4$ threshold independently, checked them symbolically (`sim/verify_static.py`)
and reproduced the welfare hump and the cliff numerically (`sim/welfare.py`). The gaps are in the
step from model to message:

- **The policy conclusion does not follow from the welfare result.** The hump exists only
  because effort is under-supplied. A planner who prices the externality is never hurt by better
  AI (our Blackwell argument, tutorial §12.2). Garbling is a *second-best* instrument, and the
  paper never compares it with the first-best one.
- **The headline "collapse" rests on an assumption that is never relaxed** ($\Delta_I=0$; see Q5).
- **Robustness is asserted, not shown.** The May revision says results "continue to hold" under
  other error metrics and functional forms (p. 8) and under other normalisations (fn. 7). There
  is no proof or appendix behind either claim.

## 4. What is the paper's contribution?

**Predecessors (what it builds on).**

| Paper | What AKO take from it | What AKO add |
|---|---|---|
| **Arrow (1962); Nelson (1959)**: knowledge as a public good, under-investment in its production | The learning externality that drives everything | A technology (AI) that *widens* the externality by lowering the private return to learning |
| **Bolton & Harris (1999)**, strategic experimentation; **Smith & Sørensen (2000)** / **Banerjee (1992)**, social learning | Collective learning with free-riding on public information | An outside aggregator (AI) that supplies *private* information and crowds out the *public* production of knowledge |
| **Shumailov et al. (2024)**, model collapse (cited in a footnote, p. 32) and **Peterson (2024)**, *AI and the Problem of Knowledge Collapse* (arXiv:2404.03502; **not cited**) | The fear that AI degrades the information ecosystem | An equilibrium, incentive-based mechanism with a precise threshold ($\varepsilon=4$, $\tau_A^c$), in contrast to model-side or distributional stories |

The phrase "knowledge collapse" for AI was used by Peterson (2024), whom the paper does not
cite. The mechanisms differ: Peterson's is about AI narrowing the distribution of knowledge that
gets accessed, AKO's about incentives to produce it. Still, the omission is worth noting.

**Follow-ups.** The paper is from 2026 and the literature is only forming. Two candidates, both
still to be read before we cite them:
- arXiv:2607.13272 (*The tragedy of the cognitive commons: collective intelligence beyond
  AI-induced knowledge collapse*). By its title it engages the knowledge-collapse hypothesis
  directly.
- Within this course, **Bastani & Cachon** (*The Human-AI Contracting Paradox*, week 8) is a
  sibling rather than a follow-up: more reliable AI crowds out human effort through a
  moral-hazard channel. The May version appears to describe it in its literature review, under a
  mismatched citation (see `version-comparison.md` §4).

**Marginal contribution.** A **new mechanism** and a **new question**. The method is standard
(Normal–Normal updating, a monotone one-dimensional map, Topkis), and there is no data. The novelty
is the joint-product structure of learning combined with an AI that substitutes for only one of
the two products. That structure turns a static substitution result, of the kind seen in
Aouad–Lykouris–Zhong in week 1, into a dynamic public-goods problem with a tipping point.

## 5. What parts are unconvincing, and why?

### (a) The welfare criterion and the instrument set, not the model, deliver "regulate AI"

- **Better information cannot hurt a planner.** Along any fixed effort path the stock of general
  knowledge does not depend on $\tau_A$, and every period's utility rises with $\tau_A$. So the
  planner's optimal value is nondecreasing in $\tau_A$ (tutorial, Result 4; `figures/fig8`). The
  welfare hump is therefore a symptom of under-provided learning, which the May version itself
  concedes is present "regardless" (p. 25). The natural remedy is to raise the private return to
  contributing general knowledge: subsidies, credit, open repositories. The paper's information
  design (p. 28) instead restricts the regulator to *garbling*, i.e. destroying information. It
  never shows why the first-best instrument is unavailable.
- **The criterion makes the proposed policy look free.** Policies are ranked by long-run average
  welfare, under which "finite transitions have vanishing weight" (p. 29). The moratorium phase of
  Proposition 13, full suppression of AI for $M^\star$ periods, therefore costs nothing by
  construction. With discounting it does. In our simulation, raising $\tau_A$ from 0 to 8 lowers
  steady-state welfare but raises discounted welfare for any discount factor below about 0.93
  (`figures/fig7`).

### (b) "Knowledge collapse" is a knife-edge of the one production assumption never relaxed

Assumption 1 imposes $\Delta_I=0$: context knowledge alone is worthless. That is what makes effort
zero at $X=0$, and hence zero a steady state. Section 5 relaxes three assumptions, all on the
information and aggregation side, and none touches production. We relaxed it (tutorial §14):

- **Collapse disappears.** With any $\Delta_I>0$, $F(0)>0$ and knowledge converges to a positive
  level for every finite AI accuracy. It becomes a "knowledge-poverty" floor, which can be tiny.
- **The welfare message survives, and is more robust than the collapse.** Welfare now tends to
  $\Delta_I$ rather than 0. For $\varepsilon<4$ it stays above that limit at high accuracy, so the
  optimal accuracy is still finite. The same threshold 4 reappears, now comparing $\gamma^{\varepsilon/4}$
  with $\gamma$. Numerically the optimal accuracy *rises* with $\Delta_I$.

So the paper's most quotable claim, that general knowledge "vanishes ultimately" (abstract), is the
least robust one. The more modest claim, an interior optimal AI accuracy in a second-best world,
is the one that survives.
