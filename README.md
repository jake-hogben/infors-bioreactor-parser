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

| Raw name | Database name | Human readable name |
|---|---|---|
| Date Time UTC | `date_time_utc` | Date Time UTC |
| Date Local Time | `date_local_time` | Date Time Local |
| Batch Time, sec | `batch_time_sec` | Batch Time, s |
| *(derived)* | `batch_time_h` | Batch Time, h |
| Batch Time (since inoc.), sec | `eft_sec` | EFT, s |
| *(derived)* | `eft_h` | EFT, h |
| Phase | `phase` | Phase |
| Phase Time, sec | `phase_time_sec` | Phase Time, s |
| Foam, - | `foam` | Foam Sensor |
| AirFlow, l/min | `airflow_lpm` | Airflow, L/min |
| TotalFlow, l/min | `total_flow_lpm` | Total Flow, L/min |
| Gas2Flow, l/min | `gas2_flow_lpm` | Gas 2 Flow, L/min |
| GasMix | `gas_mix` | Gas Mix % |
| Turbidity | `turbidity` | Turbidity |
| Pump1, % | `pump1_pct` | Pump 1, % |
| Pump1.Duration, - | `pump1_duration` | Pump 1 Duration |
| Pump2, % | `pump2_pct` | Pump 2, % |
| Pump2.Duration, - | `pump2_duration` | Pump 2 Duration |
| Pump3, % | `pump3_pct` | Pump 3, % |
| Pump3.Duration, - | `pump3_duration` | Pump 3 Duration |
| Pump4, % | `pump4_pct` | Pump 4, % |
| Pump4.Duration, - | `pump4_duration` | Pump 4 Duration |
| Stirrer, 1/min | `stirrer_rpm` | Stirrer, RPM |
| Temperature, °C | `temperature_degc` | Temperature, C |
| AnalogIO1, % | *(removed)* | (removed) |
| AnalogIO2, % | *(removed)* | (removed) |
| pH, - | `ph` | pH |
| pO2, % | `po2_pct` | DO, % |
| OptekODsensor1.OD | `optek_od` | Optek OD |
| OD600, - | `od600` | OD600 |
| *(added)* | `tank_id` | Tank ID |
| *(added)* | `experiment_id` | Experiment ID |
