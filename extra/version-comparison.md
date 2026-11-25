# Which version did we read? February (NBER) vs. May (MIT)

The assignment warns that this paper "is an unrefereed NBER working paper existing in more than
one version" and asks us to "verify against the PDF you actually downloaded, and say which
version you read". We downloaded both versions and compared them sentence by sentence (text
extracted with `pdftotext`, aligned with `difflib`; changes that only swap notation were
filtered out).

| | February | May |
|---|---|---|
| Source | NBER WP 34910 (nber.org), cover dated February 2026 | Author version (economics.mit.edu), dated 5 May 2026 |
| PDF metadata | created 20 Feb 2026 | created 5 May 2026, modified 8 May 2026 |
| Length | 69 pp. | 69 pp. |
| **Used in this repository** | for comparison only | **read and cited** |

Page numbers below are the printed page numbers of the May PDF.

## 1. What did *not* change

- **The model.** Environment, signals, Assumption 1 ($\Delta_I=0$, $\Delta_X>0$), Assumption 2
  ($\sigma^{-2}\ge\sqrt2-1$), and the statements of Observations 1–2, Lemmas 1–2 and
  Propositions 1–16 are the same.
- **Section numbering.** The model is §3 (§2 is the related literature), Observation 1 is §3.4,
  Observation 2 is §3.5, and the extensions are §5.1–5.3 in both versions. The assignment's
  "Sections 2 and 3.4" matches neither version literally. The static problem it refers to is
  §3.1–3.5.
- **The appendix.** Apart from notation, the proofs are unchanged: one sentence of wording
  differs across 348 sentences.
- **Nowhere in either version is $\Delta_I>0$ considered.** $\Delta_I$ appears only in §3–4 of the
  main text, never in the appendix.

## 2. Notation change (no change in substance)

| | February | May |
|---|---|---|
| Effort cost | $\frac1\alpha e^\alpha$, $\alpha>1$ | $\frac{\varepsilon}{\varepsilon+1}e^{(\varepsilon+1)/\varepsilon}$, $\varepsilon>0$ the Frisch elasticity (p. 9) |
| Marginal cost | $e^{\alpha-1}$ | $e^{1/\varepsilon}$ |
| Regime threshold | $\alpha-1\gtrless\frac14$ | $\varepsilon\lessgtr4$ |
| Effort near 0 | $\Theta(X^{1/(2(\alpha-1))})$ | $\Theta(X^{\varepsilon/2})$ (p. 18) |
| $\eta^{crit}$ (Prop. 14) | $1/[2(\alpha-1)]$ | $\varepsilon/2$ |
| $\lim \tau_A^\star/\tau_A^c$ | $1/\alpha$ | $\varepsilon/(\varepsilon+1)$ |
| Assumption 2 counterexample | $\alpha=100$ | $\varepsilon=0.01$ |

The two are the same model under $\varepsilon=1/(\alpha-1)$; February defines this dictionary
itself. The counterexample row is only approximately consistent ($1/99\approx0.0101$). That
is harmless, but the example is not literally the same.

## 3. Substantive additions in May — and why they matter for us

