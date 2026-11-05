#!/usr/bin/env python3
"""Rebuild the explorer page from the CSV.

    python3 scripts/build_explorer.py                  # data/ai_model_releases.csv -> docs/index.html
    python3 scripts/build_explorer.py --csv my.csv --html docs/index.html

The explorer (docs/index.html) is one self-contained page with the dataset embedded as a JSON
array (`const D=[...]`). This script replaces that array with the rows of the CSV, so you can
edit or extend the CSV, rebuild, and open the page. Needs only Python 3.8+, no packages.
Empty CSV cells become null ("not verified"), never zero.
"""
import argparse, csv, json, sys
from pathlib import Path

# page key -> CSV column
MAP = {
    'id': 'model_id', 'dev': 'developer', 'name': 'model', 'st': 'stage_at_launch',
    'counted': 'counted_strict', 'cd': 'count_date', 'cb': 'count_basis', 'why': 'reason_not_counted',
    'ci': 'count_date_any_stage', 'an': 'announced', 'fa': 'first_available', 'ga': 'general_availability',
    'api': 'api_available', 'wt': 'open_weights', 'stat': 'status', 'ret': 'retired_on', 'rep': 'replaced_by',
    'ctx': 'context_window_tokens', 'mx': 'max_output_tokens', 'ck': 'knowledge_cutoff',
    'pi': 'input_usd_per_1m_tokens', 'pc': 'cached_input_usd_per_1m_tokens', 'po': 'output_usd_per_1m_tokens',
    'lic': 'licence', 'pt': 'params_total_billions', 'pa': 'params_active_billions', 'ar': 'architecture',
    'mi': 'input_modalities', 'rm': 'reasoning_mode', 'plat': 'platforms', 'apiid': 'api_model_id',
    'snap': 'variant_of', 'src': 'vendor_page', 'card': 'model_card', 'conf': 'confidence',
    'unv': 'unverified', 'note': 'notes',
}
NUMERIC = {'pi', 'pc', 'po', 'ctx', 'mx', 'pt', 'pa', 'counted', 'unv'}


def value(key, raw):
    raw = (raw or '').strip()
    if raw == '':
        return None
    if key in NUMERIC:
        try:
            f = float(raw.replace(',', ''))
            return int(f) if f == int(f) else f
        except ValueError:
            return raw
    return raw


def main():
    root = Path(__file__).resolve().parent.parent
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--csv', default=str(root / 'data' / 'ai_model_releases.csv'))
    ap.add_argument('--html', default=str(root / 'docs' / 'index.html'))
    a = ap.parse_args()
    with open(a.csv, encoding='utf-8', newline='') as f:
        rows = list(csv.DictReader(f))
    missing = [c for c in MAP.values() if rows and c not in rows[0]]
    if missing:
        sys.exit('CSV is missing columns: ' + ', '.join(missing))
    data = [{k: value(k, r[c]) for k, c in MAP.items()} for r in rows]
    html = Path(a.html).read_text(encoding='utf-8')
    start = html.index('const D=[')
    end = html.index('];\nconst G=', start)
    out = html[:start] + 'const D=' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + html[end + 1:]
    Path(a.html).write_text(out, encoding='utf-8')
    print(f'{len(data)} models written to {a.html}')


if __name__ == '__main__':
    main()
