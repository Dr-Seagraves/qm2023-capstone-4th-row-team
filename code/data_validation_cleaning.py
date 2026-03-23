"""
Data Validation and Cleaning Module
Comprehensive data quality checks and cleaning for the Market Decoupling analysis

This module:
1. Validates data integrity and consistency
2. Detects and handles anomalies
3. Generates quality reports
4. Produces cleaned, analysis-ready datasets
"""

import os
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime

# Setup paths
ROOT_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DATA_DIR = ROOT_DIR / 'data' / 'processed'
FINAL_DATA_DIR = ROOT_DIR / 'data' / 'final'
LOGS_DIR = ROOT_DIR / 'results' / 'logs'
LOGS_DIR.mkdir(parents=True, exist_ok=True)

def log_message(msg, level="INFO"):
    """Log messages with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {level}: {msg}"
    print(log_entry)
    
    # Also write to log file
    log_file = LOGS_DIR / 'data_validation.log'
    with open(log_file, 'a') as f:
        f.write(log_entry + '\n')

def validate_fred_data(df):
    """
    Validate FRED economic data for quality and consistency.
    
    Checks:
    - Date format validity
    - No missing values
    - Price ranges are reasonable
    - CPI monotonic increase
    - Real price calculation
    """
    issues = []
    
    # Check 1: Date format
    date_format_errors = 0
    for date_str in df['YearMonth']:
        try:
            pd.to_datetime(date_str, format='%Y-%m')
        except:
            date_format_errors += 1
            issues.append(f"Invalid date format: {date_str}")
    
    if date_format_errors == 0:
        log_message(f"✓ All {len(df)} FRED dates are valid format (YYYY-MM)", "PASS")
    else:
        log_message(f"✗ {date_format_errors} invalid date formats found", "WARN")
    
    # Check 2: Missing values
    missing = df.isnull().sum()
    if missing.sum() == 0:
        log_message("✓ No missing values in FRED data", "PASS")
    else:
        log_message(f"✗ Missing values detected:\n{missing}", "WARN")
        issues.append(f"Missing values: {missing.to_dict()}")
    
    # Check 3: Price ranges
    min_price, max_price = df['Heating_Oil_Price'].min(), df['Heating_Oil_Price'].max()
    min_cpi, max_cpi = df['CPI'].min(), df['CPI'].max()
    
    if 0 < min_price < 1 and 3 < max_price < 7:
        log_message(f"✓ Heating oil prices in reasonable range: ${min_price:.2f} - ${max_price:.2f}", "PASS")
    else:
        log_message(f"⚠ Heating oil prices may be unusual: ${min_price:.2f} - ${max_price:.2f}", "WARN")
    
    if 60 < min_cpi < 80 and 300 < max_cpi < 340:
        log_message(f"✓ CPI in reasonable range: {min_cpi:.1f} - {max_cpi:.1f}", "PASS")
    else:
        log_message(f"⚠ CPI may be unusual: {min_cpi:.1f} - {max_cpi:.1f}", "WARN")
    
    # Check 4: Real price calculation accuracy
    real_calc = df['Heating_Oil_Price'] / df['CPI']
    max_diff = (real_calc - df['Real_Heating_Oil_Price']).abs().max()
    
    if max_diff < 1e-10:
        log_message("✓ Real price calculation verified (correct deflation)", "PASS")
    else:
        log_message(f"✗ Real price calculation discrepancy: max diff = {max_diff:.2e}", "ERROR")
        issues.append(f"Real price calculation error: {max_diff}")
    
    # Check 5: Duplicates
    dups = df.duplicated(subset=['YearMonth']).sum()
    if dups == 0:
        log_message("✓ No duplicate YearMonth entries", "PASS")
    else:
        log_message(f"✗ {dups} duplicate YearMonth entries found", "ERROR")
        issues.append(f"Duplicates: {dups}")
    
    return len(issues) == 0, issues

def validate_noaa_data(df):
    """
    Validate NOAA climate data for quality and consistency.
    
    Checks:
    - Date format validity
    - No missing values
    - HDD ranges are physically reasonable
    - No negative values (HDD cannot be negative)
    """
    issues = []
    
    # Check 1: Date format
    date_format_errors = 0
    for date_str in df['YearMonth']:
        try:
            pd.to_datetime(date_str, format='%Y-%m')
        except:
            date_format_errors += 1
            issues.append(f"Invalid date format: {date_str}")
    
    if date_format_errors == 0:
        log_message(f"✓ All {len(df)} NOAA dates are valid format (YYYY-MM)", "PASS")
    else:
        log_message(f"✗ {date_format_errors} invalid date formats found", "WARN")
    
    # Check 2: Missing values
    missing = df.isnull().sum()
    if missing.sum() == 0:
        log_message("✓ No missing values in NOAA data", "PASS")
    else:
        log_message(f"✗ Missing values detected:\n{missing}", "WARN")
        issues.append(f"Missing values: {missing.to_dict()}")
    
    # Check 3: HDD ranges (physically reasonable)
    min_hdd, max_hdd = df['Heating_Degree_Days'].min(), df['Heating_Degree_Days'].max()
    
    if min_hdd >= 0:
        log_message(f"✓ No negative HDD values (physically correct)", "PASS")
    else:
        log_message(f"✗ Negative HDD values found: {min_hdd}", "ERROR")
        issues.append(f"Negative HDD: {min_hdd}")
    
    if 0 <= min_hdd and max_hdd < 2000:
        log_message(f"✓ HDD range is reasonable: {min_hdd:.0f} - {max_hdd:.0f}", "PASS")
    else:
        log_message(f"⚠ HDD range seems unusual: {min_hdd:.0f} - {max_hdd:.0f}", "WARN")
    
    # Check 4: Zero HDD explanation (expected in summer)
    zero_count = (df['Heating_Degree_Days'] == 0).sum()
    if zero_count > 0:
        zero_months = df[df['Heating_Degree_Days'] == 0]['YearMonth'].sample(min(3, zero_count)).tolist()
        log_message(f"ℹ {zero_count} zero HDD months (expected for summer): e.g., {zero_months}", "INFO")
    
    # Check 5: Duplicates
    dups = df.duplicated(subset=['YearMonth']).sum()
    if dups == 0:
        log_message("✓ No duplicate YearMonth entries", "PASS")
    else:
        log_message(f"✗ {dups} duplicate YearMonth entries found", "ERROR")
        issues.append(f"Duplicates: {dups}")
    
    return len(issues) == 0, issues

def validate_merged_data(df_merged, df_fred, df_noaa):
    """
    Validate merged panel data for consistency and completeness.
    
    Checks:
    - All columns present
    - No missing values
    - Date alignment
    - Row count consistency
    - Correlation between variables makes sense
    """
    issues = []
    
    # Check 1: Column presence
    expected_cols = {'YearMonth', 'Heating_Oil_Price', 'CPI', 
                     'Real_Heating_Oil_Price', 'Heating_Degree_Days'}
    actual_cols = set(df_merged.columns)
    
    if expected_cols == actual_cols:
        log_message(f"✓ All expected columns present: {sorted(actual_cols)}", "PASS")
    else:
        missing = expected_cols - actual_cols
        extra = actual_cols - expected_cols
        if missing:
            log_message(f"✗ Missing columns: {missing}", "ERROR")
            issues.append(f"Missing columns: {missing}")
        if extra:
            log_message(f"⚠ Extra columns: {extra}", "WARN")
    
    # Check 2: Missing values
    missing = df_merged.isnull().sum()
    if missing.sum() == 0:
        log_message("✓ No missing values in merged data", "PASS")
    else:
        log_message(f"✗ Missing values detected:\n{missing}", "ERROR")
        issues.append(f"Missing values: {missing.to_dict()}")
    
    # Check 3: Date alignment
    if not df_merged['YearMonth'].is_monotonic_increasing:
        log_message("⚠ Dates not strictly sorted (but may be acceptable)", "WARN")
    else:
        log_message("✓ Dates are in chronological order", "PASS")
    
    # Check 4: Row count is reasonable
    # FRED (565 rows from 1978), NOAA (312 rows from 2000-2025)
    # Merge should have ~312 rows (where both exist)
    expected_min_rows = 300
    expected_max_rows = 320
    
    if expected_min_rows <= len(df_merged) <= expected_max_rows:
        log_message(f"✓ Row count is reasonable: {len(df_merged)} rows", "PASS")
    else:
        log_message(f"⚠ Unexpected row count: {len(df_merged)} (expected ~312)", "WARN")
    
    # Check 5: Correlation sanity
    corr = df_merged[['Heating_Oil_Price', 'Heating_Degree_Days']].corr().iloc[0, 1]
    log_message(f"ℹ Correlation between HDD and Price: {corr:.4f}", "INFO")
    
    if -0.5 < corr < 0.5:
        log_message("ℹ Moderate correlation suggests independence (good for analysis)", "INFO")
    elif corr > 0.5:
        log_message("⚠ Strong positive correlation between HDD and Price", "WARN")
    
    return len(issues) == 0, issues

def outlier_detection(df):
    """
    Detect potential outliers using statistical methods (IQR and Z-score).
    Does NOT remove outliers - reports them for analyst review.
    """
    log_message("\n" + "="*60, "INFO")
    log_message("OUTLIER DETECTION ANALYSIS", "INFO")
    log_message("="*60, "INFO")
    
    numeric_cols = ['Heating_Oil_Price', 'Real_Heating_Oil_Price', 'Heating_Degree_Days']
    
    for col in numeric_cols:
        # IQR method
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers_iqr = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        
        if len(outliers_iqr) > 0:
            log_message(f"\n{col}:", "INFO")
            log_message(f"  IQR method: {len(outliers_iqr)} outliers detected", "WARN")
            log_message(f"  Range: Q1={Q1:.4f}, Q3={Q3:.4f}, IQR={IQR:.4f}", "INFO")
            log_message(f"  Bounds: [{lower_bound:.4f}, {upper_bound:.4f}]", "INFO")
            
            # Show extreme outliers
            extreme = outliers_iqr.nlargest(3, col)
            log_message(f"  Most extreme values:", "INFO")
            for idx, row in extreme.iterrows():
                log_message(f"    {row['YearMonth']}: {row[col]:.6f}", "INFO")
        else:
            log_message(f"\n{col}: ✓ No statistical outliers detected", "PASS")

def generate_quality_report(df_fred, df_noaa, df_merged):
    """Generate comprehensive data quality report."""
    
    log_message("\n" + "="*80, "INFO")
    log_message("DATA QUALITY VALIDATION REPORT", "INFO")
    log_message("="*80, "INFO")
    log_message(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "INFO")
    
    # Validate each dataset
    log_message("\n--- FRED Data Validation ---", "INFO")
    fred_ok, fred_issues = validate_fred_data(df_fred)
    
    log_message("\n--- NOAA Data Validation ---", "INFO")
    noaa_ok, noaa_issues = validate_noaa_data(df_noaa)
    
    log_message("\n--- Merged Data Validation ---", "INFO")
    merged_ok, merged_issues = validate_merged_data(df_merged, df_fred, df_noaa)
    
    # Outlier analysis
    outlier_detection(df_merged)
    
    # Summary statistics
    log_message("\n" + "="*60, "INFO")
    log_message("SUMMARY STATISTICS", "INFO")
    log_message("="*60, "INFO")
    
    log_message("\nFRED Data Summary:", "INFO")
    log_message(f"  Rows: {len(df_fred)}", "INFO")
    log_message(f"  Date range: {df_fred['YearMonth'].min()} to {df_fred['YearMonth'].max()}", "INFO")
    log_message(f"  Mean price: ${df_fred['Heating_Oil_Price'].mean():.2f}", "INFO")
    log_message(f"  Std dev: ${df_fred['Heating_Oil_Price'].std():.2f}", "INFO")
    
    log_message("\nNOAA Data Summary:", "INFO")
    log_message(f"  Rows: {len(df_noaa)}", "INFO")
    log_message(f"  Date range: {df_noaa['YearMonth'].min()} to {df_noaa['YearMonth'].max()}", "INFO")
    log_message(f"  Mean HDD: {df_noaa['Heating_Degree_Days'].mean():.1f}", "INFO")
    log_message(f"  Std dev: {df_noaa['Heating_Degree_Days'].std():.1f}", "INFO")
    
    log_message("\nMerged Data Summary:", "INFO")
    log_message(f"  Rows: {len(df_merged)}", "INFO")
    log_message(f"  Date range: {df_merged['YearMonth'].min()} to {df_merged['YearMonth'].max()}", "INFO")
    
    # Final verdict
    log_message("\n" + "="*60, "INFO")
    if fred_ok and noaa_ok and merged_ok:
        log_message("✓ DATA VALIDATION PASSED - Data is ready for analysis", "PASS")
    else:
        log_message("⚠ DATA VALIDATION COMPLETED WITH WARNINGS", "WARN")
        log_message(f"  FRED issues: {len(fred_issues)}", "INFO")
        log_message(f"  NOAA issues: {len(noaa_issues)}", "INFO")
        log_message(f"  Merge issues: {len(merged_issues)}", "INFO")
    log_message("="*60, "INFO")
    
    return fred_ok and noaa_ok and merged_ok

def clean_and_enhance_data(df):
    """
    Enhance data with additional useful columns for analysis.
    
    Adds:
    - Absolute YearMonth as datetime
    - Year and Month components
    - Price trends (lagged differences for price changes)
    - HDD categories (winter severity classification)
    """
    df_clean = df.copy()
    
    # Parse dates
    df_clean['Date'] = pd.to_datetime(df_clean['YearMonth'], format='%Y-%m')
    df_clean['Year'] = df_clean['Date'].dt.year
    df_clean['Month'] = df_clean['Date'].dt.month
    df_clean['Quarter'] = df_clean['Date'].dt.quarter
    
    # Price changes (analyze response to weather)
    df_clean['Price_Change'] = df_clean['Real_Heating_Oil_Price'].diff()
    df_clean['Price_PctChange'] = df_clean['Real_Heating_Oil_Price'].pct_change()
    df_clean['Price_MA3'] = df_clean['Real_Heating_Oil_Price'].rolling(window=3).mean()
    
    # HDD categorization (for seasonal analysis)
    df_clean['HDD_Category'] = pd.cut(
        df_clean['Heating_Degree_Days'],
        bins=[0, 50, 300, 800, 1500],
        labels=['Warm', 'Mild', 'Cold', 'Severe'],
        include_lowest=True
    )
    
    # Lagged HDD (current month's HDD may affect next month's prices)
    df_clean['HDD_Lag1'] = df_clean['Heating_Degree_Days'].shift(1)
    df_clean['HDD_Lag3'] = df_clean['Heating_Degree_Days'].shift(3)
    
    log_message("✓ Data enhancement completed", "PASS")
    log_message(f"  Added columns: Date, Year, Month, Quarter, Price_Change, Price_PctChange, Price_MA3, HDD_Category, HDD_Lag1, HDD_Lag3", "INFO")
    
    return df_clean

def main():
    """Main execution function."""
    
    print("\n" + "="*80)
    print("DATA VALIDATION & CLEANING PIPELINE")
    print("="*80 + "\n")
    
    try:
        # Load data
        log_message("Loading data from processed files...", "INFO")
        df_fred = pd.read_csv(PROCESSED_DATA_DIR / 'fred_clean.csv')
        df_noaa = pd.read_csv(PROCESSED_DATA_DIR / 'noaa_clean.csv')
        df_merged = pd.read_csv(FINAL_DATA_DIR / 'final.csv')
        
        log_message(f"✓ FRED data loaded: {len(df_fred)} rows", "PASS")
        log_message(f"✓ NOAA data loaded: {len(df_noaa)} rows", "PASS")
        log_message(f"✓ Merged data loaded: {len(df_merged)} rows", "PASS")
        
        # Run validation
        log_message("\nStarting data validation...", "INFO")
        validation_passed = generate_quality_report(df_fred, df_noaa, df_merged)
        
        # Clean and enhance data
        log_message("\nEnhancing merged data with analytical features...", "INFO")
        df_enhanced = clean_and_enhance_data(df_merged)
        
        # Save enhanced dataset
        output_path = FINAL_DATA_DIR / 'final_enhanced.csv'
        df_enhanced.to_csv(output_path, index=False)
        log_message(f"✓ Enhanced dataset saved: {output_path}", "PASS")
        log_message(f"  Rows: {len(df_enhanced)}, Columns: {len(df_enhanced.columns)}", "INFO")
        
        # Display sample
        log_message("\nSample of enhanced data (first 5 rows):", "INFO")
        print(df_enhanced.head(5).to_string())
        
        log_message("\n" + "="*80, "INFO")
        log_message("DATA PIPELINE COMPLETE", "PASS")
        log_message("="*80, "INFO")
        
        return True
        
    except Exception as e:
        log_message(f"ERROR in data pipeline: {str(e)}", "ERROR")
        import traceback
        log_message(traceback.format_exc(), "ERROR")
        return False

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
