import AKO26KnowledgeCollapse.PaperInterface

/-!
# Verified paper-facing results
-/

namespace AKO26KnowledgeCollapse

/-- T1 holds for the concrete Gaussian marginal-accuracy function. -/
theorem t1SubstitutionEngine_holds : t1SubstitutionEngineSpec := by
  constructor
  · intro tau htau
    unfold gAKO
    have hsqrt : 0 < Real.sqrt (2 * Real.pi) := by
      exact Real.sqrt_pos.2 (mul_pos (by norm_num) Real.pi_pos)
    exact mul_pos
      (mul_pos (inv_pos.mpr hsqrt) (Real.rpow_pos_of_pos htau _))
      (Real.exp_pos _)
  · intro a ha b _ hab
    unfold gAKO
    have hsqrt : 0 < Real.sqrt (2 * Real.pi) := by
      exact Real.sqrt_pos.2 (mul_pos (by norm_num) Real.pi_pos)
    have hconstant : 0 < (Real.sqrt (2 * Real.pi))⁻¹ := inv_pos.mpr hsqrt
    have hrpow : b ^ (-(1 / 2 : ℝ)) < a ^ (-(1 / 2 : ℝ)) := by
      exact Real.rpow_lt_rpow_of_neg ha hab (by norm_num)
    have hexp : Real.exp (-b / 2) < Real.exp (-a / 2) := by
      apply Real.exp_lt_exp.mpr
      linarith
    calc
      (Real.sqrt (2 * Real.pi))⁻¹ * b ^ (-(1 / 2 : ℝ)) * Real.exp (-b / 2) <
          (Real.sqrt (2 * Real.pi))⁻¹ * a ^ (-(1 / 2 : ℝ)) * Real.exp (-b / 2) := by
            exact mul_lt_mul_of_pos_right
              (mul_lt_mul_of_pos_left hrpow hconstant) (Real.exp_pos _)
      _ < (Real.sqrt (2 * Real.pi))⁻¹ * a ^ (-(1 / 2 : ℝ)) * Real.exp (-a / 2) := by
            exact mul_lt_mul_of_pos_left hexp
              (mul_pos hconstant (Real.rpow_pos_of_pos ha _))

