# =====================================================================
#  AETHERZ3OMEGA: RUN EXTERNAL AUDIT (Reproducible Independent Audit)
# =====================================================================
#  One-command driven audit for an external reviewer. Requires:
#    - Lean 4 toolchain on PATH (elan) with Mathlib packages fetched
#      (run `cd lean4; lake update` once) - Mathlib oleans needed for
#      the kernel sweep.
#    - Python >= 3.11 with z3-solver, numpy, mpmath, scipy.
#
#  Pipeline (matches phase 1..4 of the extreme test):
#    P1  KERNEL   rebuild every Riemann module with lean.exe + LEAN_PATH
#                 mirror, then a `#print axioms` driver over all constants.
#    P2  POLLUTE  scan_defects.py (real sorry/admit/axiom counts)
#                 + mutation_test.py   (4 mutants; kernel accepts, scanner
#                                       catches -> detector is necessary)
#    P3  Z3       every z3_tribunal batch, plus vacuity audit
#    P4  NUMERIC  spectral_verification.py + real_computation_audit.py
#    P5  KERNEL   numeric cross-check of Euler-factor universal bounds
#                 (Lean: AetherZ3Omega.Riemann.KernelIndependence)
#
#  Artifacts: exports/verification_report.json (regenerated) and the
#             .kernel_build/ working tree (git-ignored).
# =====================================================================

param(
    [switch]$SkipKernel,
    [switch]$SkipPython
)
$ErrorActionPreference = "Continue"
$PSNativeCommandUseErrorActionPreference = $false
$ROOT = (Resolve-Path (Join-Path $PSScriptRoot ".")).Path
Set-Location $ROOT
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUTF8 = "1"

$hasCmd = { param($n) (Get-Command $n -ErrorAction SilentlyContinue) -ne $null }

Write-Host "=============================================================="
Write-Host "  AETHERZ3OMEGA EXTERNAL AUDIT  |  $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
Write-Host "  Root: $ROOT"
Write-Host "=============================================================="

if (-not (& $hasCmd "lean")) {
    Write-Host "ERROR: 'lean' tidak di PATH. Aktifkan toolchain: elan default leanprover/lean4:v4.33.1" -ForegroundColor Red
    exit 1
}
if (-not (& $hasCmd "python")) {
    Write-Host "ERROR: 'python' tidak ditemukan." -ForegroundColor Red
    exit 1
}
if (-not (Test-Path "lean4/.lake/packages/mathlib/.lake/build/lib/lean/Mathlib")) {
    Write-Host "WARN: Mathlib oleans belum ada. Jalankan: cd lean4; lake update; lake build Mathlib (sekali saja)." -ForegroundColor Yellow
}
$leanVer = (& lean --version | Select-Object -First 1)
Write-Host "Lean: $leanVer"
python -c "import z3, numpy, mpmath; print('Python pkgs: z3', z3.get_version_string(), '| numpy', numpy.__version__, '| mpmath', mpmath.__version__)"
Write-Host

# ---------------------------------------------------------------
# P1: KERNEL SWEEP + #print axioms
# ---------------------------------------------------------------
if (-not $SkipKernel) {
    Write-Host "--- P1 KERNEL: rebuild + axiom audit (bash validator) ---" -ForegroundColor Cyan
    if (& $hasCmd "bash") {
        bash ./lean_kernel_validator.sh
    } else {
        Write-Host "  'bash' (Git Bash/WSL) tidak ditemukan; lewati kernel sweep." -ForegroundColor Yellow
    }
} else {
    Write-Host "--- P1 SKIPPED (SkipKernel) ---" -ForegroundColor DarkGray
}

# ---------------------------------------------------------------
# P2: POLLUTION + MUTATION
# ---------------------------------------------------------------
if (-not $SkipPython) {
    Write-Host "--- P2 POLLUTION + MUTATION ---" -ForegroundColor Cyan
    python scripts/scan_defects.py
    New-Item -ItemType Directory -Force -Path ".kernel_build\mutation" | Out-Null
    python scripts/mutation_test.py
} else {
    Write-Host "--- P2 SKIPPED (SkipPython) ---" -ForegroundColor DarkGray
}

# ---------------------------------------------------------------
# P3: Z3 TRIBUNAL (all batches) + vacuity audit
# ---------------------------------------------------------------
if (-not $SkipPython) {
    Write-Host "--- P3 Z3 TRIBUNAL ---" -ForegroundColor Cyan
    New-Item -ItemType Directory -Force -Path ".kernel_build\z3_run" | Out-Null
    $batches = Get-ChildItem "z3_tribunal\z3_*.py" | Sort-Object Name
    Write-Host "  Found $($batches.Count) batch scripts (z3_deep_loop_batch14 plus z3_verify_batch*)."
    Push-Location "z3_tribunal"
    foreach ($b in $batches) {
        $sw = [System.Diagnostics.Stopwatch]::StartNew()
        & python $b.FullName 2>&1 | Out-File "$ROOT\.kernel_build\z3_run\$($b.Name).log" -Encoding utf8
        $rc = $LASTEXITCODE
        $sw.Stop()
        Write-Host ("  [{0}] {1}  {2}s" -f $rc, $b.Name, [math]::Round($sw.Elapsed.TotalSeconds,1))
    }
    Pop-Location
    python scripts/z3_division_safety.py
} else {
    Write-Host "--- P3 SKIPPED (SkipPython) ---" -ForegroundColor DarkGray
}

# ---------------------------------------------------------------
# P4: NUMERIC AUDITS
# ---------------------------------------------------------------
if (-not $SkipPython) {
    Write-Host "--- P4 NUMERIC AUDITS ---" -ForegroundColor Cyan
    python scripts/real_computation_audit.py
    python scripts/numeric_constants_check.py
    Push-Location scripts
    python spectral_verification.py
    Pop-Location
} else {
    Write-Host "--- P4 SKIPPED (SkipPython) ---" -ForegroundColor DarkGray
}

# ---------------------------------------------------------------
# P5: KERNEL-INDEPENDENCE (Euler factor universal bounds)
#     Z3 batch7/8 UNKNOWN kernel claims p^(-s) are NFE; Lean proves
#     them universally (AetherZ3Omega.Riemann.KernelIndependence) and
#     this step numerically cross-checks a sample of the domain.
# ---------------------------------------------------------------
if (-not $SkipPython) {
    Write-Host "--- P5 KERNEL-INDEPENDENCE (numeric cross-check) ---" -ForegroundColor Cyan
    python scripts/kernel_independence_check.py
} else {
    Write-Host "--- P5 SKIPPED (SkipPython) ---" -ForegroundColor DarkGray
}

# ---------------------------------------------------------------
# Summary
# ---------------------------------------------------------------
Write-Host
Write-Host "=============================================================="
Write-Host "  EXTERNAL AUDIT DONE. Lihat: exports/verification_report.json"
Write-Host "=============================================================="