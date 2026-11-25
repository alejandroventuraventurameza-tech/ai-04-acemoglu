# AKO26KnowledgeCollapse — validation report (partial)

**Source:** Acemoglu, Kong & Ozdaglar, *AI, Human Cognition and Knowledge Collapse*, MIT author version dated May 5, 2026, NBER WP 34910. The standalone Lean project is the student's own work. It is not yet the complete official AppliedModelingLib generated paper folder.

## Checked baseline

- Commit: `e5ec1ac4873c589c1ed246870d790ed66afc97d5` (PR #1).
- [GitHub Actions run 45548281818](https://github.com/alejandroventuraventurameza-tech/ai-04-acemoglu/actions/runs/45548281818), Lean job [138983050872](https://github.com/alejandroventuraventurameza-tech/ai-04-acemoglu/actions/runs/45548281818/job/138983050872): **Build completed successfully (8317 jobs)**. Axiom audit: **47 declarations**, all within `propext, Classical.choice, Quot.sound`.
- [Numerical job 138983050832](https://github.com/alejandroventuraventurameza-tech/ai-04-acemoglu/actions/runs/45548281818/job/138983050832): all static-block assertions passed; all eight figures reproduced. These computations do not prove global dynamic results.
- Beamer job failed because `\\note` was already defined. The conflict was repaired and the next Beamer build (run 45551232138) produced an 18-page PDF. That build reported a small vertical overflow in the Lean slide, now shortened. The same run stopped on two definitions involving noncomputable real division; both have been marked `noncomputable`. Run [45551457600](https://github.com/alejandroventuraventurameza-tech/ai-04-acemoglu/actions/runs/45551457600) produced the clean 18-page deck without overflow, and the updated Lean interface compiled. The proof file reported two unresolved benefit-function metavariables and a rewrite ambiguity in T4. Explicit MB1/MB2 and an explicitly instantiated distributivity rewrite repair these errors; the amended proof code requires a new build.

## Checked expanded project

- [Successful run 45551690557](https://github.com/alejandroventuraventurameza-tech/ai-04-acemoglu/actions/runs/45551690557), source commit `4ab2975b14e0fb2a776bda9e5dc04ba798645b00`.
- [Lean job 138994101386](https://github.com/alejandroventuraventurameza-tech/ai-04-acemoglu/actions/runs/45551690557/job/138994101386): `Build completed successfully (8317 jobs).` The axiom audit examined **64 declarations**, all within `propext, Classical.choice, Quot.sound`. No nonstandard axiom or proof placeholder was accepted. The only recorded Lean diagnostic was a redundant tactic-sequencing linter warning; it is not a mathematical error.
- SymPy assertions and all eight numerical figures passed. The Beamer build produced 18 pages without an overfull-box warning, and the publish job committed the generated PDF at `9d98a5be466f604f2e59e09e1e3f680eb0a0042d`.
- The build certifies the stated Lean propositions, not the unresolved links to the full Gaussian model. The official AppliedModelingLib contribution is an independent requirement.

## Target ledger

| Target | Endpoint | Scope | Status |
|---|---|---|---|
| T1 | `t1SubstitutionEngine_holds` | Concrete Gaussian marginal accuracy positive and strictly decreasing on positive precision | Checked at baseline |
| T2 | `t2ObservationOne_holds` | Derivatives of marginal benefit and differences for baseline and standalone-value extension, under explicit accuracy assumptions | Checked at baseline; Gaussian CDF bridge and utility derivative not yet discharged inside Lean |
| T3 | `t3ObservationTwoRoot_holds` | Strict order of existing nonnegative FOC roots; positivity of G explicit | Checked in run 45551690557 |
| T4 | `t4Maintenance_holds` | Factorization and maintenance inequality on the positive precision domain | Checked in run 45551690557 |
| T5 | — | Power-law bound leading to the Frisch threshold | Open; source dynamics read-only in course issue |
| T6 | `t6PositiveEffortAtZero_holds` | Positive effort at zero implies positive next precision; does not establish effort optimality | Checked in run 45551690557 |
| T7 | `t7PlannerValue_holds` | Abstract monotonicity of finite supremum under common feasible paths and pathwise monotone welfare | Checked in run 45551690557; economic specialization open |
| T8 | — | Fixed point existence for standalone contextual value | Open |

## Assumptions and source fidelity

- The source's Gaussian accuracy provides the motivation for G, g and gPrime. `AccuracyAssumptions` explicitly assumes G(0)=0, HasDerivAt G g at positive precisions, g>0, HasDerivAt g gPrime and gPrime<0. T1 alone does not discharge all of these properties. Without a boundary continuity or positivity assumption, G(0)=0 and positive derivative on (0,infinity) do not imply G(X)>0 there. T2/T3 therefore state the relevant positivity premise explicitly.
- T3 uses the increasing/decreasing shifts from T2, antitone marginal benefit in effort and monotone marginal cost. Existence, interiority and equivalence of the FOC root with a utility maximizer remain separate mathematical obligations.
- T4 and T6 define public precision by the rational transition z/(1+Sigma2*z), with z=X+K*e and K=lambda_G I. This agrees with the inverse formula for z>0 and extends continuously at z=0. Lean's total inverse maps 0 to 0, so a direct inverse-of-inverse expression would give 1/Sigma2 at z=0, an incorrect economic boundary. No desired conclusion is inserted as an assumption.
- T7 is a general order lemma with nonempty feasible paths and a finite supremum. It is not an independent proof of the planner's dynamic feasibility or Blackwell ordering in the source economy.
- The manuscript plan contains the missing handwritten verification of Observation 1 and partial crowding-out. The authentic handwritten artifact remains pending.

## AppliedModelingLib contribution gate

The course explicitly requires the complete **own-generated** `papers/AKO26KnowledgeCollapse/` folder and the actual result of `python3 scripts/paper_contribution.py check AKO26KnowledgeCollapse --fast`. Standalone CI success does not fulfill that gate. The pinned upstream commit used for the separate official intake is `194edcc95df74806a39b961d10dedddc6e730cce` of [AppliedModelingLib](https://github.com/nikhgarg/AppliedModelingLib). The separate [official intake run 45551762272](https://github.com/alejandroventuraventurameza-tech/ai-04-acemoglu/actions/runs/45551762272) was launched from `work/aml-intake`. Its final result is not claimed here. No semantic review, generated status or audit is represented as completed unless produced by the official workflow.

## Subsequent official run (25 November 2026)

The separate official intake completed successfully in run 45554882759. See ../aml-evidence/README.md for the actual official check, proof build, axiom output, and verified generated-folder import. This standalone report is retained as historical evidence, not an official generated audit file.
