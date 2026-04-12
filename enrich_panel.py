"""
enrich_panel.py
---------------
Extends the M1 panel (final.csv) with:
  (a) FRED global commodity controls:
        MCOILWTICO  : WTI Crude Oil Price, $/barrel (monthly)
        MHHNGSP     : Henry Hub Natural Gas Spot Price, $/MMBtu (monthly)
  (b) EIA population-weighted regional HDD (fixes geographic mismatch):
        ZWHD_NEC    : New England Census Division HDD — primary driver
                      (MA, ME, NH, VT, CT, RI — ~75% of U.S. heating oil consumption)
        ZWHDPUS     : U.S. National HDD — robustness check

  The original Boston Logan HDD (Heating_Degree_Days from NOAA, single weather
  station) is kept in the dataset as Boston_HDD for comparison, but NEC_HDD is
  the correct geographic match for a national heating oil price series.

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

# ── Load API keys ─────────────────────────────────────────────────────────────
def load_keys():
    keys = {}
    for fname in ['.env', '.secrets']:
        fpath = Path(fname)
        if not fpath.exists():
            fpath = Path(__file__).parent / fname
        if fpath.exists():
            with open(fpath) as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        k, v = line.strip().split('=', 1)
                        keys[k.strip()] = v.strip()
    return keys

KEYS = load_keys()
FRED_API_KEY = KEYS.get('FRED_API_KEY')
EIA_API_KEY  = KEYS.get('EIA_API_KEY')

if not FRED_API_KEY:
    raise ValueError('FRED_API_KEY not found in .env or .secrets')
if not EIA_API_KEY:
    raise ValueError('EIA_API_KEY not found in .env or .secrets')

# ── FRED fetch ────────────────────────────────────────────────────────────────
FRED_URL = 'https://api.stlouisfed.org/fred/series/observations'

def fetch_fred_monthly(series_id, rename_col):
    """Fetch a FRED monthly series, return YearMonth-indexed DataFrame."""
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
    print(f'  FRED {series_id} ({rename_col}): {len(df)} rows')
    return df

# ── EIA STEO fetch ────────────────────────────────────────────────────────────
EIA_URL = 'https://api.eia.gov/v2/steo/data/'

def fetch_eia_steo(series_id, rename_col, start='2000-01', end='2025-12'):
    """
    Fetch an EIA STEO monthly series, paginating if needed.
    Returns YearMonth-indexed DataFrame with actual historical values only
    (STEO includes forecasts; we cap at end date).
    """
    all_rows = []
    offset = 0
    page_size = 500
    while True:
        params = {
            'api_key': EIA_API_KEY,
            'frequency': 'monthly',
            'data[0]': 'value',
            'facets[seriesId][]': series_id,
            'start': start,
            'end': end,
            'sort[0][column]': 'period',
            'sort[0][direction]': 'asc',
            'length': page_size,
            'offset': offset,
        }
        resp = requests.get(EIA_URL, params=params, timeout=30)
        resp.raise_for_status()
        payload = resp.json()['response']
        rows = payload.get('data', [])
        all_rows.extend(rows)
        if len(rows) < page_size:
            break
        offset += page_size

    df = pd.DataFrame(all_rows)
    df = df.rename(columns={'period': 'YearMonth', 'value': rename_col})
    df[rename_col] = pd.to_numeric(df[rename_col], errors='coerce')
    df = df[['YearMonth', rename_col]].dropna()
    print(f'  EIA STEO {series_id} ({rename_col}): {len(df)} rows  '
          f'[{df["YearMonth"].min()} → {df["YearMonth"].max()}]')
    return df

# ── Fetch all series ──────────────────────────────────────────────────────────
print('Fetching FRED commodity controls...')
wti   = fetch_fred_monthly('MCOILWTICO', 'WTI_Price')
henry = fetch_fred_monthly('MHHNGSP',    'HenryHub_Price')

print('\nFetching EIA population-weighted HDD...')
nec_hdd = fetch_eia_steo('ZWHD_NEC',  'NEC_HDD')   # New England Census Division
us_hdd  = fetch_eia_steo('ZWHDPUS',   'US_HDD')    # U.S. National
mac_hdd = fetch_eia_steo('ZWHD_MAC',  'MAC_HDD')   # Middle Atlantic (NY/NJ/PA)

# ── Load base panel (has Boston_HDD as Heating_Degree_Days) ───────────────────
base = pd.read_csv(FINAL_PANEL)
# Rename legacy single-station column for clarity
base = base.rename(columns={'Heating_Degree_Days': 'Boston_HDD'})
print(f'\nBase panel: {base.shape[0]} rows  ({base["YearMonth"].min()} → {base["YearMonth"].max()})')

# ── Merge all series ──────────────────────────────────────────────────────────
enriched = base.copy()
for df_extra in [wti, henry, nec_hdd, us_hdd, mac_hdd]:
    enriched = enriched.merge(df_extra, on='YearMonth', how='left')

# ── Column order ──────────────────────────────────────────────────────────────
col_order = [
    'YearMonth',
    'Heating_Oil_Price',     # nominal $/gal (FRED APU000072511)
    'CPI',                   # CPIAUCSL index
    'Real_Heating_Oil_Price',# legacy ratio (Nominal/CPI)
    'NEC_HDD',               # PRIMARY DRIVER: EIA New England Census Division HDD
    'US_HDD',                # robustness: EIA national population-weighted HDD
    'MAC_HDD',               # robustness: EIA Middle Atlantic HDD (NY/NJ/PA)
    'Boston_HDD',            # legacy single-station (NOAA, Boston Logan)
    'WTI_Price',             # $/barrel
    'HenryHub_Price',        # $/MMBtu
]
# Add any remaining columns not in col_order
remaining = [c for c in enriched.columns if c not in col_order]
enriched = enriched[col_order + remaining]

print(f'\nEnriched panel: {enriched.shape[0]} rows × {enriched.shape[1]} columns')
print(f'NAs per column:\n{enriched.isna().sum().to_string()}')
print(f'\nFirst 3 rows:\n{enriched.head(3).to_string()}')

# ── Save ──────────────────────────────────────────────────────────────────────
out = FINAL_DIR / 'final_enriched.csv'
enriched.to_csv(out, index=False)
print(f'\nSaved → {out}')
print(f'Columns: {list(enriched.columns)}')
