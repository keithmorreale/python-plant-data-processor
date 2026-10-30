# Linux/Python Plant Dataset Filter — Portfolio Demonstration

A runnable, **standard-library-only** Python CLI for streaming large CSV datasets, applying configurable botanical trait thresholds, and writing auditable classification results.

**This is a demonstration using synthetic examples, not paid client work or verified plant-growth research.** The tool does not scrape the internet or look up live botanical traits. That requires a separately scoped, licensed data source or API.

## Features
- Streams rows instead of loading the full dataset into memory
- Configurable growth, height and sunlight qualification rules
- Writes `QUALIFIED`, `EXCLUDED`, or `REVIEW` per row (missing data is not silently excluded)
- Records reasons and produces a JSON summary
- Logs progress every 100,000 rows
- Linux-compatible, dependency-free Python 3.9+ script
- Automated unit and end-to-end tests

## Run
```bash
python3 plant_filter.py --input data/sample_plants.csv --output output/results.csv --summary output/summary.json --min-growth 20 --max-height 10 --sunlight 'full sun,partial shade'
python3 -m unittest discover -s tests -v
```

## Input schema
`plant_name,growth_rate_cm_year,mature_height_m,sunlight`

## Outputs
`output/results.csv` contains original values, decision and reason. `output/summary.json` contains counts and thresholds used.

## Scope notes
The design supports large CSVs, including a potential 1.3M-row source, but **1.3M-row performance is not claimed without a benchmark**. Production extensions would include API-enrichment with rate limits and caching, checkpoint/resume, source provenance, retry/backoff and more detailed validation. The simple demo overwrites output on rerun rather than resuming an interrupted job.
