# PENGEMBANGAN — Road Map Konkret
**Date:** 2026-09-23
**Status:** validated baseline; peta pengembangan jujur pasca-audit Anthropic zeta-23-lean

---

## 1. POSISI SAAT INI (baseline yang sudah teruji)

**Proyek kita (AetherZ3Omega):**
- Lean 4.33.1, Mathlib `0df444a`: 62/62 modul rebuild, 0 sorry, 1 postulat `AetherZ3Omega.riemann_hypothesis`.
- Z3: 72 klaim non-vacuous + 5 UNKNOWN (batch 14-17 = vacuous/circular, TIDAK citable).
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

### Jalur A — Karakter Paper Anthropic (sudah 80% jalan)
Lanjutkan ke lampu hijau penuh:
1. **Compile penuh 317/317 terhadap Mathlib kita** — DONE (cross-revision replica).
2. **Axiom-audit 9 teorema inti** — DONE: foundation-only.
3. **Scan defect pipeline kita atas source mereka** — DONE: 0 axiom/sorry/admit.
4. *(opsional)* Numerik reproduce konstanta-konstanta mereka (lembar SymPy 31 checks) — belum.
5. *(opsional)* Cek independence pemilihan kernel (di proyek kita sendiri diharapkan batch vakum yang lain).

**Nilai:** proyek kita menjadi **auditor independen paper AI Math** — klaim yang terverifikasi machine-audit dengan toolchain yang berbeda dari penulis.

### Jalur B — Perbaiki ketelitian perhitungan analitik kita (paling jujur saat ini)
Ganti pondasi toy-discrete dengan perhitungan nyata untuk klaim yang terekspos publik:
1. Rekam dalam `run_external_audit.ps1` bahwa **batch 14-17 tidak citable** (sudah ada di FINAL_STATUS).
2. Batch Z3 yang non-vacuous (72 klaim) → tambahkan **batas `-model`/label**: pastikan UNSAT tidak berasal dari division-by-zero atau NFE.
3. Untuk setiap faktor `cMT = √2·tan(1/√2)/(1+(1/√2)tan(1/√2))` → buktikan di Lean (bukan Z3), sebagai substitusi postulate.
4. Numerik: naikkan pengujian spectral dari 20 → probe 10⁵ zero (memperkuat atau menghentikan).

**Nilai:** menutup satu-satunya celah yang bisa dibantah reviewer: "claim numerik tanpa bukti analitik".

### Jalur C — Matematika baru (amatir, berisiko, nilai besar bila berhasil)
Target realistis, bukan RH:
1. **Helper constant bounds independent**: mis. batas eksplisit `ζ(1+ε)` / `|1/ζ(1+ε)|` yang lebih tajam dari trivial, dibuktikan di Lean — reusable untuk jalur A maupun paper lain.
2. **Hardy-ζ titik-titik positif**: formalisasi kecil (bukan penuh) bahwa ada banyak s = 1/2 + it dengan ζ ≠ 0 pada batas tertentu — input untuk memahami mengapa N0/N naik.
3. Jika tertarik ke arah Hilbert-Polya: buktikan **non-keberadaan** operator finite-dim yang cocok dengan spektrum tak-hingga (hasil negatif yang dapat dipublikasi).

**Nilai:** kontribusi kecil yang benar > klaim besar yang salah.

### Jalur D — Publishing & Tuduh-balik (kebersihan komunikasi)
1. Tulis ulang bagian "kesimpulan" FINAL_STATUS: RH tetap OPEN; proyek adalah **audit harness**, bukan bukti RH.
2. Upload `exports/zeta23_independent_audit.json` + bukti CI sebagai artifact publik (mis. di README).
3. (opsional) Tawarkan audit results ke pengelola zeta-23-lean via isu GitHub — reputasi kecil tapi nyata.

---

## 4. Keputusan yang disarankan

1. **Sekarang:** commit hasil audit independen (`papers/`, `exports/zeta23_independent_audit.json`) + catatan roadmap ini.
2. **Berikutnya:** jalankan Jalur B item 3 (Lean-proof untuk cMT), karena menutup celah paling mudah dibantah.
3. **Nanti:** Jalur A opsional 4-5 (numerik konstanta + jejaring kerja); Jalur C hanya bila eksplorasi matematikan diminta.

> Prinsip: **Segala sesuatu yang diklaim "verified" harus terverifikasi oleh kernel/decider/numerik-that-can-be-challenged. Segala sesuatu yang belum, diberi label "open".**