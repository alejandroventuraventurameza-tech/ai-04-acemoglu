#!/usr/bin/env python3
"""Import the complete tracked paper folder produced by our own upstream CI run.

Requires the downloaded official-ako-intake-evidence artifact directory.
The source archive is never changed; the generated paper folder is copied
without edits. A nonzero official check is retained as evidence, not hidden.
This tool prepares the migration and stages files; it does not commit or push.
"""
import argparse
import hashlib
import json
import re
import shutil
import stat
import subprocess
import tarfile
import tempfile
from pathlib import Path, PurePosixPath

PAPER = "AKO26KnowledgeCollapse"
PREFIX = PurePosixPath("papers") / PAPER
UPSTREAM = "194edcc95df74806a39b961d10dedddc6e730cce"
REQUIRED = {"README.md", "status.json", "PaperInterface.lean",
            "ProofInterface.lean", "MainTheorems.lean", "Assumptions.lean", ".gitignore"}
LOGS = ("generated-file-list.txt", "check-exit-codes.txt",
        "paper-contribution-check-fast.log", "paper-build.log", "axioms.log",
        "source-sha256.txt", "pdfinfo.txt", "scaffold.log", "status-sync.log")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args])


def safe_path(raw):
    p = PurePosixPath(raw)
    if p.is_absolute() or ".." in p.parts or p.parts[:2] != PREFIX.parts:
        raise ValueError(f"Unexpected archive path: {raw}")
    rel = p.relative_to(PREFIX)
    if any(x in {".lake", ".review_traces", "source", "sources", "source_tex",
                 ".audit_source", "source.pdf", "source.txt"} or
           x.startswith("source-audited") for x in rel.parts):
        raise ValueError(f"Source or private cache must not be published: {raw}")
    return rel


def read_codes(path):
    result = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.fullmatch(r"(paper_contribution_check_fast|focused_root_build|axioms_command)=(\d+)", line)
        if not m or m[1] in result:
            raise ValueError(f"Invalid check result line: {line}")
        result[m[1]] = int(m[2])
    if set(result) != {"paper_contribution_check_fast", "focused_root_build", "axioms_command"}:
        raise ValueError("Incomplete recorded check results")
    return result


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--artifact", required=True, type=Path)
    cli.add_argument("--root", default=Path.cwd(), type=Path)
    cli.add_argument("--run-id", required=True, type=int)
    args = cli.parse_args()
    artifact, root = args.artifact.resolve(), args.root.resolve()
    old = root / "lean"
    backup = root / "extra" / "standalone-lean"
    evidence = root / "extra" / "aml-evidence"
    if not (old / "lakefile.toml").is_file() or backup.exists() or evidence.exists():
        raise RuntimeError("Expected original standalone layout; refuse to overwrite an existing import")
    if git(root, "status", "--porcelain"):
        raise RuntimeError("Import requires a clean Git worktree")
    archive = artifact / f"{PAPER}.tar.gz"
    expected = {str(safe_path(line)) for line in
                (artifact / "generated-file-list.txt").read_text(encoding="utf-8").splitlines() if line}
    codes = read_codes(artifact / "check-exit-codes.txt")
    if not REQUIRED.issubset(expected) or not any(p.startswith("audit/") for p in expected) \
       or not any(p.startswith("docs/") for p in expected):
        raise RuntimeError("Generated folder lacks required structure; do not replace the original project")
    if not (artifact / "paper-contribution-check-fast.log").is_file():
        raise RuntimeError("Missing actual official paper-scoped check log")
    source_digest = (artifact / "source-sha256.txt").read_text().split()[0]
    if not re.fullmatch(r"[0-9a-f]{64}", source_digest):
        raise ValueError("Invalid source hash")
    manifest = {}
    with tempfile.TemporaryDirectory() as td:
        extracted = Path(td) / PAPER
        extracted.mkdir()
        with tarfile.open(archive, "r:gz") as tar:
            for member in tar:
                if member.isdir() and PurePosixPath(member.name) == PurePosixPath("papers"):
                    continue
                rel = safe_path(member.name)
                if member.isdir():
                    (extracted / str(rel)).mkdir(parents=True, exist_ok=True)
                    continue
                if not member.isfile() or str(rel) in manifest:
                    raise ValueError(f"Invalid or repeated archive entry: {member.name}")
                data = tar.extractfile(member).read()
                dest = extracted / str(rel)
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(data)
                executable = bool(member.mode & stat.S_IXUSR)
                dest.chmod(0o755 if executable else 0o644)
                manifest[str(rel)] = {"sha256": sha(data), "git_mode": "100755" if executable else "100644"}
        if set(manifest) != expected:
            raise RuntimeError("Archive does not exactly match the upstream tracked file inventory")
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(old), str(backup))
        shutil.copytree(extracted, old, copy_function=shutil.copy2)
    evidence.mkdir()
    for name in LOGS:
        src = artifact / name
        if src.is_file():
            # Root .gitignore excludes *.log; retain exact bytes as .log.txt.
            out_name = name + ".txt" if name.endswith(".log") else name
            shutil.copy2(src, evidence / out_name)
    record = {
        "run_id": args.run_id,
        "upstream_commit": UPSTREAM,
        "paper": PAPER,
        "source_sha256": source_digest,
        "archive_sha256": sha(archive.read_bytes()),
        "checks": codes,
        "evidence_files": {p.name: sha(p.read_bytes()) for p in sorted(evidence.iterdir())},
        "files": manifest,
    }
    (evidence / "import-manifest.json").write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    run_url = f"https://github.com/alejandroventuraventurameza-tech/ai-04-acemoglu/actions/runs/{args.run_id}"
    (evidence / "README.md").write_text(
        "# Official AppliedModelingLib import\n\n"
        f"Own-run evidence: {run_url}\n\n"
        f"Source PDF SHA-256: {source_digest}.\n\n"
        f"Upstream commit: {UPSTREAM}.\n\n"
        f"Official fast check exit code: {codes['paper_contribution_check_fast']}.\n\n"
        f"Focused root build exit code: {codes['focused_root_build']}.\n\n"
        f"Axioms command exit code: {codes['axioms_command']} (125 means not run).\n\n"
        f"The {len(manifest)} tracked generated files were copied into lean/ without "
        "altering any file contents or executable bits. Captured logs use the .log.txt "
        "suffix so ordinary git add preserves them; their bytes are unchanged. "
        "The original standalone project "
        "was retained separately at extra/standalone-lean/. This record does not imply "
        "a complete semantic review or a full-paper proof.\n"
    )
    subprocess.run(["git", "-C", str(root), "add", "-A", "--",
                    "lean", "extra/standalone-lean", "extra/aml-evidence"], check=True)
    staged = git(root, "ls-files", "--stage", "-z", "lean").decode().split("\0")
    actual = {}
    for entry in filter(None, staged):
        meta, path = entry.split("\t", 1)
        mode, _, stage = meta.split()
        if stage != "0":
            raise RuntimeError("Unmerged index entry")
        rel = path.removeprefix("lean/")
        actual[rel] = {"sha256": sha(git(root, "show", ":" + path)), "git_mode": mode}
    if actual != manifest:
        raise RuntimeError("Ordinary git add did not preserve the exact archive; do not force-add ignored files")
    print(f"Verified {len(manifest)} generated files in Git index; official check exit codes: {codes}")
    print("Before committing: update CI's standalone lake-package-directory, README links and slides.")


if __name__ == "__main__":
    main()
