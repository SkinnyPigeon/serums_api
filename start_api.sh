#!/bin/bash
service postgresql start
python3.9 /api/databases/source_table.py
python3.9 /api/databases/fill_source_tables.py
python3.9 /api/databases/convert_zmc_files.py
cd /api/
uvicorn main:app --reload --host 0.0.0.0 --port 5000
