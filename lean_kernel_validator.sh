#!/bin/bash
# =====================================================================
#  AETHERZ3OMEGA: LEAN 4 INDEPENDENT KERNEL VALIDATOR
# =====================================================================
#  Runs on Linux/macOS bash or Windows Git Bash.
#
#  Pipeline:
#   1. Probe the Lean 4 kernel/toolchain (compile + run a temp program).
#   2. Audit axiom / constant / sorry / admit pollution. Comments are
#      stripped first, so only REAL sorry tokens are counted.
#   3. Mathlib-backed kernel sweep of the Riemann corpus
#      (lean4/AetherZ3Omega/Riemann): kernel type-check with real Mathlib
#      oleans -> real `lean -o` .olean builds, then a driver `#print axioms`
#      lists the EXACT axiom dependencies the Lean kernel resolves for every
#      declaration. Modules that do not compile are recorded in a ledger with
#      the real blocking reason (fictional Mathlib paths, unknown identifiers,
#      or malformed proof terms).
#
#  LEAN 4 FACTS:
#   - `lean --export` does NOT exist in Lean 4 (Lean 3 / Trepplein flag).
#   - Modules importing Mathlib can only be verified against real Mathlib
#     oleans (Step 3); lake targets are unreliable for ad-hoc modules.
# =====================================================================

set -uo pipefail

LEAN_RIEMANN_DIR="lean4/AetherZ3Omega/Riemann"
KERNEL_BUILD=".kernel_build"

echo "=============================================================="
echo "  AETHERZ3OMEGA: LEAN 4 INDEPENDENT KERNEL VALIDATOR"
echo "=============================================================="

# ---------------------------------------------------------------
# helpers
# ---------------------------------------------------------------
has() { command -v "$1" >/dev/null 2>&1; }

code_only() {
    # strip Lean comments (-- line, /- -/ block) using perl if available
    if has perl; then
        perl -0777 -pe 's{/-.*?-/}{}sg; s/--[^\n]*//g' "$1"
    else
        cat "$1"
    fi
}

count_of() { # file pattern
    code_only "$1" | grep -cE "$2" 2>/dev/null || true
}

