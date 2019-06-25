import sys
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

db = SQLAlchemy()

Base = db.Model


class Restaurant(Base):

    __tablename__ = 'restaurant'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True, autoincrement=True)

    @staticmethod
    def create_restaurant(name):
        """Create a new restaurant entry"""
        restaurant = Restaurant(name=name)
        db.session.add(restaurant)
        db.session.commit()


class MenuItem(Base):

    __tablename__ = 'menu_item'

    id = Column(Integer, primary_key=True)
    course = Column(String(250), nullable=False)
    description = Column(String(250))
    price = Column(String(8))

    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)
