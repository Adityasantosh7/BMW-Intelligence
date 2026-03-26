#!/usr/bin/env python3
"""
BMW BI Dashboard — Database Setup Script
Parses the BMW_Vehicle_Inventory.csv (web-archive wrapped) and loads it into SQLite.
Run: python3 setup_db.py
Requires: Python 3.6+ (uses only stdlib)
"""

import sqlite3
import re
import csv
import io
import os
import json
import sys

CSV_PATH = os.path.join(os.path.dirname(__file__), 'BMW_Vehicle_Inventory.csv')
DB_PATH  = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bmw.db')

def parse_csv(path):
    """Handle the Safari WebArchive wrapper and extract raw CSV rows."""
    with open(path, 'rb') as f:
        raw = f.read()

    # The file is a Safari .webarchive — the CSV content is embedded as HTML <pre> text
    idx = raw.find(b'model')
    if idx == -1:
        raise ValueError("Could not find CSV header in file — expected 'model' column")

    csv_text = raw[idx:].decode('utf-8', errors='replace')
    # Strip trailing HTML
    csv_text = csv_text.split('</pre>')[0].split('<br')[0]

    lines = csv_text.strip().split('\r\n')
    if not lines:
        raise ValueError("No lines found after header")

    # Clean the header: strip leading HTML artefacts and stray quotes
    header = re.sub(r'^[^m]*', '', lines[0]).strip().strip('"')
    lines[0] = header

    reader = csv.DictReader(io.StringIO('\r\n'.join(lines)))
    rows = list(reader)

    # The first column key may have a trailing quote due to the archive wrapper
    model_key = next((k for k in rows[0].keys() if 'model' in k.lower()), None)
    if model_key is None:
        raise ValueError(f"No 'model' column found. Columns: {list(rows[0].keys())}")

    return rows, model_key

def create_db(rows, model_key, db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute('DROP TABLE IF EXISTS inventory')
    cur.execute('''
        CREATE TABLE inventory (
            model        TEXT,
            year         INTEGER,
            price        REAL,
            transmission TEXT,
            mileage      REAL,
            fuelType     TEXT,
            tax          REAL,
            mpg          REAL,
            engineSize   REAL
        )
    ''')

    inserted = 0
    skipped  = 0

    for row in rows:
        try:
            def f(v): return float(v.strip()) if v.strip() else None
            def i(v): return int(float(v.strip())) if v.strip() else None

            cur.execute(
                'INSERT INTO inventory VALUES (?,?,?,?,?,?,?,?,?)',
                [
                    row[model_key].strip(),
                    i(row['year']),
                    f(row['price']),
                    row['transmission'].strip(),
                    f(row['mileage']),
                    row['fuelType'].strip(),
                    f(row['tax']),
                    f(row['mpg']),
                    f(row['engineSize']),
                ]
            )
            inserted += 1
        except Exception as e:
            skipped += 1

    conn.commit()

    # Verify
    count = cur.execute('SELECT COUNT(*) FROM inventory').fetchone()[0]
    models = [r[0] for r in cur.execute('SELECT DISTINCT model FROM inventory ORDER BY model').fetchall()]
    avg_price = cur.execute('SELECT ROUND(AVG(price),0) FROM inventory').fetchone()[0]

    conn.close()
    return count, models, avg_price, skipped

def write_schema_json(db_path):
    """Write /tmp/schema.json so n8n can dynamically pick up the current table schema."""
    conn = sqlite3.connect(db_path)
    cur  = conn.cursor()

    cur.execute("PRAGMA table_info(inventory)")
    cols = [{'name': row[1], 'type': row[2]} for row in cur.fetchall()]

    # Gather sample unique values for categorical columns
    categorical = ['model','transmission','fuelType']
    samples = {}
    for col in categorical:
        vals = [r[0] for r in cur.execute(f"SELECT DISTINCT {col} FROM inventory ORDER BY {col}").fetchall()]
        samples[col] = vals

    # Numeric ranges
    numeric = ['year','price','mileage','mpg','engineSize','tax']
    ranges = {}
    for col in numeric:
        row = cur.execute(f"SELECT MIN({col}), MAX({col}), ROUND(AVG({col}),1) FROM inventory").fetchone()
        ranges[col] = {'min': row[0], 'max': row[1], 'avg': row[2]}

    total = cur.execute("SELECT COUNT(*) FROM inventory").fetchone()[0]
    conn.close()

    schema = {
        'tableName': 'inventory',
        'totalRows': total,
        'columns': cols,
        'categoricalSamples': samples,
        'numericRanges': ranges,
        'source': 'BMW Vehicle Inventory'
    }

    schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schema.json')
    with open(schema_path, 'w') as f:
        json.dump(schema, f, indent=2)

    return schema_path

if __name__ == '__main__':
    print(f"\n{'='*55}")
    print(" BMW BI Dashboard — Database Setup")
    print(f"{'='*55}\n")

    if not os.path.exists(CSV_PATH):
        print(f"❌  CSV not found at: {CSV_PATH}")
        print("    Place BMW_Vehicle_Inventory.csv in the same directory as this script.")
        sys.exit(1)

    print(f"📂  Parsing {CSV_PATH} ...")
    rows, model_key = parse_csv(CSV_PATH)
    print(f"    Found {len(rows)} rows, model column: '{model_key}'")

    print(f"\n🗄   Creating SQLite database at {DB_PATH} ...")
    count, models, avg_price, skipped = create_db(rows, model_key, DB_PATH)

    print(f"    ✅  {count} rows inserted  ({skipped} skipped)")
    print(f"    📊  {len(models)} models: {', '.join(models)}")
    print(f"    💰  Average price: £{avg_price:,.0f}")

    print(f"\n📋  Writing schema to /tmp/schema.json ...")
    schema_path = write_schema_json(DB_PATH)
    print(f"    ✅  {schema_path}")

    print(f"\n{'='*55}")
    print(" Setup complete! Next steps:")
    print(f"{'='*55}")
    print(" 1. Import n8n-workflow.json into n8n")
    print(" 2. Set GROQ_API_KEY in n8n environment")
    print(" 3. Run: next dev -p 8000")
    print(f"{'='*55}\n")
