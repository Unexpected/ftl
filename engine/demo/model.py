from sqlalchemy import Table, Column, ForeignKey, Integer, String, ForeignKeyConstraint, Boolean, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    lastname = Column(String(80))
    firstname = Column(String(80))
    birth_date = Column(Date)


class Band(Base):
    __tablename__ = 'band'
    name = Column(String(80), primary_key=True)
    genre = Column(Integer)
