import sqlalchemy
import os


def get_engine():
    engine = getattr(get_engine, 'engine', None)
    if engine is None:
        db_uri = os.getenv('FUND_DB_URI')
        engine = sqlalchemy.create_engine(db_uri)
        setattr(get_engine, 'engine', engine)

    return engine
