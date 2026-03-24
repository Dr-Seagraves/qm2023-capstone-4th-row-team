"""
enrich_panel.py
---------------
Extends the M1 panel (final.csv) with additional FRED series:
  - MCOILWTICO  : WTI Crude Oil Price, $/barrel (monthly)
  - MHHNGSP     : Henry Hub Natural Gas Spot Price, $/MMBtu (monthly)

These two global/national commodity prices let us decompose heating oil price
variance into:
  (a) Global crude oil component  (WTI)
  (b) Natural gas substitute pressure (Henry Hub)
  (c) Residual local demand premium  (explained by HDD)

Output: data/final/final_enriched.csv

Usage:
    python enrich_panel.py
"""

import sys
from pathlib import Path
import requests
import pandas as pd

sys.path.insert(0, str(Path('.').resolve()))
from config_paths import FINAL_PANEL, FINAL_DIR

# ── Load API key from .secrets ────────────────────────────────────────────────
def load_fred_key():
    secrets_path = Path('.secrets')
    if not secrets_path.exists():
        secrets_path = Path(__file__).parent / '.secrets'
    with open(secrets_path) as f:
        for line in f:
            if '=' in line:
                k, v = line.strip().split('=', 1)
                if k.strip() == 'FRED_API_KEY':
                    return v.strip()
    raise ValueError('FRED_API_KEY not found in .secrets')

FRED_API_KEY = load_fred_key()
FRED_URL = 'https://api.stlouisfed.org/fred/series/observations'

def fetch_fred_monthly(series_id, rename_col):
    """Fetch a FRED monthly series and return a YearMonth-indexed DataFrame."""
    params = {
        'series_id': series_id,
        'api_key': FRED_API_KEY,
        'file_type': 'json',
        'frequency': 'm',
        'observation_start': '2000-01-01',
    }
    resp = requests.get(FRED_URL, params=params, timeout=30)
    resp.raise_for_status()
    obs = resp.json()['observations']
    df = pd.DataFrame(obs)
    df = df[df['value'] != '.']
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    df['YearMonth'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m')
    df = df.rename(columns={'value': rename_col})[['YearMonth', rename_col]]
    print(f'  {series_id} ({rename_col}): {len(df)} rows')
    return df

print('Fetching additional FRED series...')
wti      = fetch_fred_monthly('MCOILWTICO', 'WTI_Price')       # $/barrel
henry    = fetch_fred_monthly('MHHNGSP',    'HenryHub_Price')   # $/MMBtu

# ── Load base panel ───────────────────────────────────────────────────────────
base = pd.read_csv(FINAL_PANEL)
print(f'\nBase panel: {base.shape[0]} rows')

# ── Merge ─────────────────────────────────────────────────────────────────────
enriched = base.merge(wti,   on='YearMonth', how='left')
enriched = enriched.merge(henry, on='YearMonth', how='left')

print(f'Enriched panel: {enriched.shape[0]} rows x {enriched.shape[1]} columns')
print(f'Missing WTI:       {enriched["WTI_Price"].isna().sum()}')
print(f'Missing Henry Hub: {enriched["HenryHub_Price"].isna().sum()}')
print(enriched.tail(5).to_string())

# ── Save ──────────────────────────────────────────────────────────────────────
out = FINAL_DIR / 'final_enriched.csv'
enriched.to_csv(out, index=False)
print(f'\nSaved -> {out}')
print('Columns:', list(enriched.columns))
