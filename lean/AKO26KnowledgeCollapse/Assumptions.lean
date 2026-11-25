import Mathlib

/-!
# Economic assumptions

Target T1 is an unconditional analytic statement, so it requires no economic assumptions.
-/

namespace AKO26KnowledgeCollapse

/-- Analytic assumptions on the abstract accuracy function used in T2. -/
structure AccuracyAssumptions (G g gPrime : ℝ → ℝ) : Prop where
  /-- Zero precision gives zero probability of an accurate prediction. -/
  G_zero : G 0 = 0
  /-- On positive precisions, `g` is the derivative of the accuracy function `G`. -/
  hasDerivAt_G : ∀ tau : ℝ, 0 < tau → HasDerivAt G (g tau) tau
  /-- The marginal accuracy gain is positive at every positive precision. -/
  g_pos : ∀ tau : ℝ, 0 < tau → 0 < g tau
  /-- On positive precisions, `gPrime` is the derivative of `g`. -/
  hasDerivAt_g : ∀ tau : ℝ, 0 < tau → HasDerivAt g (gPrime tau) tau
  /-- The derivative of marginal accuracy is negative at every positive precision. -/
  gPrime_neg : ∀ tau : ℝ, 0 < tau → gPrime tau < 0

end AKO26KnowledgeCollapse
