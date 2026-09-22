#!/usr/bin/env python3
"""
AETHERZ3OMEGA: SMT TRIBUNAL STRESS-TEST PIPELINE
=================================================
Stress-test SMT-LIB2 rigidity bundles:

  * Original file test      -> negation of each theorem must be UNSAT
  * Premise-consistency     -> premises alone must stay SAT (no vacuous truth)

Two solver backends are supported (auto-selected):
  1. `z3` CLI executable   (when available on PATH)
  2. Python `z3-solver`    (z3py)   (fallback)

Additionally, this tester executes the z3_tribunal/*.py batch scripts that
encode the axiom/identity checks, and reports their VERIFIED markers.

Usage:
    python smt_stress_tester.py [dir-or-file ...]
"""
import os
import re
import sys
import glob
import json
import time
import shutil
import subprocess
import tempfile

SMT_DIR = "./z3_tribunal"
SOLVER_PATH = "z3"
TIMEOUT_MS = 30000
REPO_ROOT = os.path.dirname(os.path.abspath(__file__))


# --------------------------------------------------------------------------
# Solver plumbing
# --------------------------------------------------------------------------

def z3_cli_available():
    try:
        r = subprocess.run([SOLVER_PATH, "-version"], capture_output=True,
                           text=True, encoding="utf-8", errors="replace",
                           timeout=10)
        return r.returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def z3py_available():
    try:
        import z3
        return True, z3.get_version_string()
    except Exception:
        return False, None


def _parse_asserts(text):
    """Return the list of top-level `(assert ...)` S-expressions in `text`."""
    asserts = []
    i, n = 0, len(text)
    depth = 0
    while i < n:
        c = text[i]
        if c == ";":
            j = text.find("\n", i)
            if j == -1:
                break
            i = j + 1
            continue
        if c == "(" and depth == 0 and text.startswith("(assert", i) \
                and (i + 7 == n or text[i + 7] in " \t\n("):
            d = 0
            j = i
            while j < n:
                if text[j] == "(":
                    d += 1
                elif text[j] == ")":
                    d -= 1
                    if d == 0:
                        asserts.append(text[i:j + 1])
                        i = j + 1
                        break
                j += 1
            else:
                break
            continue
        if c == "(":
            depth += 1
        elif c == ")":
            depth = max(0, depth - 1)
        i += 1
    return asserts


def _clean_block(text):
    """Strip comments, (check-sat) / (get-model) / (exit) from a block."""
    out = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith(";"):
            continue
        if re.match(r"\(\s*check-sat\s*\)", stripped):
            continue
        if re.match(r"\(\s*get-model\s*\)", stripped):
            continue
        if re.match(r"\(\s*exit\s*\)", stripped):
            continue
        out.append(line)
    return "\n".join(out)


