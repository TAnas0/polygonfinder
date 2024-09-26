from sqlalchemy import Column, Integer, String, Float
from .database import Base
from geoalchemy2 import Geometry


class Provider(Base):
    __tablename__ = "providers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String)
    language = Column(String)
    currency = Column(String)


class ServiceArea(Base):
    __tablename__ = "service_areas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    geojson = Column(Geometry('POLYGON'))
