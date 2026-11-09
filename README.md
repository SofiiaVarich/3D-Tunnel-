# QuantumMechanicsFU — 3D Tunnel

An interactive quantum mechanics flashcard tunnel built with HTML, CSS 3D transforms, and vanilla JavaScript. No installation, build step, CDN, or network connection is required. KaTeX 0.16.22 is bundled locally for mathematical typesetting (MIT license in `assets/katex/LICENSE`).

## Run

Open `index.html` in a modern browser, or serve this directory with any static web server. Keep `cards.js` and the entire `assets/` directory alongside the HTML when deploying.

## Explore and study

- Scroll to travel through the endless rotating tunnel.
- Drag to rotate it; move the pointer to tilt the view.
- Click a card to open its concept. Recall the definition or formula, then select **Antwort anzeigen** to reveal the spreadsheet material.
- Select **Kurs erkunden** or **Kurs** to accelerate through the tunnel.
- Select **Karte lernen** or **Übungen** for a random study card.
- Select **Über** for an introduction; close panels with × or Escape.

The interface is German; imported material keeps the original spreadsheet language and notation. The old 30 demonstration cards and multiple-choice quizzes have been replaced by source-based recall cards: the supplied tables do not contain multiple-choice questions or distractors. There is no grading or saved study progress.

## Imported content

**711 unique cards**, covering concept decks, supplementary named concepts and boxed rules, and the formula reference workbook. Exact duplicate rows are merged, including the duplicate Chapter 2 workbook; alternate formulations and overlapping concepts are retained deliberately.

| Chapter / collection | Cards |
| --- | ---: |
| 1 | 1 |
| 2 | 77 |
| 3 | 67 |
| 4 | 96 |
| 5 | 118 |
| 6 | 124 |
| 7 | 51 |
| 8 | 33 |
| 9 | 33 |
| 10 | 74 |
| Experimental – Franke | 37 |

Cards show only the concept, formula or key statement, meaning, and application when available. Duplicate values, card IDs, priorities, spreadsheet metadata, source references, and Telegram formatting are hidden. Original fields and source provenance remain in `cards.js`. Study-guide and verification-note sheets are not converted into cards; the supplied workbooks remain authoritative for those editorial notes.

The 418 cards with LaTeX (325 supplied in the workbooks and 93 presentation transcriptions for Chapters 7–9) are typeset with KaTeX in both tunnel previews and answer panels, using mathematical fractions, matrices, integrals, superscripts, and bra–ket notation. Cards without LaTeX retain their supplied Unicode notation rather than an inferred conversion. Exact matching to the lecture book cannot be guaranteed without the original PDFs. The formula-reference workbook's **72 embedded equation images** are extracted into `assets/formulas/` and shown in the answer panels; no formulas are inferred from images. Spreadsheet text is inserted using `textContent`, not interpreted as HTML.

### Source workbooks

- `QM_Chapter2_Concepts_BOX_Rules_Telegram_LaTeX.xlsx`
- `QM_Chapter2_Concepts_BOX_Rules_Telegram_LaTeX copy.xlsx`
- `QM_Chapter3_Concept_Learning_Cards.xlsx`
- `QM_Chapter4_Concepts_BOX_Rules_Telegram_LaTeX.xlsx`
- `QM_Chapter5_Verified_Expanded_Box_Formulas_With_LaTeX.xlsx`
- `QM_Chapter6_Script_Only_With_LaTeX.xlsx`
- `QM_Chapter7_Concept_Learning_Cards.xlsx`
- `QM_Chapter8_Concept_Learning_Cards.xlsx`
- `QM_Chapter9_Concept_Learning_Cards.xlsx`
- `QM_Chapter10_Concept_Learning_Cards.xlsx`
- `QM_formulas_rendered_multiline.xlsx`

The source XLSX files are not copied into this repository. Content is transcribed from the supplied tables, not independently verified against the lecture PDFs.

## Refreshing the cards

`import_cards.py` uses only the Python 3 standard library. Put the source workbooks together in a directory, then run:

```sh
python3 import_cards.py "/path/to/workbooks"
```

This regenerates `cards.js` and extracts formula images. Only the explicitly listed workbooks are imported; unrelated XLSX files in the directory are ignored. Do not hand-edit the generated data: update the workbooks and rerun the importer instead. `formula_latex.json` supplies the Chapter 7–9 typesetting transcriptions; review these too if the corresponding source equations change. See `FORMULA_AUDIT.md` for coverage and unresolved source-convention issues. If the source workbook schemas change, update the importer's header mappings as well.
