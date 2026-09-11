# Context brief for ChatGPT — Lean 4 formalization of Acemoglu, Kong & Ozdaglar (2026)

> **How to use this file.** Paste it in full as the first message of a new ChatGPT
> conversation (use the strongest reasoning model available). Attach, if you can:
> (1) the paper PDF, (2) `extra/tutorial-ako.pdf` from this repository.
> Then work through the targets **one at a time**, in order, pasting back the exact
> `lake build` output after each attempt.

---

## 0. Who is who in this project

This is a joint human–AI project for the course *Artificial Intelligence and Economic
Modeling* (Universidad del Pacífico, 2026-II). The course treats language models as
**proof assistants**, and the student always has the last word.

| Role | Who | Responsibility |
|---|---|---|
| Student, final judge | Alejandro | Runs every command locally, decides what is accepted, writes the handwritten derivation |
| Mathematical derivation and tutorial | Claude | Re-derives the paper's results on paper, writes the tutorial, SymPy checks and simulations |
| **Formal verification (you)** | **ChatGPT** | **Writes Lean 4 + Mathlib code that states and proves the targets below; audits Claude's derivations** |

The two AIs audit each other. If you find that a statement below is **false, mis-stated, or
missing a hypothesis**, say so explicitly — with a counterexample if you can — instead of
quietly changing it. A correct objection is worth more than a proof of the wrong statement.

## 1. The paper

**Acemoglu, D., Kong, D., & Ozdaglar, A. (2026).** *AI, Human Cognition and Knowledge
Collapse.* NBER Working Paper 34910. **We read the MIT author version dated 5 May 2026
(69 pp.)**; attach that PDF. It is an unrefereed working paper in two versions, so quote only
what is in the attached PDF.

**Notation.** The May version writes the effort cost as `(ε/(ε+1)) e^{(ε+1)/ε}`, with ε > 0 the
Frisch elasticity, so marginal cost is `e^{1/ε}`. (The February NBER version wrote `(1/α) e^α`,
with thresholds `α − 1 ≷ 1/4`; it is the same model under `ε = 1/(α − 1)`.) If `rpow` with the
exponent `(ε+1)/ε` is awkward in Lean, you may parametrize by `alpha := 1 + 1/eps` and prove the
dictionary as a lemma.

**The model in one paragraph.** A common state θ_t (general knowledge) follows a Gaussian
random walk with innovation variance Σ²; each agent also faces an iid idiosyncratic state
θ_{i,t} ~ N(0, σ²) (context knowledge). Effort e ≥ 0 buys a private signal about θ_{i,t}
with precision λ_I·e and, pooled over an island of mass I, a public signal about θ_t with
precision λ_G·E. Agentic AI gives each agent a signal about θ_{i,t} with precision τ_A.
Output depends on whether each prediction lands within distance 1 of the truth.

**Objects you need.**

- Accuracy as a function of posterior precision τ:
  `G(τ) = P(|Z| ≤ 1), Z ~ N(0, 1/τ)`, so `G(τ) = 2Φ(√τ) − 1`.
- Its derivative: `g(τ) = G'(τ) = φ(√τ)/√τ = (2π)^{-1/2} · τ^{-1/2} · exp(−τ/2)`.
- Idiosyncratic precision (paper eq. 4): `Y = σ⁻² + λ_I e + τ_A`.
- Expected payoff (eq. 6, with Assumption 1: Δ_I = 0, Δ_X > 0):
  `U(e; X, τ_A) = f(0,0) + Δ_G G(X) + Δ_X G(X) G(Y) − (ε/(ε+1)) e^{(ε+1)/ε}`.
- Marginal payoff of effort: `U_e = Δ_X G(X) λ_I g(Y) − e^{1/ε}`.
- Best response `e(X, τ_A)`: unique root of the FOC `Δ_X G(X) λ_I g(σ⁻² + λ_I e + τ_A) = e^{1/ε}`
  when X > 0; equal to 0 when X = 0.
