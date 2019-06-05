import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from src.models.SharedModels import db
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from src.models.Restaurant import Restaurant

Base = db.Model


class MenuItem(Base):

    __tablename__ = 'menu_item'

    id = Column(Integer, primary_key=True)
    course = Column(String(250), nullable=False)
    description = Column(String(250))
    price = Column(String(8))

    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)
