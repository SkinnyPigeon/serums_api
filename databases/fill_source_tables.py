from sqlalchemy import create_engine
import os
import subprocess
import pandas as pd
import sqlalchemy


project_folder = subprocess.check_output("pwd", shell=True).\
                            decode("utf-8").rstrip()

PORT = os.getenv('PGPORT')
PASSWORD = os.getenv('PGPASSWORD')
ALCHEMY_USER = os.getenv('ALCHEMY_USER')

engine = create_engine(
    f'postgresql://{ALCHEMY_USER}:{PASSWORD}@localhost:{PORT}/source'
)

directories = ['ustan', 'fcrb', 'zmc']

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

fcrb_tables = [
    'diagnostic',
    'episode',
    'hospital_doctors',
    'medical_specialty',
    'medication',
    'monitoring_params',
    'order_entry',
    'patient_address',
    'patient',
    'professional',
    'serums_ids',
    'tags',
    'translated_tags',
    'vital_signs'
]

zmc_tables = [
    'address',
    'alcohol_use',
    'allergies',
    'bloodpressure',
    'complaints_and_diagnosis',
    'documents',
    'drug_use',
    'functional_or_mental_state',
    'hospital_doctors',
    'images',
    'living_situation',
    'measurements',
    'medical_aids_and_tools',
    'medication_agreements',
    'medication_use',
    'patient_details',
    'registered_events',
    'serums_ids',
    'tags',
    'tobacco_use',
    'translated_tags',
    'warning',
    'wearable'
]

for directory in directories:
    csv_path = f'{project_folder}api/databases/data/{directory}/'
    print(f"{directory.upper()} TABLES")

    if directory == 'ustan':
        tables = ustan_tables
    elif directory == 'fcrb':
        tables = fcrb_tables
    elif directory == 'zmc':
        tables = zmc_tables

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