- Public-precision recursion (eq. 3 and Proposition 1):
  `X_{t+1} = F(X_t) = [Σ² + (X_t + λ_G I e(X_t, τ_A))⁻¹]⁻¹`.
- **Maintenance effort** (defined by us, not by the paper):
  `e_m(X) = Σ² X² / (λ_G I (1 − Σ² X))` for `0 < X < Σ⁻²`.

**The results in scope.**

- **Observation 1 (§3.4).** `∂²U/∂e∂X > 0` and `∂²U/∂e∂τ_A < 0` for X > 0: general
  knowledge complements effort, agentic AI substitutes for it.
- **Observation 2 (§3.5).** `e(X, τ_A)` is increasing in X and decreasing in τ_A, strictly for X > 0.
- **Lemma 2.** If ε < 4 the collapse state X = 0 is locally unstable (F(X) > X near 0);
  if ε > 4 it is locally stable (F(X) < X near 0). Mechanism: near 0,
  `e(X) ≈ κ X^{ε/2}` while `e_m(X) ≈ (Σ²/(λ_G I)) X²`.

## 2. Setup and conventions

- **Lean 4 + Mathlib**, pinned to the same toolchain as the course-recommended library
  [AppliedModelingLib / EconCSLib](https://github.com/nikhgarg/EconCSLib):
  `lean-toolchain = leanprover/lean4:v4.30.0-rc2`, Mathlib tag `v4.30.0-rc2`
  (rev `5450b53e5ddc75d46418fabb605edbf36bd0beb6`). If some lemma name has moved in that
  version, tell me and suggest the replacement — do not invent names.
- A **standalone Lake project** lives in this repository's `lean/` folder. It follows
  AppliedModelingLib's conventions so it could later be contributed upstream:

  ```
  lean/
  ├── lakefile.toml
  ├── lean-toolchain
  ├── AKO26KnowledgeCollapse.lean              -- root import
  └── AKO26KnowledgeCollapse/
      ├── Assumptions.lean      -- parameters, hypotheses as structures, one docstring per hypothesis
      ├── PaperInterface.lean   -- one `def ...Spec : Prop` per target, in paper order, readable
      ├── ProofInterface.lean   -- `theorem ..._holds : ...Spec := ...` for each Spec
      └── MainTheorems.lean     -- helper lemmas
  ```
  plus `lean/FINAL_VALIDATION_REPORT.md` (section 5 below).
- **No `sorry`, no `axiom`, no `admit`, no `native_decide`** in the final files. If a target
  cannot be closed, leave it out of `ProofInterface.lean`, list it in the report as
  *open*, and explain what is missing.
- Every economic hypothesis must appear **visibly in the theorem signature or in a named
  structure** in `Assumptions.lean`. No hypothesis may already contain the conclusion.
- Use `ℝ` and Mathlib's `Real.exp`, `Real.sqrt`, `Real.rpow` (`x ^ (p : ℝ)`), `Real.pi`.
  Name variables after the paper: `X`, `tauA`, `lamI`, `lamG`, `I`, `Sigma2`, `sigInv2`,
  `eps`, `DeltaX`, `DeltaI`.
- Prefer statements that avoid heavy measure theory: we treat `G` either concretely
  through `g`, or abstractly through the hypotheses `HasDerivAt G (g τ) τ`, `g > 0`,
  `g` strictly antitone.

## 3. Targets (do them in this order)

### T1 — the substitution engine: `g` is positive and strictly decreasing  *(concrete, easy)*
Define `gAKO (τ : ℝ) : ℝ := (Real.sqrt (2 * Real.pi))⁻¹ * τ ^ (-(1/2 : ℝ)) * Real.exp (-τ / 2)`.
Prove:
- `∀ τ > 0, 0 < gAKO τ`;
- `StrictAntiOn gAKO (Set.Ioi 0)`.

*(Hint: product of two positive strictly antitone functions on `Ioi 0`; `rpow` with a
negative exponent is strictly antitone on the positive reals.)*
**Stretch T1b:** prove `HasDerivAt (fun τ => 2 * Φ (Real.sqrt τ) - 1) (gAKO τ) τ` for `τ > 0`,
with Φ the standard Normal CDF from Mathlib, if Mathlib's Gaussian API makes it feasible.
If not, say so and keep `G` abstract.

### T2 — Observation 1 (the two cross-partial signs)  *(abstract, medium)*
Hypotheses: `G g : ℝ → ℝ`, `∀ τ > 0, HasDerivAt G (g τ) τ`, `∀ τ > 0, 0 < g τ`,
`∀ τ > 0, HasDerivAt g (g' τ) τ` with `g' τ < 0`, plus `0 < DeltaX`, `0 < lamI`, `0 < sigInv2`,
`0 ≤ tauA`, `0 ≤ e`. Define the marginal payoff
`MB (e X tauA : ℝ) := DeltaX * G X * lamI * g (sigInv2 + lamI * e + tauA)`.
Prove **both** forms:

- *(a) derivative form.*
  `HasDerivAt (fun X => MB e X tauA) (DeltaX * g X * lamI * g (sigInv2 + lamI*e + tauA)) X`
  and that this value is `> 0` for `X > 0`;
  `HasDerivAt (fun t => MB e X t) (DeltaX * G X * lamI * g' (sigInv2 + lamI*e + t)) tauA`
  and that this value is `< 0` when `G X > 0`.
- *(b) increasing-differences form (what Topkis needs).* For `0 < X < X'`:
  `MB e X tauA < MB e X' tauA`; for `tauA < tauA'` and `G X > 0`: `MB e X tauA' < MB e X tauA`.

**Variant T2′ (our extension, Δ_I > 0).** Replace `DeltaX * G X` by `DeltaI + DeltaX * G X`
with `0 < DeltaI`. Show that (a) and (b) still hold, and that the τ_A-sign now holds **at
X = 0 too**.

### T3 — Observation 2 (monotone best response)  *(abstract order argument, medium)*
State and prove a general lemma, then instantiate it twice.

*General lemma.* Let `MB : ℝ → ℝ → ℝ` (effort, parameter) be antitone in effort for each
parameter, and `MC : ℝ → ℝ` strictly monotone on `[0, ∞)`. Let `e₁, e₂ ≥ 0` satisfy
`MB e₁ θ₁ = MC e₁` and `MB e₂ θ₂ = MC e₂`. If `∀ e ≥ 0, MB e θ₁ < MB e θ₂`, then `e₁ < e₂`.

*Proof sketch to check:* if `e₂ ≤ e₁`, then
`MC e₂ = MB e₂ θ₂ > MB e₂ θ₁ ≥ MB e₁ θ₁ = MC e₁ ≥ MC e₂`, a contradiction.

*Instantiations.* With `MC e = e ^ (1/eps)` (`eps > 0`) and MB from T2, conclude:
(i) best-response effort is strictly increasing in X on `X > 0`;
(ii) best-response effort is strictly decreasing in τ_A when `X > 0`.
**Stretch T3b:** existence and uniqueness of the FOC root for `X > 0` (IVT plus strict
monotonicity), under the extra hypotheses `g τ → 0` as `τ → ∞` and `g` continuous on
`Ioi 0`.

### T4 — the maintenance-effort equivalence  *(pure algebra, easy; the bridge to Lemma 2)*
For `0 < Sigma2`, `0 < X`, `Sigma2 * X < 1`, `0 < lamG`, `0 < I`, `0 ≤ e`, with
`z := X + lamG * I * e`, prove:
- the identity `(Sigma2 + z⁻¹)⁻¹ - X = lamG * I * (1 - Sigma2 * X) * (e - eM X) / (1 + Sigma2 * z)`,
  where `eM X := Sigma2 * X ^ 2 / (lamG * I * (1 - Sigma2 * X))`;
- the corollary `X < (Sigma2 + z⁻¹)⁻¹ ↔ eM X < e`;
- and, for `Sigma2 * X ≥ 1`: `(Sigma2 + z⁻¹)⁻¹ < X`.

### T5 — Lemma 2, local stability of collapse  *(real analysis, harder — the main prize)*
Keep the best response abstract: `eBR : ℝ → ℝ` with `eBR X ≥ 0`, and
`F X := (Sigma2 + (X + lamG * I * eBR X)⁻¹)⁻¹`.

- **(stable, ε > 4)** If `∃ C > 0, ∃ δ > 0, ∀ X ∈ Ioo 0 δ, eBR X ≤ C * X ^ p` with `p > 2`
  (in the paper `p = ε/2`), then `∃ δ' > 0, ∀ X ∈ Ioo 0 δ', F X < X`.
- **(unstable, ε < 4)** If `∃ c > 0, ∃ δ > 0, ∀ X ∈ Ioo 0 δ, c * X ^ p ≤ eBR X` with `p < 2`,
  then `∃ δ' > 0, ∀ X ∈ Ioo 0 δ', X < F X`.

Use T4 and the fact that `X ^ (p - 2) → 0` (respectively `→ ∞`) as `X → 0⁺`.
**Do not formalize `ε = 4`**: it is a knife-edge case that depends on constants.

### T6 — what Δ_I > 0 breaks  *(easy, our extension)*
If `eBR 0 > 0` (true when Δ_I > 0), then `F 0 > 0`, so `X = 0` is **not** a fixed point:
complete knowledge collapse is impossible for every finite τ_A.

## 4. Where to be skeptical (please check, do not trust)

1. The paper (p. 15) defines the best response as the unique solution of the FOC,
   `e(X, τ_A) := {e ≥ 0 | Δ_X G(X) λ_I g(σ⁻² + λ_I e + τ_A) = e^{1/ε}}`. An earlier machine
   extraction wrote it as the `argmax` of the *marginal* payoff, which is wrong. Use the
   FOC-root definition, and if you do T3b, prove it coincides with the argmax of
   `Δ_X G(X) G(σ⁻² + λ_I e + τ_A) − (ε/(ε+1)) e^{(ε+1)/ε}`.
2. Observation 2 in the paper says “increasing/decreasing, strictly so for X > 0”. At X = 0
   the best response is 0 for every τ_A, so the τ_A-monotonicity is weak there. Make sure your
   statements carry the right strictness.
3. T5 is stated with a one-sided bound on `eBR`, which is all the proof needs. The paper
   states the ε-threshold in terms of the Frisch elasticity; the link `p = ε/2` comes from
   `G(X) ~ √(2X/π)`. That asymptotic is *not* part of T5 — keep the two separate.

## 5. What to hand back

For each target:
1. The **Lean code**, complete and ready to paste, in the file layout of section 2.
2. **One sentence per theorem saying what it proves in economic terms** (English).
3. A **fidelity note**: does the Lean statement match the paper exactly, or is it
   stronger, weaker, or different? List every added hypothesis.

At the end, a `FINAL_VALIDATION_REPORT.md` with:
- the source version (MIT author version, 5 May 2026);
- a table: *Target | Paper result | Lean name | Status (proved / open) | Deviations*;
- the list of every hypothesis in `Assumptions.lean`, tagged *source-backed* or
  *added for the formalization*;
- any error you found in the paper or in Claude's derivations.

## 6. Local workflow (for Alejandro)

```bash
# one-time setup (Windows: install elan from https://github.com/leanprover/elan, then VS Code + "Lean 4" extension)
cd lean
lake update            # resolves Mathlib at the pinned tag
lake exe cache get     # downloads pre-built Mathlib (several GB; do this once)
lake build             # compiles our files — paste the full output back to ChatGPT if it fails
```

Commit convention for this folder: `feat(lean): ...` for new statements or proofs,
`fix(lean): ...` for repairs, `docs(lean): ...` for the validation report.
