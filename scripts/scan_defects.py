import re
import sys
import json
from pathlib import Path


def code_only(text: str) -> str:
    text = re.sub(r"/-(.|\n)*?-/", "", text, flags=re.DOTALL)
    text = re.sub(r"--[^\n]*", "", text)
    return text


def scan_file(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8", errors="replace")
    code = code_only(raw)
    n_theorem = len(re.findall(r"^\s*(theorem|lemma|def|opaque|abbrev)\s+\w+", code, flags=re.M))
    n_axiom = len(re.findall(r"^\s*axiom\s+\w+", code, flags=re.M))
    n_constant = len(re.findall(r"^\s*(constant|opaque)\s+\w+", code, flags=re.M))
    n_sorry = len(re.findall(r"\bsorry\b", code))
    n_admit = len(re.findall(r"\badmit\b", code))
    n_admit_all = len(re.findall(r"admit_all\b", code))
    n_trivial = len(re.findall(r"\bby\s+trivial\b", code))
    n_rfl = len(re.findall(r"\bby\s+rfl\b", code))
    sorry_lines = []
    for i, raw_line in enumerate(raw.split("\n"), start=1):
        line = raw_line.split("--")[0]
        if re.search(r"/-", line):
            continue
        if re.search(r"\bsorry\b", line):
            sorry_lines.append((i, raw_line.strip()))
    return {
        "file": path.as_posix(),
        "declarations": n_theorem,
        "axioms": n_axiom,
        "constants": n_constant,
        "real_sorry": n_sorry,
        "admit": n_admit + n_admit_all,
        "by_trivial": n_trivial,
        "by_rfl": n_rfl,
        "sorry_lines": sorry_lines,
    }


def main() -> int:
    import glob as _glob
    paths = []
    for a in sys.argv[1:]:
        if a == "--json":
            continue
        paths.extend(Path(p) for p in _glob.glob(a))
    results = [scan_file(p) for p in paths]
    total_sorry = sum(r["real_sorry"] for r in results)
    total_axiom = sum(r["axioms"] for r in results)
    total_admit = sum(r["admit"] for r in results)
    if "--json" in sys.argv:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        for r in results:
            print(f"{r['file']}: decl={r['declarations']} axiom={r['axioms']} "
                  f"constant={r['constants']} sorry={r['real_sorry']} admit={r['admit']} "
                  f"by_trivial={r['by_trivial']} by_rfl={r['by_rfl']}")
        if total_sorry:
            print("DEFECT: real sorry found")
        if total_admit:
            print("DEFECT: admit found")
    return 1 if (total_sorry or total_admit or total_axiom > 1) else 0


if __name__ == "__main__":
    sys.exit(main())