from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
import os

PORT = os.getenv('PGPORT')
PASSWORD = os.getenv('PGPASSWORD')
ALCHEMY_USER = os.getenv('ALCHEMY_USER')


def setup_connection(schema: str):
    """Creates a connection to the database.
            Parameters:

                schema (str): The schema for the use case partner's
                data within the database
            Returns:
                connection (dict): This contains most of the important
                elements of the connection allowing for many different
                types of operations within the database
    """
    engine = create_engine(
        f'postgresql://{ALCHEMY_USER}:{PASSWORD}@localhost:{PORT}/source',
        poolclass=NullPool
    )
    metadata = MetaData(schema=schema.lower(), bind=engine)
    metadata.reflect(engine)
    Base = automap_base(metadata=metadata)
    Base.prepare()
    Session = sessionmaker(bind=engine)
    session = Session()
    return {
        "metadata": metadata,
        "base": Base,
        "engine": engine,
        "session": session,
        'schema': schema.lower()
    }
