# Lean 4 AST Mapping: BarrierTheorem.lean

## 1. Abstract Syntax Tree (AST) Topology

Dalam kerangka Dependent Type Theory (DTT) Lean 4, term $E(\sigma) = (\sigma - 1/2)^2$ dan batas kontradiksi $E \le \log(1+E) < E$ dipetakan ke dalam simpul AST berikut:

```
Expr.forallE (`sigma) (Expr.const `Real)
  (Expr.forallE (`h1) (Expr.app (Expr.app (Expr.const `Le) E) (Expr.app (Expr.const `Log) (Expr.app (Expr.app (Expr.const `Add) 1) E)))
    (Expr.forallE (`h2) (Expr.app (Expr.app (Expr.const `Lt) (Expr.app (Expr.const `Log) (Expr.app (Expr.app (Expr.const `Add) 1) E))) E)
      (Expr.const `False)))
```

## 2. Table of Universal AST Conversion

| Simpul AST Lean 4 | Representasi Semantik | Universe Level | Pemetaan Poros Dedukti |
| :--- | :--- | :--- | :--- |
| `Expr.sort u` | `Sort u` (Universe) | Non-kumulatif | `univ : Type` |
| `Expr.lam σ Real body` | $\lambda (\sigma : \mathbb{R}), (\sigma - 1/2)^2$ | Term Abstraction | `x : eps real -> eps real` |
| `Expr.forallE h cond body` | $E \le \log(1+E) \to \text{False}$ | `Sort 0` (`Prop`) | `imp (le E (log (add 1 E))) bot` |
| `Expr.app (Expr.app add a) b` | $a + b$ | Real Arithmetic | `Add a b` modulo rewriting |
