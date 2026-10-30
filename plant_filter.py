#!/usr/bin/env python3
"""Streaming botanical dataset qualification demo. Standard library only."""
import argparse
import csv
import json
import logging
from pathlib import Path

REQUIRED = ('plant_name', 'growth_rate_cm_year', 'mature_height_m', 'sunlight')
OUTPUT = ('plant_name','growth_rate_cm_year','mature_height_m','sunlight','status','reason')

def classify(row, min_growth, max_height, allowed_sun):
    name = row.get('plant_name', '').strip()
    try:
        growth = float(row['growth_rate_cm_year'])
        height = float(row['mature_height_m'])
        if growth < 0 or height < 0:
            raise ValueError('negative measurement')
    except (ValueError, TypeError, KeyError):
        return 'REVIEW', 'Missing or invalid growth/height data'
    sun = row.get('sunlight','').strip().lower()
    if not name or not sun:
        return 'REVIEW', 'Missing name or sunlight data'
    if growth >= min_growth and height <= max_height and sun in allowed_sun:
        return 'QUALIFIED', 'Meets all specified thresholds'
    return 'EXCLUDED', 'Does not meet one or more thresholds'

def run(input_path, output_path, summary_path, min_growth, max_height, sunlight, checkpoint_every=100000):
    counts = {'QUALIFIED': 0, 'EXCLUDED': 0, 'REVIEW': 0}
    output_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    allowed = {s.strip().lower() for s in sunlight.split(',') if s.strip()}
    if not allowed: raise ValueError('At least one sunlight category required')
    with input_path.open('r', newline='', encoding='utf-8-sig') as source:
        reader = csv.DictReader(source)
        if not reader.fieldnames or not set(REQUIRED).issubset(reader.fieldnames):
            raise ValueError(f'Input CSV must contain columns: {", ".join(REQUIRED)}')
        with output_path.open('w', newline='', encoding='utf-8') as dest:
            writer = csv.DictWriter(dest, fieldnames=OUTPUT)
            writer.writeheader()
            for index, row in enumerate(reader, 1):
                status, reason = classify(row, min_growth, max_height, allowed)
                counts[status] += 1
                writer.writerow({**{k: row.get(k, '') for k in REQUIRED}, 'status': status, 'reason': reason})
                if index % checkpoint_every == 0:
                    logging.info('Processed %s records', f'{index:,}')
    summary = {'total': sum(counts.values()), 'counts': counts, 'criteria': {'min_growth_cm_year': min_growth, 'max_height_m': max_height, 'sunlight': sorted(allowed)}, 'note': 'Demonstration only. Input fields are supplied data, not independently verified botanical claims.'}
    summary_path.write_text(json.dumps(summary, indent=2), encoding='utf-8')
    return summary

def main():
    parser = argparse.ArgumentParser(description='Stream and filter plant trait data from CSV')
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, default=Path('output/results.csv'))
    parser.add_argument('--summary', type=Path, default=Path('output/summary.json'))
    parser.add_argument('--min-growth', type=float, default=20)
    parser.add_argument('--max-height', type=float, default=10)
    parser.add_argument('--sunlight', default='full sun,partial shade')
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    result = run(args.input, args.output, args.summary, args.min_growth, args.max_height, args.sunlight)
    print(json.dumps(result, indent=2))

if __name__ == '__main__': main()
