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
    # status = Column(Integer)
    #__table_args__ = {'schema': 'core'}

    def update_from_dict(self, data):
        self.database_name = data["database_name"]
        self.schema_name = data["schema_name"]
        self.table_name = data["table_name"]
        self.label = data["label"]
        self.comment = data["comment"]

    def set_primary_key(self, data):
        self.name = data["name"]


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

    #__table_args__ = {'schema': 'core'}

    entity = relationship("Entity", back_populates="attributes")

    def update_from_dict(self, data):
        self.data_type = int(data["data_type"])
        self.length = int(data["length"])
        self.length_scale = int(data["length_scale"])
        self.mandatory = data["mandatory"]

        # business info
        self.order = int(data["order"])
        self.label = data["label"]
        self.caption = data["caption"]
        self.placeholder = data["placeholder"]
        self.tooltip = data["tooltip"]
        self.comment = data["comment"]
        self.initial_value = data["initial_value"]
        self.default_value = data["default_value"]

    def set_primary_key(self, data):
        self.name = data["name"]
        self.entity_name = data["entity_name"]


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
                      name, entity_name]), )  # {'schema': 'core'})

    entity = relationship("Entity", back_populates="keys")

    def update_from_dict(self, data):
        self.label = data["label"]
        self.comment = data["comment"]
        self.key_type = int(data["key_type"])
        self.target_key = data["target_key"]
        self.target_entity = data["target_entity"]

    def set_primary_key(self, data):
        self.name = data["name"]
        self.entity_name = data["entity_name"]


class KeyAttribute(Base):
    __tablename__ = 'key_attribute'

    key_name = Column(String(80), primary_key=True)
    attribute_name = Column(String(80), primary_key=True)
    entity_name = Column(String(80), primary_key=True)
    __table_args__ = (ForeignKeyConstraint([attribute_name, entity_name], [
                      Attribute.name, Attribute.entity_name]),
                      ForeignKeyConstraint([key_name, entity_name], [
                          Key.name, Key.entity_name]))  # , {'schema': 'core'})
    order = Column(Integer)

    key = relationship("Key", back_populates="key_attributes")

    def update_from_dict(self, data):
        self.order = int(data["order"])

    def set_primary_key(self, data):
        self.key_name = data["key_name"]
        self.attribute_name = data["attribute_name"]
        self.entity_name = data["entity_name"]


class Module(Base):
    __tablename__ = 'module'
    name = Column(String(80), primary_key=True)
    label = Column(String(250))
    comment = Column(String(4000))
    #__table_args__ = {'schema': 'core'}

    def update_from_dict(self, data):
        self.label = data["label"]
        self.comment = data["comment"]

    def set_primary_key(self, data):
        self.name = data["name"]


module_entity_join = Table('module_entity_join', Base.metadata,
                           Column('module_name', String(80), ForeignKey(
                               Module.name), primary_key=True),
                           Column('entity_name', String(80), ForeignKey(
                               Entity.name), primary_key=True)
                           )  # , schema='core')

Entity.attributes = relationship(
    Attribute, order_by=Attribute.order, back_populates="entity")

Entity.keys = relationship(
    Key, order_by=Key.key_type, back_populates="entity")

Key.key_attributes = relationship(
    KeyAttribute, order_by=KeyAttribute.order, back_populates="key")

Module.entities = relationship(Entity, secondary=module_entity_join)
