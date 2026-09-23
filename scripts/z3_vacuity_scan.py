import importlib.util
import sys
from pathlib import Path

from z3 import Solver, sat, unsat

ROOT = Path(__file__).resolve().parent.parent
TRIB = ROOT / "z3_tribunal"
OUT = ROOT / ".kernel_build" / "z3_run"

def check_prop_consistent(r, premises):
    s = Solver()
    s.set("timeout", 15000)
    s.add(premises)
    res = s.check()
    return res == sat

def main():
    files = sorted(TRIB.glob("z3_*.py"))
    for f in files:
        spec = importlib.util.spec_from_file_location(f.stem, f)
        mod = importlib.util.module_from_spec(spec)
        entries = []

        def make_verify(marker):
            PremiseCheck = marker[0]
            ConsMap = marker[1]
            def verify(name, mod, stmt, premises, neg):
                consistent = check_prop_consistent(None, premises)
                PremiseCheck.append((name, premises, consistent))
                s = Solver()
                s.set("timeout", 15000)
                for p in premises:
                    s.add(p)
                s.add(neg)
                r = s.check()
                ConsMap[name] = (str(r), consistent)
                entries.append((name, str(r), consistent))
            return verify

        PremiseCheck = []

        def verify(name, mod, stmt, premises, neg):
            consistent = check_prop_consistent(None, premises)
            s = Solver()
            s.set("timeout", 15000)
            for p in premises:
                s.add(p)
            s.add(neg)
            r = s.check()
            entries.append((name, str(r), consistent))

        mod.verify = verify
        sys.modules[f.stem] = mod
        try:
            spec.loader.exec_module(mod)
        except Exception as e:
            print(f"[{f.name}] EXEC FAIL: {e}")
            continue

        vac = [e for e in entries if e[1] == "unsat" and not e[2]]
        unk = [e for e in entries if e[1] == "unknown"]
        bad = [e for e in entries if e[1] == "sat"]
        print(f"[{f.name}] calls={len(entries)} VERIFIED={len([e for e in entries if e[1]=='unsat'])} "
              f"VACUOUS={len(vac)} UNKNOWN={len(unk)} COUNTERMODEL={len(bad)}")
        for nm, rs, cons in vac:
            print(f"    VACUOUS: {nm} (premises inconsistent, r={rs})")
        for nm, rs, cons in bad:
            print(f"    COUNTEREXAMPLE: {nm} (conclusion fails with r={rs})")

if __name__ == "__main__":
    main()