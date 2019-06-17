import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from src.models.SharedModels import db
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = db.Model


class Restaurant(Base):

    __tablename__ = 'restaurant'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
