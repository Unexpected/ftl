from flask import current_app, g

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm.query import Query

from db.model import *

CONNECTION_STRING = 'postgres+psycopg2://ftl:ftl@localhost:5432/ftl'

engine = create_engine(CONNECTION_STRING).execution_options(
    schema_translate_map={None: "app", "core": "core", "demo": "demo"})

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
    return g.db_session


def close_db(e=None):
    db_session = g.pop('db_session', None)
    if db_session is not None:
        db_session.close()


def drop_all():
    Base.metadata.drop_all(engine)


def create_all():
    Base.metadata.create_all(engine)


def insert_startup_data():
    db_session = get_db_session()
    # Insert a Person in the person table
    entities = []
    entities.append(Entity(name='person', table_name='person',
                           label='Personne', schema_name='demo'))
    entities.append(Entity(name='band', table_name='band',
                           label='Groupe', schema_name='demo'))
    db_session.add_all(entities)
    db_session.commit()

    attr1 = Attribute(name='id', entity_name='person',
                      data_type=0, length='8', label='id', mandatory=True, order=0)
    attr2 = Attribute(name='lastname', entity_name='person',
                      data_type=1, length='80', label='Nom', order=5)
    attr3 = Attribute(name='firstname', entity_name='person',
                      data_type=1, length='80', label='Prénom', order=10)
    attr4 = Attribute(name='birth_date', entity_name='person',
                      data_type=2, label='Date de naissance', order=15)
    attr5 = Attribute(name='name', entity_name='band',
                      data_type=1, length='80', label='Name', mandatory=True, order=0)
    attr6 = Attribute(name='genre', entity_name='band',
                      data_type=0, length='8', label='Genre', order=5)
    db_session.add_all([attr1, attr2, attr3, attr4, attr5, attr6])
    db_session.commit()

    db_session.add(Key(name='person_pk', entity_name='person', key_type=0))
    db_session.add(Key(name='band_pk', entity_name='band', key_type=0))
    db_session.commit()

    db_session.add(KeyAttribute(key_name='person_pk',
                                attribute_name='id', entity_name='person'))
    db_session.add(KeyAttribute(key_name='band_pk',
                                attribute_name='name', entity_name='band'))
    db_session.commit()

    demo_module = Module(name='demo', label='Demo App',
                         comment='Demonstration application to show how to build an FTL app')
    demo_module.entities = entities
    db_session.add(demo_module)
    db_session.commit()


def create_model():
    db_session = get_db_session()
    for module in db_session.query(Module).all():
        if module.name == "core":
            continue

        for entity in module.entities:
            table_name = entity.table_name
            if not table_name:
                table_name = entity.name
            attr_dict = {'__tablename__': table_name}
            if entity.schema_name != None:
                attr_dict['__table_args__'] = {'schema': entity.schema_name}

            pk_attributes = set()
            for key in entity.keys:
                if key.key_type == 0:
                    for key_attribute in key.key_attributes:
                        pk_attributes.add(key_attribute.attribute_name)

            for attribute in entity.attributes:
                data_type_class = None
                if attribute.data_type == 0:
                    data_type_class = Integer
                elif attribute.data_type == 1:
                    data_type_class = String(attribute.length)
                elif attribute.data_type == 2:
                    data_type_class = Date
                elif attribute.data_type == 3:
                    data_type_class = Boolean

                if attribute.name in pk_attributes:
                    column = Column(data_type_class, primary_key=True)
                else:
                    column = Column(data_type_class)

                attr_dict[attribute.name] = column

            Base = declarative_base()
            className = entity.name[0].upper() + entity.name[1:]
            MyClass = type(className, (Base,), attr_dict)

        Base.metadata.create_all(engine)

    return


def insert_core_metadata():
    core_entities, core_attributes, core_keys, core_key_attributes, core_module = get_core_metadata()

    db_session = get_db_session()
    db_session.add_all(core_entities)
    db_session.commit()

    db_session.add_all(core_attributes)
    db_session.commit()

    db_session.add_all(core_keys)
    db_session.commit()

    db_session.add_all(core_key_attributes)
    db_session.commit()

    db_session.add(core_module)
    db_session.commit()


def reset():
    drop_all()
    create_all()
    insert_core_metadata()
    insert_startup_data()
    create_model()
    # db_session = get_db_session()
    # with current_app.open_resource('schema.sql') as f:
    #    db.executescript(f.read().decode('utf8'))


def get_entities():
    db_session = get_db_session()
    q = db_session.query(Entity)
    return q.all()


def get_attributes(entity_name):
    db_session = get_db_session()
    q = db_session.query(Attribute).filter(
        Attribute.entity_name == entity_name)
    return q.all()


def insert_entity(entity_name, data):
    db_session = get_db_session()


def get_modules():
    db_session = get_db_session()
    q = db_session.query(Module)
    return q.all()


def get_module(module_name):
    db_session = get_db_session()
    module = db_session.query(Module).get(module_name)
    return module
