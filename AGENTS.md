# AGENTS.md — Anchor Anti-Tersesat (WAJIB dibaca tiap awal sesi)

> **Satu-satunya path kanonik yang VALID:**
> `C:\Users\usER\oracle-toe\FINAL_RH_PROJECT`
>
> **JANGAN PERNAH** `cd` / membaca / menulis ke:
> - `C:\Users\usER\oracle-one\FINAL_RH_PROJECT` (pohon liar, bukan git)
> - `C:\Users\usER\oracle-apex-sovereign-vessel\...` (pohon liar, bukan git)
> - `...\lean4\barrier.lean` dll (stub usang era nexus v1 — validator nexus menolak)
>
> Jika live-path `Get-Location` != kanonik → **STOP**, jangan menjalankan apa pun.

## 3 Aksioma yang TIDAK BISA dikorbankan (anti-cocoklogi)

1. **Live-AST flagship (AetherZ3Omega/Riemann/BarrierTheorem.lean)**:
   Nama flagship **TIDAK BOLEH di-hardcode**. Nexus `scripts/transpilation_nexus.py`
   me-scan korpus LIVE (66 modul, 1880 deklarasi) tiap run; flagship dipilih dari
   deklarasi NYATA (preferensi `barrier*|rigidity*|log*`). Kalau flagship tidak
   terdeteksi → nexus **MENOLAK menebak** & exit non-jujur. Flagship NYATA saat ini:
   `log_one_plus_lt`.

2. **Validator hanya membaca artefak NYATA di disk**:
   `scripts/transpilation_consistency_check.py` me-rglob `exports/transpilation/**`.
   Tidak ada "flagship_present" yang disuntik dari narasi. Anti-shadow: nexus
   menghapus stub flat usang sebelum menulis canonical 4/4
   (`dedukti|coq|isabelle|clight` => `.dki|.v|.thy|.c`).

3. **Tribunal jujur terhadap UNKNOWN (z3_spectral_tribunal.py)**:
   Z3 memutuskan: F1 UNKNOWN→dicek, F2 →, dst. **Tidak pernah** memoles
   "UNKNOWN" menjadi sukses. Uni-variansi `UNSAT`/`UNKNOWN` dicatat verbatim.

## Tata Cara Jalankan (hanya di kanonik)

```powershell
cd C:\Users\usER\oracle-toe\FINAL_RH_PROJECT

# 1) Transpilasi nexus (scan korpus -> 4 backbone + manifest)
python scripts\transpilation_nexus.py

# 2) Validasi lintas-backbone (anti-cocoklogi; baca artefak disk NYATA)
python scripts\transpilation_consistency_check.py --assert

# 3) Tribunal Z3 (jujur; UNKNOWN dibiarkan UNKNOWN)
python scripts\z3_spectral_tribunal.py --assert

# 4) Kernel sweep (gate: 0 error, 0 sorry — jika ada failure, jangan lanjut)
#    lihat lean_kernel_validator.sh / .ps1 di repo root.
```

## Standar Keluaran
- Keluaran nexus: `exports\transpilation\**` + `_transpilation_manifest.json` + `flagship.txt`
- Tribunal: `exports\z3_spectral_tribunal.json`
- Verdict wajib berformat: bbox memimpin dengan **status VERIFIED / UNVERIFIED/UNKNOWN ju