# PENGEMBANGAN — Road Map Konkret
**Date:** 2026-09-23
**Status:** validated baseline; peta pengembangan jujur pasca-audit Anthropic zeta-23-lean

---

## 1. POSISI SAAT INI (baseline yang sudah teruji)

**Proyek kita (AetherZ3Omega):**
- Lean 4.33.1, Mathlib `0df444a`: 66/66 modul rebuild, 0 sorry, 1 postulat `AetherZ3Omega.riemann_hypothesis`; +`CMTBounds`, +`ZetaBounds`, +`KernelIndependence`, +`HardyZetaPositive` (2026-09-23/24).
- Z3: 91 verifikasi terekam (86 UNSAT non-vacuous + 5 UNKNOWN NFE `p^(-s)` + 1 vacuous yang disengaja di batch15); batch 14-17 TIDAK citable.
- Hilbert-Polya: OPEN (0-2/20 zero-correspondence).
- Nilai nyata: (a) **audit pipeline** (kernel + mutation + vacuity + numeric + reproducibility, `run_external_audit.ps1` + CI), (b) framing conditional yang jujur.

**Paper Anthropic (zeta-23-lean, commit `3635e748…`):**
- Teorema baru unconditional `liminf N0*/N ≥ 2/3` (opt 0.6725), `≥2/3 simple`, `≥5/6 distinct`.
- Formal: Lean v4.33.0-rc2, Mathlib `51e6992`, Teorema A-E, axioms hanya `[propext, Classical.choice, Quot.sound]`.
- **Audit independen kita (2026-09-23):** 317/317 modul Zeta23 ter-compile terhadap Mathlib KITA (rev beda `0df444a`), `#print axioms` pada 9 teorema inti = foundation-only, scan source = 0 axiom/0 sorry/0 admit. **PASS.**

---

## 2. REALITAS EPISTEMIK (mengapa dua tier tidak setara)

| Tier | Kekuatan | Yang bisa dibuktikan |
|------|----------|----------------------|
| Z3 (kita) | aritmetika real elementer, struktur aljabar | identitas/tidak-adanya-counterexample, bukan analisis asimptotik |
| Lean (kita) | teori tipe dependen + Mathlib | struktur diskret, inequality conditional |
| Lean (mereka) | teori tipe dependen + Mathlib analisis penuh (ζ asimptotik, von Neumann, Sylvester) | teorema baru tentang N0/N (zona kritis) |

**Z3 tidak bisa naik ke tier analitik** (batas keputusan struktural). Traceability yang benar:
- Numerical checks → hypothesis-strength evidence (bukan bukti)
- Lean formalization → bukti (kalau statement riil, bukan postulate)

---

## 3. ROAD MAP (4 jalur, urut nilai)

### Jalur A — Karakter Paper Anthropic (selesai 5/5, 2026-09-23)
1. **Compile penuh 317/317 terhadap Mathlib kita** — DONE (cross-revision replica).
2. **Axiom-audit 9 teorema inti** — DONE: foundation-only.
3. **Scan defect pipeline kita atas source mereka** — DONE: 0 axiom/sorry/admit.
4. *(opsional)* Numerik reproduce konstanta-konstanta mereka (lembar SymPy 31 checks) — **DONE 2026-09-23:** `scripts/numeric_constants_check.py` (mpmath 40 digit): 4/4 desimal cocok (c₁*, 1/c₁*, 2−1/c₁*, 2c₁*−1), identitas Montgomery–Taylor cocok 1e-51, konsisten dengan bukti Lean.
5. **DONE 2026-09-23:** Independence pemilihan kernel — 5 klaim kernel UNKNOWN (`euler_factor_pos/lt1/in_unit` batch7, `euler_factor_nonzero/unit_interval` batch8) dibuktikan **universal** di Lean
   (`lean4/AetherZ3Omega/Riemann/KernelIndependence.lean`, module `AetherZ3Omega.Riemann.KernelIndependence`):
   ∀ p ≥ 2, s > 1: `0 < p^(-s) < 1`, `0 < 1-p^(-s) < 1`, `1-p^(-s) ≠ 0`, `(1-p^(-s))⁻¹ > 1`
   — aksioma foundation-only, tak bergantung postulat RH; hasil tak bergantung nilai kernel konkret
   (bukan hanya sampel `2 ≤ p < 10` yang dipakai Z3). Vakuum tetap hanya 1 (batch15, disengaja);
   batch 7/8 tak berbagi kode dengan batch15 (no cross-import). Cross-check numerik 90 poin PASS
   (`scripts/kernel_independence_check.py`, P5 di `run_external_audit.ps1`).

