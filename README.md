# Repository 4 — Acemoglu, Kong & Ozdaglar (2026)

*AI, Human Cognition and Knowledge Collapse* · NBER WP 34910 · [DOI](https://doi.org/10.3386/w34910) · [MIT version, 5 May 2026](https://economics.mit.edu/sites/default/files/2026-05/AI%2C%20Human%20Cognition%20and%20Knowledge%20Collapse%2005-05-26.pdf), 69 pages. All references and the Frisch parameterization follow that version.

## Question and individual problem

Can more accurate AI reduce incentives to learn and thereby erode the general knowledge on which society depends? Human effort creates private contextual information and, through aggregation, public general information. Agentic AI supplies contextual information only. The agent takes public precision $X$ as given and does not internalize the future social return of learning.

Let $e\ge0$ be effort, $\tau_A$ AI precision, $\sigma^{-2}$ prior contextual precision, $\lambda_I$ private learning productivity, and $G(z)=2\Phi(\sqrt z)-1$ the probability of an accurate prediction. With $\Delta_G$ the direct value of general knowledge and $\Delta_X$ the complementarity of the two knowledge types, Assumption 1 sets $\Delta_I=0$ and $\Delta_X>0$. Omitting an additive constant, the agent solves

$$\max_{e\ge0}\ U(e;X,\tau_A)=\Delta_G G(X)+\Delta_X G(X)G(Y)-\frac{\varepsilon}{\varepsilon+1}e^{(\varepsilon+1)/\varepsilon},\qquad Y=\sigma^{-2}+\lambda_I e+\tau_A.$$

At the interior optimum, $\Delta_X\lambda_I G(X)g(Y)=e^{1/\varepsilon}$, where $g=G'$.

## Main result: Observation 1 (Section 3.4)

For $X>0$, $\sigma^{-2}>0$, $\lambda_I>0$, $\varepsilon>0$, $\tau_A\ge0$, $e\ge0$, and $\Delta_X>0$ under Assumption 1, the Gaussian precision model gives

$$g(z)=\frac{\exp(-z/2)}{\sqrt{2\pi z}}>0,\qquad g'(z)=-g(z)\frac{1+z}{2z}<0\quad(z>0),$$

$$U_{eX}=\Delta_X\lambda_Ig(X)g(Y)>0,\qquad U_{e\tau_A}=\Delta_X\lambda_I G(X)g'(Y)<0.$$

General knowledge complements effort; contextual AI substitutes for effort. Strict concavity and interiority imply that optimal effort rises with $X$ and falls with $\tau_A$ (Observation 2). At $X=0$, baseline effort is zero, so strict substitution in AI precision does not hold. The dynamic mechanism additionally relies on public aggregation, knowledge depreciation and atomistic agents.

## This week's trap and our work

Decentralized steady-state welfare is not necessarily increasing in AI accuracy: the direct gain may be outweighed by reduced collective learning. The paper's welfare claims have additional conditions, including Assumption 2. Section 5 relaxes aggregation, synthetic data and separability, but not $\Delta_I=0$. We explore $\Delta_I>0$: positive effort at zero knowledge removes the zero fixed point under the extension's conditions. Our simulations illustrate—not prove globally—the welfare implications. See [extended analysis](extra/analysis-overview.md), [extensions](extensions.md) and [tutorial](extra/tutorial-ako.pdf).

## Evidence and reproduction

- [Beamer source](presentation.tex) · [18-slide PDF](presentation.pdf) · [approved handwritten proof](hand/ai-04.pdf) · [review](hand/README.md).
- [Prompts and answers](prompts.md) · [original Codex transcript](extra/chat-history.md) · [official Lean folder](lean/README.md) · [scope and validation](extra/standalone-lean/FINAL_VALIDATION_REPORT.md) · [official check evidence](extra/aml-evidence/README.md) · [successful CI](https://github.com/alejandroventuraventurameza-tech/ai-04-acemoglu/actions/runs/45557465434).
- Six standalone Lean targets (T1, T2, T3, T4, T6, T7) compile; 64 declarations pass the standard-axiom audit. The concrete Gaussian CDF bridge and full source correspondence remain open. The official AppliedModelingLib folder contains 20 unchanged generated files; its fast check, focused build, and seven selected axiom checks passed in run 45554882759. The approved six-page manuscript is published and its SHA-256 verified; slide 16 displays its original third page.
- Reproduce the illustrative figures with `pip install -r requirements.txt`, `python sim/verify_static.py`, `python sim/fig_static.py` and `python sim/welfare.py`.

The student reports permission for late submission and GPT-6 with xhigh reasoning effort. The oral presentation already took place. [PR #1](https://github.com/alejandroventuraventurameza-tech/ai-04-acemoglu/pull/1) records the submission cycle. Available original chat evidence is preserved; the separate historical cold-test answers have not been recovered. The Lean status remains explicitly partial.
