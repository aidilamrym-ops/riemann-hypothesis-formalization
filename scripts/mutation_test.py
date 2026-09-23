import os
import re
import shutil
import subprocess
import sys
import json
from pathlib import Path

from scan_defects import scan_file, code_only

ROOT = Path(__file__).resolve().parent.parent
MUT_DIR = ROOT / ".kernel_build" / "mutation"
CLEAN_DOC = "lean4/AetherZ3Omega/Riemann/ConreyZeroFree.lean"
LEAN_EXE = Path(os.environ.get("LEAN_EXE", "") or (
    shutil.which("lean") or r"C:\Users\usER\.elan\toolchains\leanprover--lean4---v4.33.1\bin\lean.exe"
))
LEAN_PATH_SEP = ";" if os.name == "nt" else ":"
LEAN_PATH = (
    LEAN_PATH_SEP.join(
        str(p / ".lake/build/lib/lean")
        for p in sorted((ROOT / "lean4/.lake/packages").iterdir())
        if (p / ".lake/build/lib/lean").exists()
    )
    + f"{LEAN_PATH_SEP}{ROOT / '.kernel_build' / 'sweep'}"
)


def make_mutant(name: str, inject: callable) -> tuple[Path, str]:
    src = (ROOT / CLEAN_DOC).read_text(encoding="utf-8")
    mutated = inject(src)
    out = MUT_DIR / "AetherZ3Omega" / "Riemann" / f"{name}.lean"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(mutated, encoding="utf-8")
    return out, mutated


def check_compiles(path: Path) -> bool:
    env = os.environ.copy()
    env["LEAN_PATH"] = LEAN_PATH
    rel = path.relative_to(MUT_DIR)
    root_arg = str(MUT_DIR)
    olean = (MUT_DIR / rel).with_suffix(".olean")
    res = subprocess.run(
        [str(LEAN_EXE), "-R", root_arg, "-o", str(olean), str(path)],
        env=env,
        capture_output=True,
        text=True,
    )
    return res.returncode == 0


def main():
    MUT_DIR.mkdir(parents=True, exist_ok=True)
    mutants = {}

    src = (ROOT / CLEAN_DOC).read_text(encoding="utf-8")

    # M1: real sorry injected into proof (Lean ACCEPTS sorry -> this must compile,
    # proving the scanner catches what the kernel lets through)
    m1 = src.replace(
        "  exact derive_zero_free_phi.conr_premise hx",
        "  exact by\n    sorry",
    ) if "exact derive_zero_free_phi.conr_premise hx" in src else None
    if m1 is None:
        m1 = src + "\n\ntheorem mutation_sorry (x : ℝ) : 0 ≤ Real.exp x := by\n  sorry\n"
    mutants["M1_sorry"] = make_mutant("M1_sorry", lambda s: m1)

    # M2: admit in proof
    m2 = src + "\n\ntheorem mutation_admit (x : ℝ) : 0 ≤ Real.exp x := by\n  admit\n"
    mutants["M2_admit"] = make_mutant("M2_admit", lambda s: m2)

    # M3: rogue axiom (non-RH postulate)
    m3 = src + "\n\naxiom mutation_rogue_axiom : 0 < 1 → False\n"
    mutants["M3_rogue_axiom"] = make_mutant("M3_rogue_axiom", lambda s: m3)

    # M4: fake proof of a false claim via sorry in disguise
    m4 = src + "\n\ntheorem mutation_fake (x : ℝ) : Real.exp x < 0 := by\n  sorry\n"
    mutants["M4_fake_proof"] = make_mutant("M4_fake_proof", lambda s: m4)

    report = []
    for name, (path, _) in mutants.items():
        scan = scan_file(path)
        compiles = check_compiles(path)
        detected = bool(scan["real_sorry"] or scan["admit"] or scan["axioms"] or scan["sorry_lines"])
        report.append(
            {
                "mutant": name,
                "lean_accepts_compiles": compiles,
                "scanner_real_sorry": scan["real_sorry"],
                "scanner_admit": scan["admit"],
                "scanner_axioms": scan["axioms"],
                "detected_by_scanner": detected,
            }
        )
        print(f"{name}: lean_compiles={compiles} sorry={scan['real_sorry']} "
              f"admit={scan['admit']} axiom={scan['axioms']} detected={detected}")

    ok = all(r["lean_accepts_compiles"] and r["detected_by_scanner"] for r in report)
    print(json.dumps(report, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())