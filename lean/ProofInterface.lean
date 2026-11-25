import AKO26KnowledgeCollapse.PaperInterface

/-!
# Proof Interface: AI, Human Cognition and Knowledge Collapse

This file contains exact-type proof endpoints for the transparent propositions
in `PaperInterface.lean`. It is not a human semantic-review surface: one source
claim is reviewed once, against its expanded `...Spec : Prop` declaration.
-/

namespace AKO26KnowledgeCollapse

/--
Lean proof endpoint for `observationOneSpec`.

This theorem is intentionally outside `PaperInterface.lean`: Lean Meta checks
that it has exactly the transparent Spec type, while source-to-Lean semantic
review compares the raw source bundle only to that Spec.
-/
theorem observationOne :
  observationOneSpec := by
  intro G g gPrime hZero hDG hPos hDg hNeg DeltaX lamI sigInv2 eps
    effort tauA X hDX hLam hSig _ hEff hTau hX hGX
  have h : AccuracyAssumptions G g gPrime :=
    ⟨hZero, hDG, hPos, hDg, hNeg⟩
  have hBase := (t2ObservationOne_holds G g gPrime h DeltaX lamI sigInv2
    effort tauA hDX hLam hSig hEff hTau).1
  obtain ⟨hDerivX, hSignX⟩ := hBase.crossPartialX X hX
  obtain ⟨hDerivTau, hSignTau⟩ := hBase.crossPartialTauA X hGX
  dsimp
  constructor
  · constructor
    · simpa [marginalBenefitBaseline, idiosyncraticPrecision] using
        hDerivX.sub_const (effort ^ (1 / eps))
    · simpa [idiosyncraticPrecision] using hSignX
  · constructor
    · simpa [marginalBenefitBaseline, idiosyncraticPrecision] using
        hDerivTau.sub_const (effort ^ (1 / eps))
    · simpa [idiosyncraticPrecision] using hSignTau

end AKO26KnowledgeCollapse
