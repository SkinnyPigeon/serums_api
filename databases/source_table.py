from sqlalchemy import create_engine, MetaData
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os

PORT = os.getenv('PGPORT')
PASSWORD = os.getenv('PGPASSWORD')

metadata = MetaData()
Base = declarative_base()
base = Base()
engine = create_engine(
    f'postgresql://postgres:{PORT}@localhost:{PASSWORD}/source'
)
if not database_exists(engine.url):
    create_database(engine.url)
Session = sessionmaker(
    bind=engine, autoflush=True, autocommit=True
)
session = Session()
connection = {
    'base': base,
    'metadata': metadata,
    'engine': engine,
    'session': session
}