| # | Where | What May adds | Our reading |
|---|---|---|---|
| A | §3.1, p. 8 | "The fact that payoff depends on whether the prediction errors are less than 1 is **entirely** for simplicity. **Our qualitative results continue to hold when payoffs are defined over other metrics of prediction errors and using other functional forms.**" | A robustness claim with **no proof or appendix behind it**. The results use $G(\tau)=2\Phi(\sqrt\tau)-1$ concretely: concavity drives the substitution sign, and $G(X)\sim\sqrt{2X/\pi}$ drives the $\varepsilon=4$ threshold. Our check is partly in their favour. For any **bounded, integrable** reward $h$ of the prediction error, $\mathbb E[h(Z)]=\sqrt{\tau/2\pi}\int h\,(1+o(1))$ as $\tau\to0$, so the square-root law, and with it the threshold 4, is generic. It fails for **unbounded losses** such as squared error: expected loss $-1/\tau$ has a marginal value of precision that explodes as $X\to0$. And concavity in $\tau$ is not automatic for every $h$. So the claim is plausible for a class of payoffs and not shown for "other functional forms" in general. |
| B | §3.6, p. 22, fn. 7 | When $\Delta_X$ rises, "$\Delta_G$ needs to be adjusted in order to satisfy the normalization $\Delta_X+\Delta_G=1$ … **our qualitative results do not depend on this normalization**." | The normalization $\Delta_X+\Delta_G=1$ silently uses $\Delta_I=0$. Another unproven robustness claim, and one that again leans on the production-side assumption that is never relaxed. |
| C | §3.1, p. 10 | Agents' "individual incentives come **entirely** from context-specific learning. We view this as a natural benchmark since learning externalities from general knowledge are typically much larger than an individual's utility from that general knowledge." | A new justification for the atomistic-agent assumption. It makes explicit that agents get **zero private value** from their contribution to general knowledge. |
| D | §4.1, p. 25 | "regardless of whether there is a unique or multiple steady states … **human effort is always under-supplied because of the general knowledge externality**. This under-provision of effort is at the root of the results presented in the rest of the section." | Central to the week's trap. The welfare hump in $\tau_A$ is a statement about an economy that already under-invests in learning. Welfare is not maximised in the first-best sense even at $\tau_A=0$. |
| E | §4.4, p. 28 | "because the benefits of larger $I$ only scale with $\log I$, any aggregation benefits of AI will tend to be small relative to AI's agentic capabilities that change $\tau_A^c$." | A new policy-flavoured implication of Prop. 12. It anticipates §5.1. |
| F | §5, p. 30 | "Our main purpose is to show that the simplifying assumptions imposed in our baseline model do not change the general insights." | Sets up the trap question. The three extensions (5.1 aggregation, 5.2 synthetic data, 5.3 separability) touch only the **information/aggregation side**. The production function $f$ and Assumption 1 ($\Delta_I=0$) are never touched. |
| G | §3.6, p. 17 | The collapse steady state now points to "Sections 5.1 and 5.2 for generalizations". | Collapse is generalised only on the information side. |
| H | Intro, p. 1 | New evidence: Lei et al. (2026), 26,811 Chinese K–12 students over 30 months. AI raises homework scores but lowers closed-book and entrance-exam scores. | Stronger empirical motivation for the substitution channel. |
| I | Intro, p. 4 | Adds the premise that "useful collective knowledge needs to be replenished constantly". "All human knowledge is destroyed" becomes "all **(useful)** human knowledge". | A softer framing of collapse. Economically it is the same thing: the random walk with $\Sigma^2>0$. |
| J | Intro, p. 5 | "Two-**period** garbling policy" becomes "two-**phase**", with an explanation of each phase. | A correction. Prop. 13 was always about phases. |

## 4. A citation that does not match its reference (May only)

§2 (Related Literature, p. 6) adds:

> "In a complementary principal-agent framework, Bastani et al. (2024) show that more reliable AI
> can reduce human oversight effort and harm welfare in human-AI teams, because motivating costly
> human inspection of rare AI errors becomes prohibitively expensive, leading the principal to
> abandon human-AI collaboration or to prefer a less reliable AI tool."

The only Bastani entry in the bibliography is *Hamsa Bastani, Osbert Bastani, Alp Sungu, Haosen
Ge, Özge Kabakcı, and Rei Mariman, "Generative AI can harm learning", Wharton School Research
Paper, 2024*. That paper is a field experiment with students, not a principal-agent model. The
description in the text matches **Bastani & Cachon, *The Human-AI Contracting Paradox***
(SSRN 5962739), which is the course's week-8 paper. The citation appears to point to the wrong
reference.
*Status: our reading. Check it against the Bastani & Cachon abstract before quoting it in class.*

## 5. Bottom line for the assignment

- **Version read and cited:** the MIT author version dated 5 May 2026.
- **Every result we use is identical in both versions**; only the notation changes.
- **The May revision adds robustness claims (A, B, F) but no new robustness results.** All three
  concern the production side or functional forms. Those are exactly the parts that no
  extension in §5 relaxes.
