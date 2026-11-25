"""Run the pinned upstream intake using our own earlier, CI-checked Lean proofs.
No independent semantic-review or closure verdict is fabricated.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
from argparse import Namespace
from pathlib import Path

ROOT = Path(os.environ["GITHUB_WORKSPACE"])
UP = ROOT / "upstream-aml"
EVIDENCE = ROOT / "aml-evidence"
TEMP = Path(os.environ["RUNNER_TEMP"])
PDF = TEMP / "AKO26-MIT-2026-05-05.pdf"
PAPER = "AKO26KnowledgeCollapse"
VERSION = "MIT author version, May 5, 2026 (69 pages); NBER WP 34910"
SOURCE = "https://economics.mit.edu/sites/default/files/2026-05/AI,%20Human%20Cognition%20and%20Knowledge%20Collapse%2005-05-26.pdf"
BASELINE = "4ab2975b14e0fb2a776bda9e5dc04ba798645b00"
DIGEST = hashlib.sha256(PDF.read_bytes()).hexdigest()
# The upstream facade starts child Python processes from its root. Preserve
# the root on their import path; the first run exposed its absence.
os.environ["PYTHONPATH"] = str(UP) + os.pathsep + os.environ.get("PYTHONPATH", "")
sys.path.insert(0, str(UP))

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
    "--pdf-url", SOURCE, "--no-download"], "scaffold.log")
if status:
    raise SystemExit(status)

folder = UP / "papers" / PAPER

# Use the official contributor facade for the initial scaffold, then the
# pinned upstream generator's rendering functions for the source-pinned
# draft. This avoids rebuilding the entire library merely to elaborate a
# one-theorem starter. The actual generated statement and proof are checked
# below by the official scoped check and the full paper target build.
from scripts import new_paper as generator

draft = generator.load_statement_spec(spec)
args = Namespace(
    title="AI, Human Cognition and Knowledge Collapse",
    authors="Daron Acemoglu, Dingwen Kong, Asuman Ozdaglar",
    version=VERSION, official_url="https://www.nber.org/papers/w34910",
    pdf_url=SOURCE, url=SOURCE, folder=PAPER, namespace=PAPER,
)
audit_source = folder / generator.audited_source_filename(PDF)
shutil.copyfile(PDF, audit_source)
if hashlib.sha256(audit_source.read_bytes()).hexdigest() != DIGEST:
    raise RuntimeError("Source bytes changed during copy")
generator.extract_text(audit_source, folder / "source.txt", True)
source_rel = str(audit_source.relative_to(UP))
def write_generated(rel, value):
    (folder / rel).write_text(value, encoding="utf-8")
write_generated("PaperInterface.lean",
    generator.paper_interface_text(args.title, PAPER, PAPER, draft.targets))
write_generated("ProofInterface.lean",
    generator.proof_interface_text(args.title, PAPER, PAPER, draft.targets))
write_generated("status.json", generator.status_text(args, PAPER, draft.targets))
write_generated("audit/paper_statement_map.json",
    generator.paper_statement_map_text(args, PAPER, draft, source_rel))
write_generated("audit/v11_source_map_preparation_config.json",
    generator.source_inventory_review_config_text(PAPER, draft, PAPER))
write_generated("audit/source_proof_fidelity.json",
    generator.source_proof_fidelity_text(PAPER, source_rel, DIGEST))
# These are generator-produced drafts, NOT validated semantic judgments.
# All reviews, source inventory decisions and closeout receipts remain open.

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
  verified in Actions run 45551690557; no other student's run is used.
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
    a.write_text("import AKO26KnowledgeCollapse\n#print axioms AKO26KnowledgeCollapse.observationOne\n#print axioms AKO26KnowledgeCollapse.t1SubstitutionEngine_holds\n#print axioms AKO26KnowledgeCollapse.t2ObservationOne_holds\n#print axioms AKO26KnowledgeCollapse.t3ObservationTwoRoot_holds\n#print axioms AKO26KnowledgeCollapse.t4Maintenance_holds\n#print axioms AKO26KnowledgeCollapse.t6PositiveEffortAtZero_holds\n#print axioms AKO26KnowledgeCollapse.t7PlannerValue_holds\n")
    axioms = run_log(["lake", "env", "lean", str(a)], "axioms.log")
    log = (EVIDENCE / "axioms.log").read_text()
    if "sorryAx" in log:
        axioms = 1
results = f"paper_contribution_check_fast={fast}\nfocused_root_build={build}\naxioms_command={axioms}\n"
# Retain a truthful status for the actual result. No semantic or human review
# is marked complete; a successful build of the partial target is not full
# source coverage.
status_path = folder / "status.json"
payload = json.loads(status_path.read_text())
payload["status"] = "partially formalized" if build == 0 and axioms == 0 else "not formalized"
payload["main_caveat"] = ("Observation 1 is represented by derivatives of the displayed "
    "marginal payoff under explicit analytic premises; the concrete Gaussian CDF, "
    "utility-to-marginal-payoff bridge, and independent semantic review remain open.")
payload["human_summary"] = ("Own course intake; static marginal-benefit identities and "
    "related helper proofs. Full paper coverage is not claimed.")
status_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
sync = run_log(["python3", "scripts/sync_paper_status.py", "--paper", PAPER], "status-sync.log")
print(f"status_sync_exit_code={sync}")
(EVIDENCE / "check-exit-codes.txt").write_text(results)
(folder / "docs" / "CHECK_EXIT_CODES.txt").write_text(results)
with (folder / "docs" / "FORMALIZATION_WORKING_MEMO.md").open("a", encoding="utf-8") as f:
    f.write("\n## Actual execution results\n\n" + results +
            "\nCI run: " + os.environ["GITHUB_RUN_ID"] +
            "\nThis focused check is not independent semantic approval.\n")
raise SystemExit(0 if fast == build == axioms == 0 else 1)