private lemma accuracy_strictMonoOn
    {G g gPrime : ℝ → ℝ} (h : AccuracyAssumptions G g gPrime) :
    StrictMonoOn G (Set.Ioi 0) := by
  apply strictMonoOn_of_deriv_pos (convex_Ioi 0)
  · intro x hx
    exact (h.hasDerivAt_G x hx).continuousAt.continuousWithinAt
  · intro x hx
    have hx' : 0 < x := by simpa using hx
    rw [(h.hasDerivAt_G x hx').deriv]
    exact h.g_pos x hx'

private lemma marginalAccuracy_strictAntiOn
    {G g gPrime : ℝ → ℝ} (h : AccuracyAssumptions G g gPrime) :
    StrictAntiOn g (Set.Ioi 0) := by
  apply strictAntiOn_of_deriv_neg (convex_Ioi 0)
  · intro x hx
    exact (h.hasDerivAt_g x hx).continuousAt.continuousWithinAt
  · intro x hx
    have hx' : 0 < x := by simpa using hx
    rw [(h.hasDerivAt_g x hx').deriv]
    exact h.gPrime_neg x hx'

/-- T2 holds under the paper's abstract analytic and economic assumptions. -/
theorem t2ObservationOne_holds : t2ObservationOneSpec := by
  intro G g gPrime h DeltaX lamI sigInv2 effort tauA
    hDeltaX hLamI hSigInv2 hEffort hTauA
  have hY : 0 < idiosyncraticPrecision sigInv2 lamI effort tauA := by
    unfold idiosyncraticPrecision
    have hLearning : 0 ≤ lamI * effort := mul_nonneg hLamI.le hEffort
    linarith
  have hInner :
      HasDerivAt
        (fun t : ℝ ↦ idiosyncraticPrecision sigInv2 lamI effort t) 1 tauA := by
    simpa [idiosyncraticPrecision] using
      (hasDerivAt_id tauA).const_add (sigInv2 + lamI * effort)
  have hMarginalComposition :
      HasDerivAt
        (fun t : ℝ ↦ g (idiosyncraticPrecision sigInv2 lamI effort t))
        (gPrime (idiosyncraticPrecision sigInv2 lamI effort tauA)) tauA := by
    simpa using
      (h.hasDerivAt_g
        (idiosyncraticPrecision sigInv2 lamI effort tauA) hY).comp tauA hInner
  have hGMono : StrictMonoOn G (Set.Ioi 0) := accuracy_strictMonoOn h
  have hgAnti : StrictAntiOn g (Set.Ioi 0) := marginalAccuracy_strictAntiOn h
  constructor
  · refine
      { crossPartialX := ?_
        crossPartialTauA := ?_
        increasingDifferencesX := ?_
        decreasingDifferencesTauA := ?_ }
    · intro X hX
      constructor
      · simpa [marginalBenefitBaseline] using
          (((h.hasDerivAt_G X hX).const_mul DeltaX).mul_const lamI).mul_const
            (g (idiosyncraticPrecision sigInv2 lamI effort tauA))
      · exact mul_pos
          (mul_pos (mul_pos hDeltaX (h.g_pos X hX)) hLamI)
          (h.g_pos (idiosyncraticPrecision sigInv2 lamI effort tauA) hY)
    · intro X hGX
      constructor
      · simpa [marginalBenefitBaseline] using
          hMarginalComposition.const_mul (DeltaX * G X * lamI)
      · exact mul_neg_of_pos_of_neg
          (mul_pos (mul_pos hDeltaX hGX) hLamI)
          (h.gPrime_neg (idiosyncraticPrecision sigInv2 lamI effort tauA) hY)
    · intro X X' hX hXX'
      have hX' : 0 < X' := lt_trans hX hXX'
      have hGXX' : G X < G X' := hGMono hX hX' hXX'
      have hFactor :
          0 < DeltaX * lamI *
            g (idiosyncraticPrecision sigInv2 lamI effort tauA) :=
        mul_pos (mul_pos hDeltaX hLamI)
          (h.g_pos (idiosyncraticPrecision sigInv2 lamI effort tauA) hY)
      calc
        marginalBenefitBaseline G g DeltaX lamI sigInv2 effort X tauA =
            G X * (DeltaX * lamI *
              g (idiosyncraticPrecision sigInv2 lamI effort tauA)) := by
                unfold marginalBenefitBaseline
                ring
        _ < G X' * (DeltaX * lamI *
              g (idiosyncraticPrecision sigInv2 lamI effort tauA)) :=
            mul_lt_mul_of_pos_right hGXX' hFactor
        _ = marginalBenefitBaseline G g DeltaX lamI sigInv2 effort X' tauA := by
              unfold marginalBenefitBaseline
              ring
    · intro X tauA' hGX hTauLt
      have hTauA' : 0 ≤ tauA' := hTauA.trans (le_of_lt hTauLt)
      have hY' : 0 < idiosyncraticPrecision sigInv2 lamI effort tauA' := by
        unfold idiosyncraticPrecision
        have hLearning : 0 ≤ lamI * effort := mul_nonneg hLamI.le hEffort
        linarith
      have hYY' :
          idiosyncraticPrecision sigInv2 lamI effort tauA <
            idiosyncraticPrecision sigInv2 lamI effort tauA' := by
        unfold idiosyncraticPrecision
        linarith
      have hgYY' :
          g (idiosyncraticPrecision sigInv2 lamI effort tauA') <
            g (idiosyncraticPrecision sigInv2 lamI effort tauA) :=
        hgAnti hY hY' hYY'
      have hFactor : 0 < DeltaX * G X * lamI :=
        mul_pos (mul_pos hDeltaX hGX) hLamI
      exact mul_lt_mul_of_pos_left hgYY' hFactor
  · intro DeltaI hDeltaI
    have hStandaloneTau :
        ∀ X : ℝ, 0 ≤ G X →
          HasDerivAt
              (fun t ↦ marginalBenefitWithStandaloneValue
                G g DeltaI DeltaX lamI sigInv2 effort X t)
              ((DeltaI + DeltaX * G X) * lamI *
                gPrime (idiosyncraticPrecision sigInv2 lamI effort tauA)) tauA ∧
            (DeltaI + DeltaX * G X) * lamI *
              gPrime (idiosyncraticPrecision sigInv2 lamI effort tauA) < 0 := by
      intro X hGX
      have hBracket : 0 < DeltaI + DeltaX * G X :=
        add_pos_of_pos_of_nonneg hDeltaI (mul_nonneg hDeltaX.le hGX)
      constructor
      · simpa [marginalBenefitWithStandaloneValue] using
          hMarginalComposition.const_mul ((DeltaI + DeltaX * G X) * lamI)
      · exact mul_neg_of_pos_of_neg (mul_pos hBracket hLamI)
          (h.gPrime_neg (idiosyncraticPrecision sigInv2 lamI effort tauA) hY)
    have hStandaloneTauDifferences :
        ∀ X tauA' : ℝ, 0 ≤ G X → tauA < tauA' →
          marginalBenefitWithStandaloneValue
              G g DeltaI DeltaX lamI sigInv2 effort X tauA' <
            marginalBenefitWithStandaloneValue
              G g DeltaI DeltaX lamI sigInv2 effort X tauA := by
      intro X tauA' hGX hTauLt
      have hTauA' : 0 ≤ tauA' := hTauA.trans (le_of_lt hTauLt)
      have hY' : 0 < idiosyncraticPrecision sigInv2 lamI effort tauA' := by
        unfold idiosyncraticPrecision
        have hLearning : 0 ≤ lamI * effort := mul_nonneg hLamI.le hEffort
        linarith
      have hYY' :
          idiosyncraticPrecision sigInv2 lamI effort tauA <
            idiosyncraticPrecision sigInv2 lamI effort tauA' := by
        unfold idiosyncraticPrecision
        linarith
      have hgYY' :
          g (idiosyncraticPrecision sigInv2 lamI effort tauA') <
            g (idiosyncraticPrecision sigInv2 lamI effort tauA) :=
        hgAnti hY hY' hYY'
      have hBracket : 0 < DeltaI + DeltaX * G X :=
        add_pos_of_pos_of_nonneg hDeltaI (mul_nonneg hDeltaX.le hGX)
      exact mul_lt_mul_of_pos_left hgYY' (mul_pos hBracket hLamI)
    refine
      { crossPartialX := ?_
        crossPartialTauA := hStandaloneTau
        crossPartialTauAAtZero := ?_
        increasingDifferencesX := ?_
        decreasingDifferencesTauA := hStandaloneTauDifferences
        decreasingDifferencesTauAAtZero := ?_ }
    · intro X hX
      constructor
      · simpa [marginalBenefitWithStandaloneValue] using
          (((((h.hasDerivAt_G X hX).const_mul DeltaX).const_add DeltaI).mul_const lamI).mul_const
            (g (idiosyncraticPrecision sigInv2 lamI effort tauA)))
      · exact mul_pos
          (mul_pos (mul_pos hDeltaX (h.g_pos X hX)) hLamI)
          (h.g_pos (idiosyncraticPrecision sigInv2 lamI effort tauA) hY)
    · have hGZeroNonneg : 0 ≤ G 0 := by rw [h.G_zero]
      exact hStandaloneTau 0 hGZeroNonneg
    · intro X X' hX hXX'
      have hX' : 0 < X' := lt_trans hX hXX'
      have hGXX' : G X < G X' := hGMono hX hX' hXX'
      have hBracket : DeltaI + DeltaX * G X < DeltaI + DeltaX * G X' :=
        by
          simpa [add_comm] using
            (add_lt_add_left (mul_lt_mul_of_pos_left hGXX' hDeltaX) DeltaI)
      have hFactor :
          0 < lamI * g (idiosyncraticPrecision sigInv2 lamI effort tauA) :=
        mul_pos hLamI
          (h.g_pos (idiosyncraticPrecision sigInv2 lamI effort tauA) hY)
      calc
        marginalBenefitWithStandaloneValue
            G g DeltaI DeltaX lamI sigInv2 effort X tauA =
          (DeltaI + DeltaX * G X) *
            (lamI * g (idiosyncraticPrecision sigInv2 lamI effort tauA)) := by
              unfold marginalBenefitWithStandaloneValue
              ring
        _ < (DeltaI + DeltaX * G X') *
            (lamI * g (idiosyncraticPrecision sigInv2 lamI effort tauA)) :=
          mul_lt_mul_of_pos_right hBracket hFactor
        _ = marginalBenefitWithStandaloneValue
            G g DeltaI DeltaX lamI sigInv2 effort X' tauA := by
              unfold marginalBenefitWithStandaloneValue
              ring
    · intro tauA' hTauLt
      have hGZeroNonneg : 0 ≤ G 0 := by rw [h.G_zero]
      exact hStandaloneTauDifferences 0 tauA' hGZeroNonneg hTauLt

end AKO26KnowledgeCollapse
