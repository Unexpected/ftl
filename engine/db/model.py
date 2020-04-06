import os
import sys
from sqlalchemy import Table, Column, ForeignKey, Integer, String, ForeignKeyConstraint, Boolean, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Entity(Base):
    __tablename__ = 'entity'
    name = Column(String(80), primary_key=True)
    # meta info
    database_name = Column(String(80))
    schema_name = Column(String(80))
    table_name = Column(String(80))
    # business info
    label = Column(String(250))
    comment = Column(String(4000))
    # engine technical data
    status = Column(Integer)
    __table_args__ = {'schema': 'core'}


class Attribute(Base):
    __tablename__ = 'attribute'
    # meta info
    name = Column(String(80), primary_key=True)
    entity_name = Column(String(80), ForeignKey(Entity.name), primary_key=True)
    data_type = Column(Integer)  # 0 : Integer, 1 : String,
    length = Column(Integer)
    length_scale = Column(Integer)
    mandatory = Column(Boolean)

    # business info
    order = Column(Integer)
    label = Column(String(250))
    caption = Column(String(250))
    placeholder = Column(String(250))
    tooltip = Column(String(250))
    comment = Column(String(4000))
    initial_value = Column(String(250))
    default_value = Column(String(250))

    __table_args__ = {'schema': 'core'}

    entity = relationship("Entity", back_populates="attributes")


class Key(Base):
    __tablename__ = 'key'
    name = Column(String(80), primary_key=True)
    entity_name = Column(String(80), ForeignKey(Entity.name), primary_key=True)
    label = Column(String(250))
    comment = Column(String(4000))
    key_type = Column(Integer)
    target_key = Column(String(80))
    target_entity = Column(String(80))

    __table_args__ = (ForeignKeyConstraint([target_key, target_entity], [
                      name, entity_name]), {'schema': 'core'})

    entity = relationship("Entity", back_populates="keys")


class KeyAttribute(Base):
    __tablename__ = 'key_attribute'

    key_name = Column(String(80), primary_key=True)
    attribute_name = Column(String(80), primary_key=True)
    entity_name = Column(String(80), primary_key=True)
    __table_args__ = (ForeignKeyConstraint([attribute_name, entity_name], [
                      Attribute.name, Attribute.entity_name]), 
                      ForeignKeyConstraint([key_name, entity_name], [
                      Key.name, Key.entity_name]), {'schema': 'core'})
    order = Column(Integer)

    key = relationship("Key", back_populates="key_attributes")


class Module(Base):
    __tablename__ = 'module'
    name = Column(String(80), primary_key=True)
    label = Column(String(250))
    comment = Column(String(4000))
    __table_args__ = {'schema': 'core'}


module_entity_join = Table('module_entity_join', Base.metadata,
                           Column('module_name', String(80), ForeignKey(
                               Module.name), primary_key=True),
                           Column('entity_name', String(80), ForeignKey(
                               Entity.name), primary_key=True),
                           schema='core')

Entity.attributes = relationship(
    Attribute, order_by=Attribute.order, back_populates="entity")

Entity.keys = relationship(
    Key, order_by=Key.key_type, back_populates="entity")

Key.key_attributes = relationship(
    KeyAttribute, order_by=KeyAttribute.order, back_populates="key")

Module.entities = relationship(Entity, secondary=module_entity_join)