**Nilai:** proyek kita menjadi **auditor independen paper AI Math** — klaim yang terverifikasi machine-audit dengan toolchain yang berbeda dari penulis.

### Jalur B — Perbaiki ketelitian perhitungan analitik kita (paling jujur saat ini)
Ganti pondasi toy-discrete dengan perhitungan nyata untuk klaim yang terekspos publik:
1. Rekam dalam `run_external_audit.ps1` bahwa **batch 14-17 tidak citable** (sudah ada di FINAL_STATUS).
2. **DONE 2026-09-23:** Batch Z3 → **batas `-model`/label** via `scripts/z3_division_safety.py`
   (menggantikan `z3_vacuity_scan.py` yang ternyata **tidak pernah berfungsi** — injeksi `verify` ditimpa
   oleh definisi modul sendiri & guard `__main__` tak terpicu, sehingga old scan selalu `calls=0`):
   - 91 verifikasi terekam via `Solver.check`-level; 86 UNSAT **non-vacuous** (witness model disertakan, 53 label),
     0 countermodel, 0 UNSAT **division-sensitive** (semua divisor dipaksa ≠ 0 oleh premises),
     5 UNKNOWN = NFE/transcendental (`p^(-s)` simbolik, di luar QF_NRA) di batch 7/8 — bukan artefak.
   - Hasil penuh: `exports/z3_division_safety.json`.
3. **DONE 2026-09-23:** `cMT = √2·tan(1/√2)/(1+(1/√2)tan(1/√2))` dibuktikan di Lean
   (`lean4/AetherZ3Omega/Riemann/CMTBounds.lean`, module `AetherZ3Omega.Riemann.CMTBounds`):
   `2/3 < cMT ≤ 4/5`, `0 < cMT < 1`, dan dua proporsi Theorem D positif
   (`2 − 1/c₁* > 1/2`, `2c₁* − 1 > 1/3`) — aksioma hanya `[propext, Classical.choice, Quot.sound]`,
   tidak tergantung postulat RH proyek.
4. **DONE 2026-09-23:** Probe spektral 10⁵ zero — `scripts/spectral_big_probe.py` (P6 pipeline):
   - Scan arb (interval aritmetik, python-flint) Z(t)=Re(e^{iθ}ζ(0.5+it)) pada t ∈ [14, 76420]
     (grid 0.02 prec 53; ekor 0.005 prec 128; recovery band 0.005 prec 128 di (71250, 72500)):
     **102.241** tanda-ganti terdeteksi vs hitungan von Mangoldt **102.240** (+1).
   - `γ₁₀₀₀₀₀ = 74920.8275`; RvM di situ dev −0.59; spot-check mpmath 12 indeks Δ ≤ 1.5e-11;
     rekonsiliasi `mpmath.nzeros` di 12 ketinggian: **0 deviasi**.
   - Semua di garis kritis (Re=1/2 by construction, dikoreksi mpmath); mean spacing ternormalisasi 1.000013.
   - Statistik spacing: χ² GUE-Wigner **619.8** vs Poisson **87.049** (ndf 56, ratio 0.007)
     → konsisten dengan bukti numerik gaya Odlyzko untuk gambaran statistik Hilbert–Pólya;
     **operator Dirac finite-dim spesifik kertas tetap gagal mencocokkan zero individual (0-2/20)**.
   - Interpretasi jujur: **STOP** operator toy; gambaran **GUE/HP statistik diperkuat** (tetap OPEN).
   - Zero cache: `exports/spectral_big_zeros.npz`; regenerasi penuh: `python scripts/spectral_big_probe.py --recompute`.
   - Keluaran: `exports/spectral_big_probe.json`.

**Nilai:** menutup satu-satunya celah yang bisa dibantah reviewer: "claim numerik tanpa bukti analitik".

