import os
from pathlib import Path
import requests
import pandas as pd

# --- Load API Keys from .secrets ---
def load_api_keys():
    root_dir = Path(__file__).resolve().parent.parent
    secrets_path = root_dir / '.secrets'
    keys = {}
    with open(secrets_path) as f:
        for line in f:
            if '=' in line:
                k, v = line.strip().split('=', 1)
                keys[k] = v
    return keys['FRED_API_KEY'], keys['NOAA_API_TOKEN']

FRED_API_KEY, NOAA_API_TOKEN = load_api_keys()

# --- Setup Paths & Directories ---
ROOT_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DATA_DIR = ROOT_DIR / 'data' / 'processed'
FINAL_DATA_DIR = ROOT_DIR / 'data' / 'final'
for d in [PROCESSED_DATA_DIR, FINAL_DATA_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# --- Fetch FRED Data ---
FRED_URL = 'https://api.stlouisfed.org/fred/series/observations'
def fetch_fred_series(series_id):
    params = {
        'series_id': series_id,
        'api_key': FRED_API_KEY,
        'file_type': 'json',
        'frequency': 'm'
    }
    response = requests.get(FRED_URL, params=params)
    response.raise_for_status()
    data = response.json()['observations']
    df = pd.DataFrame(data)
    df = df[df['value'] != '.']
    df = df[['date', 'value']]
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    return df

df_oil = fetch_fred_series('APU000072511')
df_cpi = fetch_fred_series('CPIAUCSL')
df_fred = pd.merge(df_oil, df_cpi, on='date', suffixes=('_Nominal', '_CPI'))
df_fred['YearMonth'] = pd.to_datetime(df_fred['date']).dt.strftime('%Y-%m')
df_fred['Real_Heating_Oil_Price'] = df_fred['value_Nominal'] / df_fred['value_CPI']
df_fred = df_fred.rename(columns={'value_Nominal': 'Heating_Oil_Price', 'value_CPI': 'CPI'})
df_fred = df_fred[['YearMonth', 'Heating_Oil_Price', 'CPI', 'Real_Heating_Oil_Price']]
df_fred.to_csv(PROCESSED_DATA_DIR / 'fred_clean.csv', index=False)
print(f"Saved cleaned FRED data: {len(df_fred)} rows.")

# --- Fetch NOAA Data ---
NOAA_URL = 'https://www.ncei.noaa.gov/cdo-web/api/v2/data'
headers = {'token': NOAA_API_TOKEN}
station_id = 'GHCND:USW00014739'
date_ranges = [
    ('2000-01-01', '2009-12-31'),
    ('2010-01-01', '2019-12-31'),
    ('2020-01-01', '2025-12-31')
]
all_data = []
for start, end in date_ranges:
    params = {
        'datasetid': 'GSOM',
        'datatypeid': 'HTDD',
        'stationid': station_id,
        'startdate': start,
        'enddate': end,
        'limit': 1000,
        'units': 'standard'
    }
    response = requests.get(NOAA_URL, headers=headers, params=params)
    response.raise_for_status()
    chunk = response.json().get('results', [])
    print(f"Fetched {len(chunk)} rows for {start} to {end} at Boston Logan")
    all_data.extend(chunk)
df_noaa = pd.DataFrame(all_data)
if not df_noaa.empty:
    df_noaa = df_noaa[['date', 'value']]
    df_noaa['YearMonth'] = pd.to_datetime(df_noaa['date']).dt.strftime('%Y-%m')
    df_noaa = df_noaa.rename(columns={'value': 'Heating_Degree_Days'})
    df_noaa = df_noaa[['YearMonth', 'Heating_Degree_Days']]
else:
    print("WARNING: No NOAA data returned.")
df_noaa.to_csv(PROCESSED_DATA_DIR / 'noaa_clean.csv', index=False)
print(f"Saved cleaned NOAA data: {len(df_noaa)} rows.")

# --- Merge for Analysis-Ready Panel ---
panel = pd.merge(df_fred, df_noaa, on='YearMonth', how='outer')
panel = panel.dropna(subset=['Heating_Degree_Days', 'Real_Heating_Oil_Price'])
panel = panel.sort_values('YearMonth').reset_index(drop=True)
print(f"Final panel shape: {panel.shape}")
print(panel.head())
output_path = FINAL_DATA_DIR / 'final.csv'
panel.to_csv(output_path, index=False)
print(f"Saved merged panel to {output_path}")
print("Pipeline execution complete.")
