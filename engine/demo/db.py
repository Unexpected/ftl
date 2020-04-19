from flask import g

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from demo.model import *

CONNECTION_STRING = 'sqlite:///core/sqlite/demo.db'

engine = create_engine(CONNECTION_STRING)
# .execution_options(schema_translate_map={None: "app", "core": "core", "demo": "demo"})

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)


def get_db_session():
    if 'db_session' not in g:
        # A DBSession() instance establishes all conversations with the database
        # and represents a "staging zone" for all the objects loaded into the
        # database session object. Any change made against the objects in the
        # session won't be persisted into the database until you call
        # session.commit(). If you're not happy about the changes, you can
        # revert all of them back to the last commit by calling
        # session.rollback()
        g.db_session = DBSession()

    # if 'loaded_model' not in g:
    #    g.loaded_model = True
    #    load_model()
    return g.db_session


def check_db_connection():
    session = get_db_session()
    create_all()
    session.close()


def create_all():
    Base.metadata.create_all(engine)


def close_db_connection(e=None):
    db_session = g.pop('db_session', None)
    if db_session is not None:
        db_session.close()
