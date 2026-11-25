"""Run the pinned upstream intake using our own earlier, CI-checked Lean proofs.
No independent semantic-review or closure verdict is fabricated.
"""
import hashlib
import json
import os
import subprocess
from pathlib import Path

ROOT = Path(os.environ["GITHUB_WORKSPACE"])
UP = ROOT / "upstream-aml"
EVIDENCE = ROOT / "aml-evidence"
TEMP = Path(os.environ["RUNNER_TEMP"])
PDF = TEMP / "AKO26-MIT-2026-05-05.pdf"
PAPER = "AKO26KnowledgeCollapse"
VERSION = "MIT author version, May 5, 2026 (69 pages); NBER WP 34910"
SOURCE = "https://economics.mit.edu/sites/default/files/2026-05/AI,%20Human%20Cognition%20and%20Knowledge%20Collapse%2005-05-26.pdf"
BASELINE = "e5ec1ac4873c589c1ed246870d790ed66afc97d5"
DIGEST = hashlib.sha256(PDF.read_bytes()).hexdigest()

# Self-contained scaffold target: the two derivatives of the displayed
# marginal payoff. The Gaussian CDF bridge remains a visible proof boundary.
TYPE = """∀ (G g gPrime : ℝ → ℝ),
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
        DeltaX * G X * lamI * gPrime Y < 0)"""
PROOF = """by
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
    · simpa [idiosyncraticPrecision] using hSignTau"""

def run_log(args, filename):
    with (EVIDENCE / filename).open("w", encoding="utf-8") as log:
        proc = subprocess.Popen(args, cwd=UP, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, text=True)
        for line in proc.stdout:
            print(line, end="", flush=True)
            log.write(line)
        return proc.wait()

spec = TEMP / "ako-statement-spec.json"
spec.write_text(json.dumps({
    "schema": 1, "source_artifact_path": str(PDF),
    "source_artifact_sha256": DIGEST, "source_version": VERSION,
    "targets": [{
        "source_item": "Observation 1 (analytic partial formalization)",
        "source_kind": "claim",
        "source_location": "Section 3.4, printed pages 14 and 15; Equation 6",
        "source_statement": "U_eX = Delta_X lambda_I g(X) g(Y) > 0; U_e,tau_A = Delta_X G(X) lambda_I g'(Y) < 0. Y = sigma^(-2) + lambda_I e + tau_A under Assumption 1.",
        "lean_name": "observationOne", "lean_type": TYPE, "kind": "theorem"
    }]
}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
status = run_log(["python3", "scripts/paper_contribution.py", "new", SOURCE,
    "--folder", PAPER, "--title", "AI, Human Cognition and Knowledge Collapse",
    "--authors", "Daron Acemoglu, Dingwen Kong, Asuman Ozdaglar",
    "--version", VERSION, "--official-url", "https://www.nber.org/papers/w34910",
    "--pdf-url", SOURCE, "--statement-spec", str(spec)], "scaffold.log")
if status:
    raise SystemExit(status)

folder = UP / "papers" / PAPER
def old_body(name):
    path = f"lean/{PAPER}/{name}.lean"
    src = subprocess.check_output(["git", "-C", str(ROOT), "show", f"{BASELINE}:{path}"], text=True)
    return src.split(f"namespace {PAPER}\n", 1)[1].rsplit(f"\nend {PAPER}", 1)[0].strip()
helpers = "\n\n".join(old_body(n) for n in ("Assumptions", "PaperInterface", "ProofInterface"))
p = folder / "MainTheorems.lean"
p.write_text(p.read_text().replace(f"\nend {PAPER}", "\n\n" + helpers + f"\n\nend {PAPER}"))
p = folder / "ProofInterface.lean"
generated = p.read_text()
old = "observationOneSpec := by\n  sorry"
if old not in generated:
    raise RuntimeError("Unexpected scaffold proof shape; refuse guessed replacement")
p.write_text(generated.replace(old, "observationOneSpec := " + PROOF))

with (folder / "docs" / "FORMALIZATION_PLAN.md").open("a", encoding="utf-8") as f:
    f.write(f"""
## Repository 4: actual bounded intake
- Exact source: {VERSION}. PDF SHA-256: {DIGEST}.
- Source locations checked: Equation 4 (p. 13), Equation 6 (p. 14),
  Observation 1 (pp. 14–15), best-response FOC (p. 15).
- One named source result is prioritized. The displayed marginal payoff is
  differentiated in X and AI precision with the Gaussian accuracy properties
  assumed explicitly; the exact CDF and utility-to-marginal-payoff bridge
  are open. The other observations, definitions, and dynamic results have
  not received a full source-only inventory and are not claimed as covered.
- Baseline helpers belong to the student's own commit {BASELINE},
  verified in Actions run 45548281818; no other student's run is used.
- The course marks the dynamic sections read-only. The static block is the
  priority. No final source-atom review, independent semantic receipt,
  or human approval is claimed. This is partial, not a closeout.
""")

fast = run_log(["python3", "scripts/paper_contribution.py", "check", PAPER, "--fast"],
               "paper-contribution-check-fast.log")
build = run_log(["lake", "build", "+" + PAPER], "paper-build.log")
axioms = 125
if build == 0:
    a = TEMP / "ako-axioms.lean"
    a.write_text("import AKO26KnowledgeCollapse\n#print axioms AKO26KnowledgeCollapse.observationOne\n#print axioms AKO26KnowledgeCollapse.t1SubstitutionEngine_holds\n#print axioms AKO26KnowledgeCollapse.t2ObservationOne_holds\n")
    axioms = run_log(["lake", "env", "lean", str(a)], "axioms.log")
    if "sorryAx" in (EVIDENCE / "axioms.log").read_text():
        axioms = 1
results = f"paper_contribution_check_fast={fast}\nfocused_root_build={build}\naxioms_command={axioms}\n"
(EVIDENCE / "check-exit-codes.txt").write_text(results)
(folder / "docs" / "CHECK_EXIT_CODES.txt").write_text(results)
with (folder / "docs" / "FORMALIZATION_WORKING_MEMO.md").open("a", encoding="utf-8") as f:
    f.write("\n## Actual execution results\n\n" + results +
            "\nCI run: " + os.environ["GITHUB_RUN_ID"] +
            "\nThis focused check is not independent semantic approval.\n")
raise SystemExit(0 if fast == build == axioms == 0 else 1)