### Jalur C — Matematika baru (amatir, berisiko, nilai besar bila berhasil)
Target realistis, bukan RH:
1. **DONE 2026-09-23:** Helper constant bounds independent — batas eksplisit `ζ(1+ε)` / `|1/ζ(1+ε)|`
   dibuktikan di Lean (`lean4/AetherZ3Omega/Riemann/ZetaBounds.lean`, module `AetherZ3Omega.Riemann.ZetaBounds`):
   untuk `1 < s` dan `ε > 0`:
   `1 ≤ ζ(s) ≤ s/(s-1)`, `ζ(1+ε) ≤ (1+ε)/ε`, `|1/ζ(1+ε)| ≤ 1`, dari ζ analitik Mathlib
   (`zeta_eq_tsum_one_div_nat_add_one_cpow` + `ZetaAsymptotics.zeta_limit_aux1`) — aksioma hanya
   `[propext, Classical.choice, Quot.sound]`, tidak tergantung postulat RH proyek; reusable untuk Jalur A maupun paper lain.
2. **DONE 2026-09-24:** Hardy-ζ titik-titik positif (formalisasi kecil) —
   `scripts .. lean4/AetherZ3Omega/Riemann/HardyZetaPositive.lean`, module `AetherZ3Omega.Riemann.HardyZetaPositive`:
   memakai `riemannZetaZeros` Mathlib (himpunan nol ζ) yang **diskret**
   (`IsDiscrete`, `IsCompact.inter_riemannZetaZeros_finite`):
   - nol ζ pada garis kritis dalam pita imajiner `[a,b]` **terbatas-banyaknya** (`criticalLine_zero_finite_Icc`),
     sehingga `N₀(T)` = banyak nol pada garis kritis di bawah tinggi `T` terdefinisi baik & hingga (`criticalLine_zero_finite_below_height`);
   - di **setiap interval real terbuka `(a,b)` ada `t` dengan `ζ(1/2 + i·t) ≠ 0`** (`exists_zeroFree_on_criticalLine_Ioo`) — himpunan nol pada garis kritis tidak berisi interval apa pun;
   - **tak hingga banyak** tinggi `t` dengan `ζ(1/2+i·t) ≠ 0` (`infinite_zeroFree_heights_on_criticalLine`) — kompatibel dengan teorema Hardy (nol di garis kritis tetap tak hingga): nol itu himpunan tipis/exsepsional, bukan menutup garis → menjelaskan kenapa `N₀(T)/N(T)` bisa naik tanpa garis kritis "penuh nol";
   - himpunan nol ζ diskret di ℂ (`isDiscrete_riemannZetaZeros`) & hingga pada kompak mana pun (`finite_zetaZeros_on_compact`);
   - **daerah bebas nol**: `Re s ≥ 1` tidak memuat nol (`zeroSet_disjoint_halfPlane_geOne`, via `riemannZeta_ne_zero_of_one_le_re`).
   - `#print axioms` 8 teorema = `[propext, Classical.choice, Quot.sound]` (foundation-only, tanpa postulat RH proyek).
3. Jika tertarik ke arah Hilbert-Polya: buktikan **non-keberadaan** operator finite-dim yang cocok dengan spektrum tak-hingga (hasil negatif yang dapat dipublikasi).

**Nilai:** kontribusi kecil yang benar > klaim besar yang salah.

### Jalur D — Publishing & Tuduh-balik (kebersihan komunikasi)
1. Tulis ulang bagian "kesimpulan" FINAL_STATUS: RH tetap OPEN; proyek adalah **audit harness**, bukan bukti RH.
2. Upload `exports/zeta23_independent_audit.json` + bukti CI sebagai artifact publik (mis. di README).
3. (opsional) Tawarkan audit results ke pengelola zeta-23-lean via isu GitHub — reputasi kecil tapi nyata.

---

## 4. Keputusan yang disarankan

1. **Sekarang:** commit hasil audit independen (`exports/zeta23_independent_audit.json`) + bukti `CMTBounds.lean` + `ZetaBounds.lean` + `KernelIndependence.lean` + roadmap + audit Z3 (division-safety/vacuity) + P5/P6 pipeline.
2. **Berikutnya:** Jalur A tuntas (item 1-5), Jalur B item 4 tuntas (probe 10⁵ zero — lihat §3), Jalur C item 2 tuntas (Hardy-ζ titik-titik positif — lihat §3). Lanjutkan **Jalur D** (publishing artifact & tawaran audit ke pengelola) bila ingin menyelesaikan siklus auditor.
3. **Nanti:** Jalur D (publishing artifact & tawaran audit ke pengelola).

> Prinsip: **Segala sesuatu yang diklaim "verified" harus terverifikasi oleh kernel/decider/numerik-that-can-be-challenged. Segala sesuatu yang belum, diberi label "open".**