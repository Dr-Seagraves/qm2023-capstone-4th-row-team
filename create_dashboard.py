"""
create_dashboard.py
-------------------
Generates a self-contained interactive HTML dashboard for the M2 EDA.
Run this script from the project root:

    python create_dashboard.py

Output: results/dashboard.html  (open in any browser — no server needed)

Requires: plotly  (pip install plotly)
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
import warnings
warnings.filterwarnings('ignore')

# ── Paths ──────────────────────────────────────────────────────────────────────
sys.path.insert(0, str(Path('.').resolve()))
from config_paths import FINAL_PANEL, RESULTS_DIR

try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    import plotly.io as pio
except ImportError:
    print('ERROR: plotly not installed.  Run: pip install plotly')
    sys.exit(1)

OUTPUT_HTML = RESULTS_DIR / 'dashboard.html'

# ── Load & prepare data ───────────────────────────────────────────────────────
df = pd.read_csv(FINAL_PANEL)
df['YearMonth'] = pd.to_datetime(df['YearMonth'], format='%Y-%m')
df = df.sort_values('YearMonth').reset_index(drop=True)

CPI_2020_REF = df.loc[df['YearMonth'].dt.year == 2020, 'CPI'].mean()
df['Real_Price_2020'] = df['Heating_Oil_Price'] * (CPI_2020_REF / df['CPI'])
df['Month'] = df['YearMonth'].dt.month
df['Year']  = df['YearMonth'].dt.year
for lag in [1, 2, 3, 6, 12]:
    df[f'HDD_lag{lag}'] = df['Heating_Degree_Days'].shift(lag)
df['Price_lag1'] = df['Real_Price_2020'].shift(1)
df['Roll_corr_24'] = df['Real_Price_2020'].rolling(24).corr(df['Heating_Degree_Days'])

def assign_period(yr):
    if yr <= 2007:   return 'Pre-Crisis (2000-07)'
    elif yr <= 2014: return 'Post-GFC (2008-14)'
    elif yr <= 2019: return 'Shale Era (2015-19)'
    elif yr <= 2021: return 'COVID (2020-21)'
    else:            return 'Recovery (2022-24)'

df['Period'] = df['Year'].apply(assign_period)

PERIOD_ORDER = ['Pre-Crisis (2000-07)', 'Post-GFC (2008-14)',
                'Shale Era (2015-19)', 'COVID (2020-21)', 'Recovery (2022-24)']
COLORS = px.colors.qualitative.Plotly

# ── Seasonal decomposition ────────────────────────────────────────────────────
ts = df.set_index('YearMonth')['Real_Price_2020'].dropna()
decomp = seasonal_decompose(ts, model='additive', period=12)

# ══════════════════════════════════════════════════════════════════════════════
# BUILD DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
print('Building interactive dashboard...')

# ── Chart 1: Time Series ──────────────────────────────────────────────────────
fig_ts = go.Figure()
fig_ts.add_trace(go.Scatter(
    x=df['YearMonth'], y=df['Real_Price_2020'],
    mode='lines', name='Real Price (2020 $/gal)',
    line=dict(color='#1f77b4', width=2),
    fill='tozeroy', fillcolor='rgba(31,119,180,0.08)',
    hovertemplate='%{x|%Y-%m}<br>Real Price: $%{y:.2f}/gal<extra></extra>'
))
roll = df['Real_Price_2020'].rolling(12, center=True).mean()
fig_ts.add_trace(go.Scatter(
    x=df['YearMonth'], y=roll,
    mode='lines', name='12-month rolling mean',
    line=dict(color='darkred', width=2.5, dash='dash'),
    hovertemplate='%{x|%Y-%m}<br>Rolling Mean: $%{y:.2f}/gal<extra></extra>'
))
# Event annotations
events_ts = [
    ('2008-07', 'Oil Peak 2008', 'above'),
    ('2009-02', 'GFC Trough',    'below'),
    ('2014-12', 'Shale Glut',    'below'),
    ('2020-04', 'COVID Crash',   'below'),
    ('2022-06', 'Ukraine War',   'above'),
]
for date_str, label, pos in events_ts:
    d = pd.Timestamp(date_str)
    idx = (df['YearMonth'] - d).abs().idxmin()
    y = df.loc[idx, 'Real_Price_2020']
    ay = -50 if pos == 'above' else 50
    fig_ts.add_annotation(x=d, y=y, text=label, showarrow=True, arrowhead=2,
                          ay=ay, font=dict(size=10), bgcolor='white', bordercolor='gray')
fig_ts.update_layout(
    title='Real Heating Oil Price (2020 Constant $/gallon), 2000–2024',
    xaxis_title='Date', yaxis_title='Real Price (2020 $/gal)',
    legend=dict(x=0.01, y=0.99), hovermode='x unified',
    template='plotly_white', height=420
)

# ── Chart 2: Dual-Axis ────────────────────────────────────────────────────────
fig_dual = make_subplots(specs=[[{'secondary_y': True}]])
fig_dual.add_trace(go.Scatter(
    x=df['YearMonth'], y=df['Real_Price_2020'],
    name='Real Price (2020 $/gal)', line=dict(color='#1f77b4', width=2),
    hovertemplate='%{x|%Y-%m}<br>Price: $%{y:.2f}<extra></extra>'
), secondary_y=False)
fig_dual.add_trace(go.Bar(
    x=df['YearMonth'], y=df['Heating_Degree_Days'],
    name='HDD (Boston Logan)', marker_color='rgba(255,127,14,0.35)',
    hovertemplate='%{x|%Y-%m}<br>HDD: %{y:.0f}<extra></extra>'
), secondary_y=True)
fig_dual.update_layout(
    title='Dual-Axis: Real Heating Oil Price vs. Heating Degree Days (2000–2024)',
    xaxis_title='Date', hovermode='x unified',
    template='plotly_white', height=440, barmode='overlay',
    legend=dict(x=0.01, y=0.99)
)
fig_dual.update_yaxes(title_text='Real Price (2020 $/gal)', secondary_y=False)
fig_dual.update_yaxes(title_text='Heating Degree Days — Boston Logan', secondary_y=True)

# ── Chart 3: Lag Correlation ──────────────────────────────────────────────────
lags = [0, 1, 2, 3, 6, 12]
lag_corrs = [df['Real_Price_2020'].corr(df['Heating_Degree_Days'].shift(l)) for l in lags]
opt_idx = int(np.argmax(np.abs(lag_corrs)))
bar_colors = ['gold' if i == opt_idx else '#1f77b4' for i in range(len(lags))]

fig_lag = go.Figure(go.Bar(
    x=[str(l) for l in lags], y=lag_corrs,
    marker_color=bar_colors, marker_line_color='black', marker_line_width=1,
    text=[f'{r:+.3f}' for r in lag_corrs], textposition='outside',
    hovertemplate='Lag %{x} months<br>r = %{y:.4f}<extra></extra>'
))
fig_lag.add_hline(y=0, line_color='black', line_width=1)
fig_lag.add_hline(y=0.15,  line_dash='dot', line_color='gray', opacity=0.6)
fig_lag.add_hline(y=-0.15, line_dash='dot', line_color='gray', opacity=0.6)
fig_lag.add_annotation(
    text=f'Optimal lag: {lags[opt_idx]}mo  (r={lag_corrs[opt_idx]:+.3f})',
    xref='paper', yref='paper', x=0.98, y=0.95, showarrow=False,
    bgcolor='lightyellow', bordercolor='goldenrod', font=dict(size=11)
)
fig_lag.update_layout(
    title='HDD–Real Price Correlation by Lag (0–12 months)',
    xaxis_title='HDD Lag (months before price)', yaxis_title='Pearson r',
    template='plotly_white', height=420,
    yaxis=dict(range=[-0.8, 0.8])
)

# ── Chart 4: Rolling Correlation ──────────────────────────────────────────────
fig_roll = go.Figure()
fig_roll.add_trace(go.Scatter(
    x=df['YearMonth'], y=df['Roll_corr_24'],
    mode='lines', name='Rolling 24-month r',
    line=dict(color='#2ca02c', width=2),
    fill='tozeroy', fillcolor='rgba(44,160,44,0.10)',
    hovertemplate='%{x|%Y-%m}<br>r = %{y:.3f}<extra></extra>'
))
fig_roll.add_hline(y=0,    line_color='black', line_width=1)
fig_roll.add_hline(y=0.3,  line_dash='dash', line_color='gray', opacity=0.5)
fig_roll.add_hline(y=-0.3, line_dash='dash', line_color='gray', opacity=0.5)
# Shade crisis periods
crisis_periods = [
    ('2008-01', '2009-12', 'rgba(255,100,100,0.15)', 'GFC'),
    ('2014-07', '2016-06', 'rgba(100,200,100,0.15)', 'Shale Glut'),
    ('2020-01', '2021-12', 'rgba(100,100,255,0.15)', 'COVID'),
]
for s, e, color, label in crisis_periods:
    fig_roll.add_vrect(x0=pd.Timestamp(s), x1=pd.Timestamp(e),
                       fillcolor=color, layer='below', line_width=0,
                       annotation_text=label, annotation_position='top left',
                       annotation_font_size=10)
fig_roll.update_layout(
    title='Rolling 24-Month Correlation: Real Price & HDD — How the Relationship Has Evolved',
    xaxis_title='Date', yaxis_title='Rolling Pearson r (24-month window)',
    yaxis=dict(range=[-1.1, 1.1]),
    template='plotly_white', height=420, hovermode='x unified'
)

# ── Chart 5: Period Scatter (coloured by regime) ──────────────────────────────
fig_scatter = px.scatter(
    df.dropna(subset=['Heating_Degree_Days', 'Real_Price_2020']),
    x='Heating_Degree_Days', y='Real_Price_2020',
    color='Period', category_orders={'Period': PERIOD_ORDER},
    color_discrete_sequence=COLORS,
    trendline='ols',
    labels={'Heating_Degree_Days': 'HDD (Boston Logan)',
            'Real_Price_2020': 'Real Price (2020 $/gal)',
            'Period': 'Economic Regime'},
    title='HDD vs. Real Price — Colored by Economic Regime (with OLS trend lines)',
    hover_data={'YearMonth': '|%Y-%m'},
    opacity=0.55,
    height=500
)
fig_scatter.update_layout(template='plotly_white')

# ── Chart 6: Decomposition ───────────────────────────────────────────────────
fig_decomp = make_subplots(
    rows=4, cols=1, shared_xaxes=True,
    subplot_titles=['Observed', 'Trend', 'Seasonal', 'Residual'],
    vertical_spacing=0.07
)
decomp_traces = [
    (ts,              '#1f77b4', 1),
    (decomp.trend,    '#ff7f0e', 2),
    (decomp.seasonal, '#2ca02c', 3),
    (decomp.resid,    '#d62728', 4),
]
for data, color, row in decomp_traces:
    if row == 4:
        fig_decomp.add_trace(go.Bar(
            x=data.index, y=data.values,
            marker_color=color, marker_opacity=0.55,
            name='Residual', showlegend=False,
            hovertemplate='%{x|%Y-%m}<br>Residual: %{y:.3f}<extra></extra>'
        ), row=row, col=1)
    else:
        fig_decomp.add_trace(go.Scatter(
            x=data.index, y=data.values,
            line=dict(color=color, width=1.8),
            mode='lines', showlegend=False,
            hovertemplate=f'%{{x|%Y-%m}}<br>Value: $%{{y:.3f}}<extra></extra>'
        ), row=row, col=1)
fig_decomp.update_layout(
    title='Additive Seasonal Decomposition — Real Heating Oil Price (Period = 12 months)',
    height=700, template='plotly_white', hovermode='x unified'
)
fig_decomp.update_yaxes(title_text='$/gal', row=1, col=1)
fig_decomp.update_xaxes(title_text='Date', row=4, col=1)

# ══════════════════════════════════════════════════════════════════════════════
# ASSEMBLE HTML
# ══════════════════════════════════════════════════════════════════════════════
html_parts = []
html_parts.append("""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>QM2023 Capstone M2 — EDA Dashboard</title>
  <style>
    body { font-family: 'Segoe UI', Arial, sans-serif; background: #f5f6fa;
           color: #222; margin: 0; padding: 0; }
    header { background: #1a237e; color: white; padding: 28px 40px 20px; }
    header h1 { margin: 0 0 6px; font-size: 1.7rem; }
    header p  { margin: 0; opacity: 0.85; font-size: 0.95rem; }
    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px;
            padding: 28px 40px; max-width: 1600px; margin: 0 auto; }
    .card { background: white; border-radius: 10px; padding: 18px 20px 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08); }
    .card.full { grid-column: 1 / -1; }
    .card h3 { margin: 0 0 4px; font-size: 1.0rem; color: #1a237e; }
    .caption { font-size: 0.82rem; color: #555; margin-top: 8px;
               border-left: 3px solid #1a237e; padding-left: 10px; line-height: 1.55; }
    footer { text-align: center; padding: 20px; color: #888; font-size: 0.82rem; }
  </style>
</head>
<body>
<header>
  <h1>QM 2023 Capstone &mdash; Milestone 2: EDA Dashboard</h1>
  <p>Real Heating Oil Prices &amp; Winter Severity (2000&ndash;2024) &nbsp;|&nbsp;
     Boston Logan HDD &times; FRED National Average Price &nbsp;|&nbsp;
     <em>4th Row Team</em></p>
</header>
<div class="grid">
""")

def card(title, fig, caption, full=False):
    cls = 'card full' if full else 'card'
    chart_html = pio.to_html(fig, full_html=False, include_plotlyjs=False,
                             config={'displayModeBar': True, 'responsive': True})
    return f"""
  <div class="{cls}">
    <h3>{title}</h3>
    {chart_html}
    <p class="caption">{caption}</p>
  </div>
"""

html_parts.append(card(
    'Figure 2: Real Heating Oil Price Over Time',
    fig_ts,
    'CPI-deflated prices in 2020 constant dollars reveal the full commodity super-cycle: '
    'surge (2000–2008), GFC collapse, shale-era decline (2015–19), COVID crash, '
    'and Ukraine-war spike (2022). Global supply shocks dominate the price level.',
    full=True
))
html_parts.append(card(
    'Figure 3: Dual-Axis — Real Price vs. HDD',
    fig_dual,
    'Orange bars show monthly HDD (right axis); blue line shows real price (left axis). '
    'HDD has reliable winter spikes, but prices follow global crude cycles, '
    'suggesting local demand is only a partial driver.',
))
html_parts.append(card(
    'Figure 4: HDD–Price Correlation by Lag',
    fig_lag,
    'Bar chart of Pearson r at lags 0–12 months. Gold bar = optimal lag for M3 regression. '
    'Correlation weakens at long lags, consistent with short-lived demand-side effects.',
))
html_parts.append(card(
    'Figure 5: Rolling 24-Month Correlation',
    fig_roll,
    'The HDD–price relationship is time-varying. During global supply shocks (shaded), '
    'the correlation collapses — confirming that globalization intermittently severs the '
    'winter–price link. M3 should include a supply-shock interaction term.',
    full=True
))
html_parts.append(card(
    'Figure 7: HDD vs. Real Price by Economic Regime',
    fig_scatter,
    'Scatter colored by regime with per-regime OLS trend lines. The Post-GFC and Shale '
    'eras show different slopes, supporting structural break testing in M3.',
    full=True
))
html_parts.append(card(
    'Figure 8: Seasonal Decomposition',
    fig_decomp,
    'Additive decomposition (period = 12). Trend dominates; seasonal component is real but '
    'secondary. Residuals show large outliers in 2008 and 2022 — warrant robust S.E. in M3.',
    full=True
))

html_parts.append("""
</div>
<footer>
  QM 2023 Capstone &mdash; Milestone 2 EDA Dashboard &nbsp;&bull;&nbsp;
  Data: FRED (APU000072511, CPIAUCSL) &amp; NOAA GSOM (Boston Logan WBAN:14739) &nbsp;&bull;&nbsp;
  Generated with Python + Plotly
</footer>
</body>
</html>""")

# Inject plotly.js once at the top
PLOTLY_JS = pio.to_html(go.Figure(), full_html=False, include_plotlyjs='cdn')
# Actually embed cdn script tag directly
CDN_SCRIPT = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>'
full_html = CDN_SCRIPT + '\n' + ''.join(html_parts)

OUTPUT_HTML.write_text(full_html, encoding='utf-8')
print(f'\nDashboard saved -> {OUTPUT_HTML}')
print('Open in any browser (no server required).')
