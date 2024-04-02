from sqlalchemy import create_engine, Column, JSON, Integer, String, Float
from database import Base, SessionLocal, engine


# Модель данных для хранения точек маршрута
class RoutePoint(Base):
    __tablename__ = "route_points"

    id = Column(Integer, primary_key=True, index=True)
    lat = Column(Float)
    lng = Column(Float)
    city = Column(String)
    state_id = Column(String)
    state_name = Column(String)
    zcta = Column(String)
    parent_zcta = Column(String)
    population = Column(Integer)
    density = Column(Float)
    county_fips = Column(Integer)
    county_name = Column(String)
    county_weights = Column(String)
    county_names_all = Column(String)
    county_fips_all = Column(String)
    imprecise = Column(String)
    military = Column(String)
    timezone = Column(String)


# Модель для хранения маршрутов
class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)
    points = Column(JSON)
