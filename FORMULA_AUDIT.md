# Formula audit — Chapters 7, 8, and 9

## Scope

Reviewed all 117 imported entries in Chapters 7–9 against their stored spreadsheet text and standard mathematical consistency. The original lecture PDFs were not available, so this is not a page-by-page verification against the book. Image files were checked for presence, not independently transcribed or compared with the PDFs.

| Chapter | Entries | Added LaTeX transcriptions | Existing equation images | Prose-only entries |
| --- | ---: | ---: | ---: | ---: |
| 7 | 51 | 46 | 4 | 1 |
| 8 | 33 | 27 | 2 | 4 |
| 9 | 33 | 20 | 0 | 13 |

All 93 added LaTeX transcriptions render successfully with the bundled KaTeX. They are presentation transcriptions of the supplied text, not formulas recovered from the book. Original spreadsheet fields remain unchanged. Purely descriptive entries remain prose; no equations were invented for them.

## Findings requiring attention

### Chapter 8: Normal Zeeman Hamiltonian (C8-012, equation 8.8)

The spreadsheet gives `H = H⁽⁰⁾ + (eB/2mc)L₃`. Its earlier orbital coupling is `−(e/2mc)L·B`, and its Larmor-frequency entry calls `e` the signed electron charge. With a common signed-charge convention and B along +z, those signs are inconsistent. A change from signed charge to positive charge magnitude could explain the discrepancy, but cannot be assumed without the PDF. The source expression is preserved and an explanatory note is shown on this card.

### Chapter 8: Cyclotron frequency (C8-029, equation 8.16)

The spreadsheet gives `ωc = eB/m`, while earlier electromagnetic formulas include Gaussian-unit factors of `c`. The positive nonrelativistic cyclotron frequency is `|q|B/m` in SI and `|q|B/(mc)` in Gaussian units. The expression therefore needs unit and charge-sign confirmation from the PDF. It has not been silently corrected; the card shows a warning.

### Chapter 9: Extremal contradiction (C9-025, equation 9.10)

The equality chain `â₁=b̂₁=b̂₂=â₂=−b̂₂` is impossible for extremal ±1 response means, but is satisfied when all means are zero. The card now explicitly states the extremality assumption required for the contradiction.

### Chapter 9: CHSH normalization (C9-023–C9-030)

The half-scaled CHSH expression has local bound 1. The unscaled correlator sum has local bound 2. The imported table already corrects the latter to 2 and says the source prints 1. This distinction and the source-typo explanation are preserved. The PDF typo itself could not be independently confirmed.

### Chapter 7: notation and domain caveats

- Coupled kets retain the subscript `j` to distinguish them from product kets with similar labels.
- The spreadsheet's convention that product `|1,1⟩` has positive z-spin is preserved; it should not be replaced with a different qubit-label convention.
- The `l−½` branch applies only when nonnegative; the existing explanation correctly excludes it for `l=0`.
- The Hilbert-space entry retains `L²(ℝ) ⊗ ℂ²` as supplied; whether the lecture intends one or three spatial dimensions requires the PDF.
- The group-representation entry retains `GL(n,ℝ)` as supplied; this is not a claim that every quantum spin representation is real.

## Maintenance

`formula_latex.json` stores the 93 typesetting transcriptions by source card ID. `import_cards.py` applies them and adds the three explicit audit notes while keeping the original source fields. Reimporting the workbooks preserves the typesetting and notes. If formulas change in the workbooks, review the corresponding transcriptions again.
