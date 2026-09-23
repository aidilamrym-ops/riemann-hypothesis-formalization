#!/usr/bin/env python3
"""DEPRECATED alias: superseded by scripts/z3_division_safety.py.

The old implementation injected a `verify` into each batch module, but every
batch either re-defines `verify` itself (overwriting the injection) or keeps
its solver.check() calls behind an `if __name__ == "__main__"` guard that
never fires under importlib exec_module -- so the old scan recorded calls=0
for ALL thirteen batches.  This thin wrapper runs the working engine, which
records at the Solver.check() level and executes each batch with
__name__ == "__main__".
"""
import runpy
from pathlib import Path

runpy.run_path(str(Path(__file__).resolve().with_name("z3_division_safety.py")),
               run_name="__main__")