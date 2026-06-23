#!/usr/bin/env python3
"""
Infors Bioreactor CSV Parser

Reads a raw Infors bioreactor export and produces a clean, database-ready CSV.
"""

import os
import sys
import pandas as pd


COLUMN_RENAME = {
    'Date Time UTC':                 'date_time_utc',
    'Date Local Time':               'date_local_time',
    'Batch Time, sec':               'batch_time_sec',
    'Batch Time (since inoc.), sec': 'eft_sec',
    'Phase':                         'phase',
    'Phase Time, sec':               'phase_time_sec',
    'Foam, -':                       'foam',
    'AirFlow, l/min':                'airflow_lpm',
    'TotalFlow, l/min':              'total_flow_lpm',
    'Gas2Flow, l/min':               'gas2_flow_lpm',
    'GasMix':                        'gas_mix',
    'Turbidity':                     'turbidity',
    'Pump1, %':                      'pump1_pct',
    'Pump1.Duration, -':             'pump1_duration',
    'Pump2, %':                      'pump2_pct',
    'Pump2.Duration, -':             'pump2_duration',
    'Pump3, %':                      'pump3_pct',
    'Pump3.Duration, -':             'pump3_duration',
    'Pump4, %':                      'pump4_pct',
    'Pump4.Duration, -':             'pump4_duration',
    'Stirrer, 1/min':                'stirrer_rpm',
    'pH, -':                         'ph',
    'pO2, %':                        'po2_pct',
    'OptekODsensor1.OD':             'optek_od',
    'OD600, -':                      'od600',
}

COLUMN_ORDER = [
    'date_time_utc',
    'date_local_time',
    'batch_time_sec',
    'batch_time_h',
    'eft_sec',
    'eft_h',
    'phase',
    'phase_time_sec',
    'foam',
    'airflow_lpm',
    'total_flow_lpm',
    'gas2_flow_lpm',
    'gas_mix',
    'turbidity',
    'pump1_pct',
    'pump1_duration',
    'pump2_pct',
    'pump2_duration',
    'pump3_pct',
    'pump3_duration',
    'pump4_pct',
    'pump4_duration',
    'stirrer_rpm',
    'temperature_degc',
    'ph',
    'po2_pct',
    'optek_od',
    'od600',
    'tank_id',
    'experiment_id',
]


def read_raw(path: str) -> pd.DataFrame:
    """Read the raw Infors CSV, skipping the version/locale header line."""
    for enc in ('utf-8', 'latin-1', 'cp1252'):
        try:
            df = pd.read_csv(path, sep=';', skiprows=1, encoding=enc)
            return df
        except (UnicodeDecodeError, pd.errors.ParserError):
            continue
    raise ValueError(f"Could not read {path} with any supported encoding.")


def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Drop AnalogIO columns and rename remaining columns to snake_case."""
    analog_cols = [c for c in df.columns if 'analogio' in c.lower()]
    df = df.drop(columns=analog_cols)

    # Detect temperature column regardless of degree-sign encoding
    temp_col = next((c for c in df.columns if c.lower().startswith('temperature')), None)
    rename = dict(COLUMN_RENAME)
    if temp_col and temp_col not in rename:
        rename[temp_col] = 'temperature_degc'

    return df.rename(columns=rename)


def add_derived_columns(df: pd.DataFrame, tank_id: str, experiment_id: str) -> pd.DataFrame:
    """Add batch_time_h, eft_h, tank_id, and experiment_id."""
    df['batch_time_h'] = pd.to_numeric(df['batch_time_sec'], errors='coerce') / 3600
    df['eft_h'] = pd.to_numeric(df['eft_sec'], errors='coerce') / 3600
    df['tank_id'] = tank_id
    df['experiment_id'] = experiment_id
    return df


def reorder_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Place columns in logical order; any unexpected extras go at the end."""
    ordered = [c for c in COLUMN_ORDER if c in df.columns]
    extras = [c for c in df.columns if c not in COLUMN_ORDER]
    return df[ordered + extras]


def parse(input_path: str, output_path: str = None) -> str:
    """Run the full parse pipeline. Returns the path of the output file."""
    print(f"\nInput:  {input_path}")
    tank_id = input("Tank ID (e.g. R1):           ").strip()
    experiment_id = input("Experiment ID (e.g. PD-0001): ").strip()

    df = read_raw(input_path)
    df = clean_columns(df)
    df = add_derived_columns(df, tank_id, experiment_id)
    df = reorder_columns(df)

    if output_path is None:
        stem = os.path.splitext(input_path)[0]
        output_path = f"{stem}_parsed.csv"

    df.to_csv(output_path, index=False)
    print(f"Output: {output_path}  ({len(df)} rows)")
    return output_path


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python parse_bioreactor.py <raw_export.csv> [output.csv]")
        sys.exit(1)

    parse(
        input_path=sys.argv[1],
        output_path=sys.argv[2] if len(sys.argv) > 2 else None,
    )