def check_block(block_text, time_ms=TIMEOUT_MS):
    """Check a cleaned SMT-LIB2 block: returns sat/unsat/unknown/error."""
    text = _clean_block(block_text)
    if not text.strip():
        return "empty"

    # Backend 1: z3 CLI
    if z3_cli_available():
        tmp = None
        try:
            fd, tmp = tempfile.mkstemp(suffix=".smt2")
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                fh.write(text + "\n(check-sat)\n(exit)\n")
            r = subprocess.run([SOLVER_PATH, tmp], capture_output=True,
                               text=True, encoding="utf-8", errors="replace",
                               timeout=max(10, time_ms // 1000))
            return (r.stdout.strip().splitlines() or ["error"])[0]
        except subprocess.TimeoutExpired:
            return "timeout"
        except Exception as exc:
            return f"error:{exc}"
        finally:
            if tmp and os.path.exists(tmp):
                os.remove(tmp)

    # Backend 2: Python z3-solver binding
    try:
        import z3
        exprs = z3.parse_smt2_string(text)
        s = z3.Solver()
        s.set("timeout", time_ms)
        for e in exprs:
            s.add(e)
        return str(s.check())
    except ImportError:
        return "error:no z3 backend available"
    except Exception as exc:
        return f"error:{exc}"


def solver_info():
    if z3_cli_available():
        try:
            r = subprocess.run([SOLVER_PATH, "-version"], capture_output=True,
                               text=True, encoding="utf-8", errors="replace",
                               timeout=10)
            return f"z3-cli ({r.stdout.strip().splitlines()[0]})"
        except Exception:
            return "z3-cli"
    ok, ver = z3py_available()
    if ok:
        return f"z3py (z3-solver {ver})"
    return "NO Z3 SOLVER AVAILABLE"


# --------------------------------------------------------------------------
# Single-file rigidity audit (per theorem block)
# --------------------------------------------------------------------------

def rigid_verdict(full, premises):
    if full == "unsat" and premises == "sat":
        return "RIGID & VALID (No Vacuous Truth)", "PASS"
    if full == "unsat" and premises == "unsat":
        return "CRITICAL FAULT: Vacuous Truth (premises contradictory)", "VACUOUS"
    if full == "sat":
        return f"INVALID: negation satisfiable (premises: {premises})", "FAIL"
    return f"INDETERMINATE (full={full}, premises={premises})", "UNKNOWN"


def audit_smt_file(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        full = fh.read()

    # Split the file into per-theorem blocks between (check-sat) calls.
    parts = re.split(r"\(\s*check-sat\s*\)", full)
    blocks = [b for b in parts if any(
        re.match(r"\(\s*(assert|declare-fun|declare-const)\b", ln.strip())
        for ln in b.splitlines())]

    results = []
    for idx, block in enumerate(blocks):
        full_status = check_block(block)
        assertions = _parse_asserts(block)
        if not assertions:
            premises_status = "sat"
        else:
            # Drop the LAST top-level assert (normally the theorem negation)
            # to test pure premise consistency.
            lowered = block
            last = assertions[-1]
            pos = lowered.rfind(last)
            premises_text = lowered[:pos] + lowered[pos + len(last):]
            premises_status = check_block(premises_text)

        verdict, tag = rigid_verdict(full_status, premises_status)
        results.append({
            "block": idx + 1,
            "assert_count": len(assertions),
            "full_negation": full_status,
            "premises_only": premises_status,
            "verdict": verdict,
            "tag": tag,
        })
    return results


# --------------------------------------------------------------------------
# Discovery
# --------------------------------------------------------------------------

def discover_smt2(roots):
    files = []
    seen = set()
    for root in roots:
        if not os.path.exists(root):
            continue
        if os.path.isfile(root) and root.endswith(".smt2"):
            files.append(os.path.abspath(root))
            continue
        for dirpath, _, names in os.walk(root):
            for name in names:
                if not name.endswith(".smt2"):
                    continue
                fp = os.path.abspath(os.path.join(dirpath, name))
                if fp not in seen:
                    seen.add(fp)
                    files.append(fp)
    return sorted(files)


def discover_batch_scripts(roots):
    scripts = []
    seen = set()
    for root in roots:
        if not os.path.exists(root):
            continue
        if os.path.isfile(root) and root.endswith(".py"):
            scripts.append(os.path.abspath(root))
            continue
        for dirpath, _, names in os.walk(root):
            for name in sorted(names):
                if not re.match(r"z3_verify_.*\.py$", name):
                    continue
                fp = os.path.abspath(os.path.join(dirpath, name))
                if fp not in seen:
                    seen.add(fp)
                    scripts.append(fp)
    return sorted(scripts)


def run_batch_script(path):
    env = dict(os.environ)
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    try:
        r = subprocess.run([sys.executable, path], capture_output=True,
                           text=True, encoding="utf-8", errors="replace",
                           timeout=300, cwd=os.path.dirname(path),
                           env=env)
        verified = r.stdout.count("[VERIFIED]")
        tail = "\n".join(r.stdout.strip().splitlines()[-6:])
        return {
            "script": os.path.basename(path),
            "exit_code": r.returncode,
            "verified_lines": verified,
            "stdout_tail": tail,
        }
    except subprocess.TimeoutExpired:
        return {"script": os.path.basename(path), "exit_code": -1,
                "verified_lines": 0, "stdout_tail": "TIMEOUT (>300s)"}
    except Exception as exc:
        return {"script": os.path.basename(path), "exit_code": -2,
                "verified_lines": 0, "stdout_tail": f"ERROR: {exc}"}


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main():
    print("=" * 62)
    print("  AETHERZ3OMEGA: SMT TRIBUNAL STRESS-TEST PIPELINE")
    print("=" * 62)

    roots = sys.argv[1:] if len(sys.argv) > 1 else [SMT_DIR, REPO_ROOT]
    smt_files = discover_smt2(roots)

    instant = solver_info()
    print(f"Backend solver : {instant}\n")

    # -- Phase 1: rigidity audit of .smt2 files ---------------------------
    if not smt_files:
        print("Tidak ada file .smt2 ditemukan. Skipping Phase 1.")
        report = []
    else:
        report = []
        for path in smt_files:
            rel = os.path.relpath(path, REPO_ROOT)
            print(f"Audit rigiditas {rel} ...")
            blocks = audit_smt_file(path)
            tags = [b["tag"] for b in blocks]
            if tags and all(t == "PASS" for t in tags):
                fv = "VALID"
            elif any(t == "VACUOUS" for t in tags):
                fv = "WEAK (vacuous block detected)"
            elif any(t == "FAIL" for t in tags):
                fv = "INVALID"
            else:
                fv = "UNKNOWN"
            entry = {"batch": rel, "file_verdict": fv, "blocks": blocks}
            report.append(entry)
            print(f"  -> file_verdict={fv}")
            for b in blocks:
                print(f"     block {b['block']}: full={b['full_negation']} "
                      f"premises={b['premises_only']} | {b['verdict']}")

    # -- Phase 2: execute z3_tribunal batch scripts ------------------------
    print("\nMenjalankan batch verifikasi Z3 (z3_verify_*.py) ...")
    batch_reports = []
    for script in discover_batch_scripts([SMT_DIR]):
        print(f"  {os.path.basename(script)} ...")
        br = run_batch_script(script)
        batch_reports.append(br)
        tail = (br["stdout_tail"].splitlines() or [""])[-1]
        print(f"    exit={br['exit_code']} verified_lines={br['verified_lines']}"
              f" last={tail}")

    out = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "solver_string": instant,
        "smt_files": report,
        "z3_batch_scripts": batch_reports,
    }
    out_path = os.path.join(REPO_ROOT, "smt_stress_test_report.json")
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=4, ensure_ascii=False)
    print(f"\nEvaluasi selesai. Laporan formal diekspor ke '{out_path}'")


if __name__ == "__main__":
    main()