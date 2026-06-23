# infors-bioreactor-parser

Transforms raw Infors bioreactor CSV exports into a clean, database-ready format.

## What it does

- Skips the Infors version/locale header line
- Renames all columns to `snake_case` database-safe names
- Adds `batch_time_h` (batch time in hours) and `eft_h` (elapsed fermentation time in hours)
- Removes `AnalogIO1` and `AnalogIO2` columns
- Prompts for `tank_id` and `experiment_id`, fills every row with the provided values
- Outputs standard comma-separated CSV

## Usage

```bash
pip install -r requirements.txt
python parse_bioreactor.py "Raw file.csv"
# or specify an output path:
python parse_bioreactor.py "Raw file.csv" "Parsed file.csv"
```

You will be prompted for:
- **Tank ID** – e.g. `R1`, `R2`
- **Experiment ID** – e.g. `PD-0001`

## Column mapping

| Raw name | Database name |
|---|---|
| Date Time UTC | `date_time_utc` |
| Date Local Time | `date_local_time` |
| Batch Time, sec | `batch_time_sec` |
| *(derived)* | `batch_time_h` |
| Batch Time (since inoc.), sec | `eft_sec` |
| *(derived)* | `eft_h` |
| Phase | `phase` |
| Phase Time, sec | `phase_time_sec` |
| Foam, - | `foam` |
| AirFlow, l/min | `airflow_lpm` |
| TotalFlow, l/min | `total_flow_lpm` |
| Gas2Flow, l/min | `gas2_flow_lpm` |
| GasMix | `gas_mix` |
| Turbidity | `turbidity` |
| Pump1, % | `pump1_pct` |
| Pump1.Duration, - | `pump1_duration` |
| Pump2, % | `pump2_pct` |
| Pump2.Duration, - | `pump2_duration` |
| Pump3, % | `pump3_pct` |
| Pump3.Duration, - | `pump3_duration` |
| Pump4, % | `pump4_pct` |
| Pump4.Duration, - | `pump4_duration` |
| Stirrer, 1/min | `stirrer_rpm` |
| Temperature, °C | `temperature_degc` |
| AnalogIO1, % | *(removed)* |
| AnalogIO2, % | *(removed)* |
| pH, - | `ph` |
| pO2, % | `po2_pct` |
| OptekODsensor1.OD | `optek_od` |
| OD600, - | `od600` |
| *(added)* | `tank_id` |
| *(added)* | `experiment_id` |
