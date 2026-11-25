import AKO26KnowledgeCollapse.MainTheorems
import AKO26KnowledgeCollapse.Assumptions

/-!
# Human-Facing Paper Interface: AI, Human Cognition and Knowledge Collapse

This is the compact Lean file a human should read after formalization to check
whether the paper's definitions and named theorem statements were represented
correctly. Keep the row-level dashboard and LLM audit statements in this file
for every paper. Move implementation details, proof aliases, and bulky helper
lemmas behind imported modules such as `AuditInterface.lean`, but expose the
audited paper-facing statements directly here; do not use
`paper_interface.audit_surface_path`.

Rules for completing this file:

- Keep the paper's definitions/formatted objects first, in source order.
- Expose the actual paper formulas here; do not only point to generic library
  definitions or implementation witnesses.
- A material reusable `AppliedModelingLib` primitive may remain a reference here only
  after `audit/library_semantic_review.json` records its exact bounded library
  declaration and an explicit byte-pinned paper-source connection. The
  dashboard and human-review packet show and source-check that declaration
  before the dependent Spec; a library name, docstring, or glossary is not a
  semantic bridge. Do not add a duplicate paper claim merely to restate it.
- If a named theorem needs a hypothesis that is not derived from earlier Lean
  declarations, declare that hypothesis in `Assumptions.lean` and list it in
  `status.json` `review_surface.assumption_names`.
- Then state the named results directly, with assumptions visible in each
  theorem signature by referencing named paper assumptions imported from
  `Assumptions.lean`.
- In the statement-first phase, write every complete source-facing statement as
  a transparent `<name>Spec : Prop` here, exactly once. Put the paired
  theorem/lemma of that exact type in `ProofInterface.lean`; its temporary
  proof body may be `by sorry` only in a private draft. This separation keeps
  the human semantic surface free of thin wrapper declarations.
- Before drafting that Lean surface, independently inventory every material
  source atom from exact pinned source quote bytes. Do not infer source atoms
  from declaration, binder, field, function, or source-map names.
- Run raw-source-to-expanded-Spec statement matching plus Lean-emitted
  premise/conclusion claim-atom review on the skeleton. The semantic comparison uses
  only byte-pinned source quotes (and separately pinned source context) against
  the expanded transparent Spec; map summaries and proof wrappers are not
  semantic inputs. Then freeze each canonical Lean declaration-manifest digest.
- In the proof phase, replace the `ProofInterface.lean` `sorry` with a short
  proof that calls into `MainTheorems.lean` or lower proof files without
  changing the specification or theorem type. Any specification/type change
  invalidates the freeze and requires a fresh statement audit.
- At formalized closeout, complete the v11 realization receipt: Lean Meta checks
  the theorem has exactly the transparent Spec type; each source atom is bound
  to the elaborated Spec surface; closure traversal includes proof and instance
  arguments; and every material terminal has a source, approved correction or
  additional assumption, checked derivation, or version-pinned foundation
  disposition. No data, container, or identifier-based exemption is allowed.
- The transparent `...Spec` is the sole semantic-review target for its source
  claim. The paired theorem/lemma is a proof endpoint whose exact Spec type is
  verified by Lean Meta, not a duplicate source-to-Lean comparison row.
- Keep proof endpoints, exhaustive endpoint aliases, and proof-seam checks in
  `ProofInterface.lean`, implementation modules, or `ProofLedger.lean`, not
  here. Do not create new `PostPaperAudit.lean` or `AuditLedger.lean` files;
  those names are legacy.

## Named Results

Each entry has one semantic-review target (`Spec`) and one proof endpoint (the
paired theorem/lemma). The human dashboard and review packet present that pair
once rather than treating the two declarations as duplicate paper claims.

- `observationOneSpec` -> `observationOne`: Observation 1 (analytic partial formalization), Section 3.4, printed pages 14 and 15; Equation 6.
-/

namespace AKO26KnowledgeCollapse

/--
Observation 1 (analytic partial formalization)

Paper statement: U_eX = Delta_X lambda_I g(X) g(Y) > 0; U_e,tau_A = Delta_X G(X) lambda_I g'(Y) < 0. Y = sigma^(-2) + lambda_I e + tau_A under Assumption 1.

Source location: Section 3.4, printed pages 14 and 15; Equation 6
Source status: pinned statement-spec transcription; independent source audit pending

This transparent proposition is the exact statement-audit target. It is not
proof evidence. Its exact-type proof endpoint is declared in
`ProofInterface.lean`, so this human-facing file presents the full semantic
proposition once. At closeout, source atoms must be independently inventoried
from pinned source quote bytes and bound to this elaborated proposition rather
than inferred from identifiers.
-/
def observationOneSpec : Prop :=
  ∀ (G g gPrime : ℝ → ℝ),
      G 0 = 0 →
      (∀ z : ℝ, 0 < z → HasDerivAt G (g z) z) →
      (∀ z : ℝ, 0 < z → 0 < g z) →
      (∀ z : ℝ, 0 < z → HasDerivAt g (gPrime z) z) →
      (∀ z : ℝ, 0 < z → gPrime z < 0) →
      ∀ (DeltaX lamI sigInv2 eps effort tauA X : ℝ),
        0 < DeltaX → 0 < lamI → 0 < sigInv2 → 0 < eps →
        0 ≤ effort → 0 ≤ tauA → 0 < X → 0 < G X →
        let Y := sigInv2 + lamI * effort + tauA
        (HasDerivAt
          (fun x : ℝ ↦ DeltaX * G x * lamI * g Y - effort ^ (1 / eps))
          (DeltaX * g X * lamI * g Y) X ∧
          0 < DeltaX * g X * lamI * g Y) ∧
        (HasDerivAt
          (fun t : ℝ ↦ DeltaX * G X * lamI *
            g (sigInv2 + lamI * effort + t) - effort ^ (1 / eps))
          (DeltaX * G X * lamI * gPrime Y) tauA ∧
          DeltaX * G X * lamI * gPrime Y < 0)

end AKO26KnowledgeCollapse