def get_core_metadata():
    core_entities = []
    core_entities.append(Entity(name='entity', schema_name='core',
                                table_name='entity', label='Entity', comment='Entity model'))

    core_keys = []
    core_keys.append(Key(name='entity_pk', entity_name='entity',
                         label='Entity PK', comment='Entity primary key', key_type=0))

    core_attributes = []
    core_attributes.append(Attribute(name='name', entity_name='entity',
                                     data_type=1, length=80, mandatory=True, order=0, label='Name'))
    core_attributes.append(Attribute(name='database_name', entity_name='entity',
                                     data_type=1, length=80, mandatory=False, order=5, label='Database Name'))
    core_attributes.append(Attribute(name='schema_name', entity_name='entity',
                                     data_type=1, length=80, mandatory=False, order=10, label='Schema Name'))
    core_attributes.append(Attribute(name='table_name', entity_name='entity',
                                     data_type=1, length=80, mandatory=True, order=15, label='Table Name'))
    core_attributes.append(Attribute(name='label', entity_name='entity',
                                     data_type=1, length=250, mandatory=True, order=20, label='Label'))
    core_attributes.append(Attribute(name='comment', entity_name='entity',
                                     data_type=1, length=4000, mandatory=False, order=25, label='Comment'))

    core_key_attributes = []
    core_key_attributes.append(KeyAttribute(
        key_name='entity_pk', attribute_name='name', entity_name='entity', order=0))

    core_entities.append(Entity(name='attribute', schema_name='core',
                                table_name='attribute', label='Attribute', comment='Attribute model'))

    core_attributes.append(Attribute(name='name', entity_name='attribute',
                                     data_type=1, length=80, mandatory=True, order=0, label='Name'))
    core_attributes.append(Attribute(name='entity_name', entity_name='attribute',
                                     data_type=1, length=80, mandatory=True, order=5, label='Entity Name'))
    core_attributes.append(Attribute(name='data_type', entity_name='attribute',
                                     data_type=0, length=3, mandatory=True, order=10, label='Data type'))
    core_attributes.append(Attribute(name='length', entity_name='attribute',
                                     data_type=0, length=8, mandatory=True, order=15, label='Length'))
    core_attributes.append(Attribute(name='length_scale', entity_name='attribute',
                                     data_type=0, length=8, mandatory=True, order=20, label='Length scale'))
    core_attributes.append(Attribute(name='mandatory', entity_name='attribute',
                                     data_type=4, length=8, mandatory=True, order=25, label='Mandatory'))
    core_attributes.append(Attribute(name='order', entity_name='attribute',
                                     data_type=0, length=8, mandatory=True, order=30, label='Order'))
    core_attributes.append(Attribute(name='label', entity_name='attribute',
                                     data_type=1, length=250, mandatory=True, order=35, label='Label'))
    core_attributes.append(Attribute(name='caption', entity_name='attribute',
                                     data_type=1, length=250, mandatory=True, order=40, label='Caption'))
    core_attributes.append(Attribute(name='placeholder', entity_name='attribute',
                                     data_type=1, length=250, mandatory=True, order=45, label='Placeholder'))
    core_attributes.append(Attribute(name='tooltip', entity_name='attribute',
                                     data_type=1, length=250, mandatory=True, order=50, label='Tooltip'))
    core_attributes.append(Attribute(name='comment', entity_name='attribute',
                                     data_type=1, length=4000, mandatory=True, order=55, label='Comment'))
    core_attributes.append(Attribute(name='initial_value', entity_name='attribute',
                                     data_type=1, length=250, mandatory=True, order=60, label='Initial Value'))
    core_attributes.append(Attribute(name='default_value', entity_name='attribute',
                                     data_type=1, length=250, mandatory=True, order=65, label='Default Value'))

    core_keys.append(Key(name='attribute_pk', entity_name='attribute',
                         label='Attribute PK', comment='Attribute primary key', key_type=0))

    core_key_attributes.append(KeyAttribute(
        key_name='attribute_pk', attribute_name='name', entity_name='attribute', order=0))

    # Key
    core_entities.append(Entity(name='key', schema_name='core',
                                table_name='key', label='Key', comment='Key model'))

    core_attributes.append(Attribute(name='name', entity_name='key',
                                     data_type=1, length=80, mandatory=True, order=0, label='Name'))
    core_attributes.append(Attribute(name='entity_name', entity_name='key',
                                     data_type=1, length=80, mandatory=True, order=5, label='Entity name'))
    core_attributes.append(Attribute(name='label', entity_name='key',
                                     data_type=1, length=250, mandatory=True, order=10, label='Label'))
    core_attributes.append(Attribute(name='comment', entity_name='key',
                                     data_type=1, length=4000, mandatory=False, order=15, label='Comment'))
    core_attributes.append(Attribute(name='key_type', entity_name='key',
                                     data_type=0, length=10, mandatory=True, order=20, label='Key type'))
    core_attributes.append(Attribute(name='target_key', entity_name='key',
                                     data_type=1, length=80, mandatory=False, order=25, label='Target key name'))
    core_attributes.append(Attribute(name='target_entity', entity_name='key',
                                     data_type=1, length=80, mandatory=False, order=30, label='Target entity name'))

    target_key = Column(String(80))
    target_entity = Column(String(80))


    core_keys.append(Key(name='key_pk', entity_name='key',
                         label='Key PK', comment='Key primary key', key_type=0))

    core_key_attributes.append(KeyAttribute(
        key_name='key_pk', attribute_name='name', entity_name='key', order=0))
    core_key_attributes.append(KeyAttribute(
        key_name='key_pk', attribute_name='entity_name', entity_name='key', order=5))

    # KeyAttribute
    core_entities.append(Entity(name='key_attribute', schema_name='core',
                                table_name='key_attribute', label='Key attribute', comment='Key attribute model'))

    core_attributes.append(Attribute(name='key_name', entity_name='key_attribute',
                                     data_type=1, length=80, mandatory=True, order=0, label='Key name'))
    core_attributes.append(Attribute(name='attribute_name', entity_name='key_attribute',
                                     data_type=1, length=80, mandatory=True, order=5, label='Attribute name'))
    core_attributes.append(Attribute(name='entity_name', entity_name='key_attribute',
                                     data_type=1, length=80, mandatory=True, order=10, label='Entity name'))
    core_attributes.append(Attribute(name='order', entity_name='key_attribute',
                                     data_type=0, length=10, mandatory=True, order=15, label='Order'))

    core_keys.append(Key(name='key_attribute_pk', entity_name='key_attribute',
                         label='Key attribute PK', comment='Key attribute primary key', key_type=0))

    core_key_attributes.append(KeyAttribute(
        key_name='key_attribute_pk', attribute_name='key_name', entity_name='key_attribute', order=0))
    core_key_attributes.append(KeyAttribute(
        key_name='key_attribute_pk', attribute_name='attribute_name', entity_name='key_attribute', order=5))
    core_key_attributes.append(KeyAttribute(
        key_name='key_attribute_pk', attribute_name='entity_name', entity_name='key_attribute', order=10))

    # Module
    core_entities.append(Entity(name='module', schema_name='core',
                                table_name='module', label='Module', comment='Module model'))

    core_attributes.append(Attribute(name='name', entity_name='module',
                                     data_type=1, length=80, mandatory=True, order=0, label='Module name'))
    core_attributes.append(Attribute(name='label', entity_name='module',
                                     data_type=1, length=250, mandatory=True, order=5, label='Label'))
    core_attributes.append(Attribute(name='comment', entity_name='module',
                                     data_type=1, length=4000, mandatory=True, order=10, label='Comment'))

    core_keys.append(Key(name='module_pk', entity_name='module',
                         label='Module PK', comment='Module primary key', key_type=0))

    core_key_attributes.append(KeyAttribute(
        key_name='module_pk', attribute_name='name', entity_name='module', order=0))

    core_module = Module(name='core', label='FTL',
                         comment='FTL Prototyper module')
    core_module.entities = core_entities

    return core_entities, core_attributes, core_keys, core_key_attributes, core_module
