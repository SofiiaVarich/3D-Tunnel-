"""Import the supplied learning workbooks using only the Python standard library.
Usage: python3 import_cards.py /path/to/workbooks
"""
import collections
import json
from pathlib import Path
import posixpath
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parent
NS = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
FILES = [
    'QM_Chapter2_Concepts_BOX_Rules_Telegram_LaTeX.xlsx',
    'QM_Chapter2_Concepts_BOX_Rules_Telegram_LaTeX copy.xlsx',
    'QM_Chapter3_Concept_Learning_Cards.xlsx',
    'QM_Chapter4_Concepts_BOX_Rules_Telegram_LaTeX.xlsx',
    'QM_Chapter5_Verified_Expanded_Box_Formulas_With_LaTeX.xlsx',
    'QM_Chapter6_Script_Only_With_LaTeX.xlsx',
    *[f'QM_Chapter{i}_Concept_Learning_Cards.xlsx' for i in range(7, 11)],
    'QM_formulas_rendered_multiline.xlsx',
]


def rows(z, name):
    strings = []
    if 'xl/sharedStrings.xml' in z.namelist():
        strings = [''.join(x.itertext()) for x in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('s:si', NS)]
    result = []
    for row in ET.fromstring(z.read(name)).findall('.//s:sheetData/s:row', NS):
        cells = {}
        for c in row.findall('s:c', NS):
            v, inline = c.find('s:v', NS), c.find('s:is', NS)
            value = v.text or '' if v is not None else ''.join(inline.itertext()) if inline is not None else ''
            if c.get('t') == 's':
                value = strings[int(value)]
            cells[re.sub(r'\d', '', c.get('r'))] = value
        result.append((int(row.get('r')), cells))
    return result


def images(z):
    """Map worksheet row numbers to embedded formula images via drawing anchors."""
    result = {}
    for name in z.namelist():
        if not re.fullmatch(r'xl/drawings/drawing\d+\.xml', name):
            continue
        relpath = posixpath.join(posixpath.dirname(name), '_rels', posixpath.basename(name) + '.rels')
        relations = {r.get('Id'): r.get('Target') for r in ET.fromstring(z.read(relpath))}
        for anchor in ET.fromstring(z.read(name)):
            row = anchor.find('.//{*}from/{*}row')
            blip = anchor.find('.//{*}blip')
            if row is None or blip is None:
                continue
            rid = next(v for k, v in blip.attrib.items() if k.endswith('}embed'))
            target = relations[rid]
            source = target.lstrip('/') if target.startswith('/') else posixpath.normpath(posixpath.join(posixpath.dirname(name), target))
            dest = ROOT / 'assets' / 'formulas' / posixpath.basename(source)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(z.read(source))
            result[int(row.text) + 1] = dest.relative_to(ROOT).as_posix()
    return result


def main(directory):
    cards, seen, sources = [], {}, []
    for filename in FILES:
        with zipfile.ZipFile(directory / filename) as z:
            chapter_match = re.search(r'Chapter(\d+)', filename)
            chapter = chapter_match.group(1) if chapter_match else None
            formula_images = images(z) if chapter is None else {}
            sheets = ET.fromstring(z.read('xl/workbook.xml')).findall('s:sheets/s:sheet', NS)
            sheet_paths = sorted((n for n in z.namelist() if re.fullmatch(r'xl/worksheets/sheet\d+\.xml', n)), key=lambda n: int(re.search(r'sheet(\d+)', n).group(1)))
            for sheet, path in zip(sheets, sheet_paths):
                data = rows(z, path)
                if not data:
                    continue
                headers = data[0][1]
                title_col = next((col for col, h in headers.items() if h in ['Front — Concept', 'Named concept', 'Rule / formula', 'Name in script', 'Concept / rule / law', 'Name / rule', 'What it is called', 'English formula name']), None)
                if title_col is None:
                    continue  # Study guides and verification notes are not flashcards.
                for rownum, cells in data[1:]:
                    title = cells.get(title_col, '').strip()
                    if not title:
                        continue
                    fields = {h: cells.get(col, '').strip() for col, h in headers.items() if cells.get(col, '').strip()}
                    formula = next((v for k, v in fields.items() if k.startswith('Back — Formula') or k in ['Formula / Key rule', 'Back — Definition / Formula', 'Formula']), '')
                    definition = next((v for k, v in fields.items() if k in ['Back — Meaning', 'Back — Definition', 'Meaning in script', 'Definition from script', 'Physical meaning', 'Script meaning', 'Definition / explanation from script', 'When to use formula']), '')
                    card = {'t': title, 'f': formula, 'x': definition, 'chapter': chapter or fields.get('Chapter', ''), 'fields': fields, 'sources': [{'file': filename, 'sheet': sheet.get('name'), 'row': rownum}]}
                    if rownum in formula_images:
                        card['image'] = formula_images[rownum]
                    # Exact duplicates only; distinct rules and alternate formulations remain available.
                    key = json.dumps([card['chapter'], fields], ensure_ascii=False, sort_keys=True)
                    if key in seen:
                        seen[key]['sources'].extend(card['sources'])
                    else:
                        seen[key] = card
                        cards.append(card)
            sources.append(filename)
    typesetting = json.loads((ROOT / 'formula_latex.json').read_text(encoding='utf-8'))
    notes = {
        'C8-012': 'Convention check: this source uses +eBL₃/(2mc), while the orbital coupling uses −eL·B/(2mc). With the same signed charge e and B along +z these signs disagree. Original PDF needed; formula preserved as supplied.',
        'C8-029': 'Unit/sign check: the source gives ωc = eB/m (SI form), while earlier formulas contain Gaussian-unit factors of c. The positive cyclotron frequency is |q|B/m in SI or |q|B/(mc) in Gaussian units. Original PDF needed; formula preserved as supplied.',
        'C9-025': 'This contradiction requires extremal response means ±1. The equality chain alone is satisfied when all means are zero; it is not a contradiction for arbitrary stochastic means.',
    }
    applied = set()
    for card in cards:
        card_id = card['fields'].get('Card ID')
        if card_id in typesetting:
            card['latex'] = typesetting[card_id]
            applied.add(card_id)
        if card_id in notes:
            card['formulaNote'] = notes[card_id]
    if applied != set(typesetting):
        raise ValueError(f'Unmatched typesetting IDs: {set(typesetting) - applied}')
    payload = {'sources': sources, 'cards': cards}
    text = json.dumps(payload, ensure_ascii=False, indent=2).replace('<', '\\u003c')
    (ROOT / 'cards.js').write_text('// Generated by import_cards.py; do not edit by hand.\nwindow.QM_DATA = ' + text + ';\n', encoding='utf-8')
    print(f'Imported {len(cards)} unique cards')
    print(dict(sorted(collections.Counter(c['chapter'] for c in cards).items(), key=lambda x: (not x[0].isdigit(), int(x[0]) if x[0].isdigit() else x[0]))))
    print(f'Formula images: {sum("image" in c for c in cards)}')


if __name__ == '__main__':
    main(Path(sys.argv[1]))
