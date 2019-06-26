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

    @staticmethod
    def get_restaurant_by_id(id):
        return Restaurant.query.filter_by(id=id).first()

    @staticmethod
    def update_restaurant_name(id, name):
        restaurant = Restaurant.query.filter_by(id=id).first()
        restaurant.name = name
        db.session.commit()

    @staticmethod
    def delete_restaurant(id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        db.session.delete(restaurant)
        db.session.commit()


class MenuItem(Base):

    __tablename__ = 'menu_item'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), nullable=False)
    course = Column(String(250), nullable=False)
    description = Column(String(250))
    price = Column(String(8))

    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

    @staticmethod
    def create_new_menu_item(restaurant_id, name, description, price, course):
        menu_item = MenuItem(
            restaurant_id=restaurant_id, name=name, course=course, description=description, price=price)
        db.session.add(menu_item)
        db.session.commit()

    @staticmethod
    def get_menu_by_restaurant_id(id):
        return MenuItem.query.filter_by(restaurant_id=id).all()