sum_dir() { # dir pattern -> integer
    local dir="$1" pattern="$2" total=0 n f
    for f in "$dir"/*.lean; do
        [ -e "$f" ] || continue
        n="$(count_of "$f" "$pattern")"
        total=$((total + n))
    done
    echo "$total"
}

# ---------------------------------------------------------------
# Step 0: prerequisites
# ---------------------------------------------------------------
if ! has lean; then
    echo "🚨 Error: 'lean' tidak ditemukan di PATH."
    exit 1
fi
if [ ! -d "$LEAN_RIEMANN_DIR" ]; then
    echo "🚨 Error: direktori source Lean tidak ditemukan ($LEAN_RIEMANN_DIR)."
    exit 1
fi

LEAN_VER="$(lean --version | head -n1)"
echo "Lean toolchain : $LEAN_VER"
echo

cleanup() { rm -f "$PROBE_FILE" "$OUT_OLEAN" "$PROBE_FILE.out" "$PROBE_FILE.err"; }
trap cleanup EXIT

# ---------------------------------------------------------------
# Step 1: kernel probe
# ---------------------------------------------------------------
PROBE_FILE=".lean_kernel_probe.lean"
OUT_OLEAN=".lean_kernel_probe.olean"
echo "Step 1: Proba Kernel Lean 4 (kompilasi program temp + jalankan main)..."
cat > "$PROBE_FILE" <<'LEAN_EOF'
import Lean

#eval Lean.versionString

def main : IO Unit :=
  IO.println "KERNEL_PROBE_OK"
LEAN_EOF

if lean --run "$PROBE_FILE" >"$PROBE_FILE.out" 2>"$PROBE_FILE.err"; then
    echo "  ✅ KERNEL PROBE PASS"
    echo "     version : $(tail -n 1 "$PROBE_FILE.out" | tr -d '\n')"
    echo "     probe   : $(grep -o 'KERNEL_PROBE_OK' "$PROBE_FILE.out")"
else
    echo "  🚨 KERNEL PROBE FAIL"
    sed 's/^/     /' "$PROBE_FILE.err" | head -n 10
fi
rm -f "$PROBE_FILE.out" "$PROBE_FILE.err"

# ---------------------------------------------------------------
# Step 2: pollution audit (comments stripped)
# ---------------------------------------------------------------
echo "Step 2: Audit Polusi Aksioma & sorry (komentar dibuang)..."

audit_dir() {
    local dir="$1"
    [ -d "$dir" ] || { echo "  (dir $dir tidak ada)"; return; }
    local files theorems axioms consts sorries admits
    files="$(ls "$dir"/*.lean 2>/dev/null | wc -l)"
    theorems="$(sum_dir "$dir" '^[[:space:]]*(theorem|lemma|def|opaque|abbrev)[[:space:]]+')"
    axioms="$(sum_dir "$dir" '^[[:space:]]*axiom[[:space:]]+')"
    consts="$(sum_dir "$dir" '^[[:space:]]*(constant|opaque)[[:space:]]+')"
    sorries="$(sum_dir "$dir" '\bsorry\b')"
    admits="$(sum_dir "$dir" '\badmit\b')"
    echo "  $dir :"
    echo "    file        : $files"
    echo "    thm/lem/def : $theorems"
    echo "    axiom       : $axioms"
    echo "    constant    : $consts"
    echo "    sorry (real): $sorries"
    echo "    admit       : $admits"
}

audit_dir "$LEAN_RIEMANN_DIR"

echo "  -- Spot-check critical path (sorry berwarna hanya jika kode) --"
for f in "$LEAN_RIEMANN_DIR"/{BarrierTheorem,Rigidity,ZetaBasic,Axioms,RhCore,RhZetaTower}.lean; do
    [ -f "$f" ] || continue
    ax="$(count_of "$f" '^[[:space:]]*axiom[[:space:]]+')"
    ct="$(count_of "$f" '^[[:space:]]*(constant|opaque)[[:space:]]+')"
    so="$(count_of "$f" '\bsorry\b')"
    th="$(count_of "$f" '^[[:space:]]*(theorem|lemma|def)[[:space:]]+')"
    echo "    $(basename "$f"): thm/lem/def=$th axiom=$ax constant=$ct sorry=$so"
done
echo "  -- File dengan sorry SEJATI --"
for f in "$LEAN_RIEMANN_DIR"/*.lean; do
    [ -f "$f" ] || continue
    so="$(count_of "$f" '\bsorry\b')"
    if [ "$so" -gt 0 ]; then
        echo "    $f: $so"
    fi
done

# ---------------------------------------------------------------
# Step 3: Mathlib-backed kernel sweep of the Riemann corpus
# ---------------------------------------------------------------
echo
echo "Step 3: Sweep Korpus Riemann dgn Mathlib NYATA..."
MATHLIB_LIB="lean4/.lake/packages/mathlib/.lake/build/lib/lean"
SWEEP_DIR="$KERNEL_BUILD/sweep"

has_match_lib() { [ -d "$MATHLIB_LIB" ] && [ -n "$(ls "$MATHLIB_LIB" 2>/dev/null)" ]; }

if has_match_lib; then
    ML_PATH="$SWEEP_DIR"
    for d in lean4/.lake/build/lib/lean lean4/.lake/packages/*/.lake/build/lib/lean; do
        [ -d "$d" ] && ML_PATH="$ML_PATH;$d"
    done
    ML_PATH="${ML_PATH#;}"

    mkdir -p "$SWEEP_DIR/AetherZ3Omega/Riemann"
    ledger="$SWEEP_DIR/ledger.txt"
    : > "$ledger"
    built=0

    sweep_round() {
        local f b out log first
        for f in "$LEAN_RIEMANN_DIR"/*.lean; do
            [ -f "$f" ] || continue
            b="$(basename "$f" .lean)"
            [ -f "$SWEEP_DIR/AetherZ3Omega/Riemann/$b.olean" ] && continue
            grep -q "^$b|FAIL" "$ledger" && continue
            out="$SWEEP_DIR/AetherZ3Omega/Riemann/$b.olean"
            log="$SWEEP_DIR/_t_$b.log"
            if LEAN_PATH="$ML_PATH" lean -R "lean4" -o "$out" "$f" >"$log" 2>&1; then
                echo "$b|PASS" >> "$ledger"
                built=$((built + 1))
            else
                first="$(grep -m1 'error' "$log" | sed 's#^.*: error#error#' | head -c 120)"
                echo "$b|FAIL|$first" >> "$ledger"
            fi
            rm -f "$log"
        done
    }

    for i in 1 2 3 4 5 6 7 8; do
        before="$built"
        sweep_round
        [ "$built" = "$before" ] && break
    done

    total="$(ls "$LEAN_RIEMANN_DIR"/*.lean 2>/dev/null | wc -l)"
    echo "  🔄 Loop sampai jenuh -> $built PASS / $total modul"
    echo "  -- Ledger FAIL (alasan blokir) --"
    pass_names=""
    for olean in "$SWEEP_DIR"/AetherZ3Omega/Riemann/*.olean; do
        [ -f "$olean" ] || continue
        pass_names="$(basename "$olean" .olean) $pass_names"
    done
    while IFS='|' read -r b st rest; do
        if [ "$st" != "PASS" ]; then
            echo "    ❌ $b : $rest"
        fi
    done < "$ledger"

    if [ -n "$pass_names" ]; then
        {
            for b in $pass_names; do echo "import AetherZ3Omega.Riemann.$b"; done
            for f in "$LEAN_RIEMANN_DIR"/*.lean; do
                b="$(basename "$f" .lean)"
                case " $pass_names " in *" $b "*) ;; *) continue ;; esac
                ns="$(grep -m1 '^namespace' "$f" | sed 's/^namespace[[:space:]]*//; s/[[:space:]]*$//')"
                [ -z "$ns" ] && ns="$b"
                code_only "$f" | grep -oE '^(theorem|lemma|def)[[:space:]]+[A-Za-z0-9_]+' \
                    | awk -v p="$ns." '{print "#print axioms " p $2}'
            done
        } > "$KERNEL_BUILD/_driver_mathlib.lean"

        LEAN_PATH="$ML_PATH" lean "$KERNEL_BUILD/_driver_mathlib.lean" \
            > "$SWEEP_DIR/_axioms.txt" 2>&1 || true

        clean="$(grep -c 'does not depend on any axioms' "$SWEEP_DIR/_axioms.txt" || true)"
        dep="$(grep -c 'depends on axioms' "$SWEEP_DIR/_axioms.txt" || true)"
        echo "  Audit kernel #print axioms (semua deklarasi korpus yang compile):"
        echo "    bersih (0 axiom)                : $clean deklarasi"
        echo "    bergantung sejumlah axiom       : $dep deklarasi"
        echo "  -- Deklarasi dgn aksioma DI LUAR fondasi standar --"
        awk '/depends on axioms/ {
            line=$0; getline rest; while (rest ~ /^[[:space:]]/) { line=line rest; getline rest }
            if (line !~ /propext, Classical.choice, Quot.sound\]$/) print "     " line }' \
            "$SWEEP_DIR/_axioms.txt" | head -n 25
        echo "  -- Flagship: teorema kunci ---"
        grep -E "Barrier.rigidity_at_infinity|AetherZ3Omega.barrier_from_riemann_hypothesis|AetherZ3Omega.old_absolute_barrier_is_inconsistent|AetherZ3Omega.zeta_dirichlet_series|AetherZ3Omega.completed_zeta_zero_neg_equiv" "$SWEEP_DIR/_axioms.txt" || true
    fi
else
    echo "  Mathlib oleans tidak ditemukan ($MATHLIB_LIB)."
    echo "  Jalankan dulu: cd lean4 && lake update (unduh Mathlib v4.33.1)."
    echo "  Tanpa Mathlib, verifikasi kernel tidak dapat dijalankan untuk korpus Riemann."
fi

echo
echo "=============================================================="
echo "Protokol audit Kernel Lean selesai."
echo "=============================================================="