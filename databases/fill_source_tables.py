from sqlalchemy import create_engine
import os
import subprocess
import pandas as pd
import sqlalchemy

project_folder = subprocess.check_output("pwd", shell=True).\
                            decode("utf-8").rstrip()

PORT = os.getenv('PGPORT')
PASSWORD = os.getenv('PGPASSWORD')

engine = create_engine(
    f'postgresql://root:{PASSWORD}@localhost:{PORT}/source'
)

directories = ['ustan']
ustan_tables = [
    'serums_ids',
    'cycles',
    'general',
    'hospital_doctors',
    'intentions',
    'patients',
    'regimes',
    'smr01',
    'smr06',
    'tags',
    'translated_tags'
]

for directory in directories:
    csv_path = f'{project_folder}api/databases/data/{directory}/'

    if directory == 'ustan':
        tables = ustan_tables

    for table in tables:
        print(f"FILLING TABLE: {table}")
        try:
            with open(f"{csv_path}{table}.csv", 'r') as csv:
                df = pd.read_csv(csv)
            df.to_sql(table,
                      con=engine,
                      index=False,
                      schema=directory,
                      if_exists='append')
        except sqlalchemy.exc.DataError as d:
            with open(f"{csv_path}{table}.csv", 'r') as csv:
                df = pd.read_csv(csv, escapechar='\\')
                df.to_sql(table,
                          con=engine,
                          if_exists='append',
                          index=False,
                          schema=directory,
                          dtype={'tag': sqlalchemy.types.JSON})
        except sqlalchemy.exc.IntegrityError as i:
            print("DATA HAS ALREADY BEEN INSERTED!")
            break

engine.dispose()
print("FINISHED FILLING DATABASES")
