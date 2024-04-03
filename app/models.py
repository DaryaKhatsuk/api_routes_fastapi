from sqlalchemy import Column, JSON, Integer
from .database import Base
from sqlalchemy.orm import Mapped, mapped_column


# Модель данных для хранения точек маршрута
class RoutePoint(Base):
    __tablename__ = "route_points"

    zip: Mapped[int] = mapped_column(primary_key=True)
    lat: Mapped[float | None] = None
    lng: Mapped[float | None] = None
    city: Mapped[str | None] = None
    state_id: Mapped[str | None] = None
    state_name: Mapped[str | None] = None
    zcta: Mapped[str | None] = None
    parent_zcta: Mapped[str | None] = None
    population: Mapped[int | None] = None
    density: Mapped[float | None] = None
    county_fips: Mapped[int | None] = None
    county_name: Mapped[str | None] = None
    county_weights: Mapped[str | None] = None
    county_names_all: Mapped[str | None] = None
    county_fips_all: Mapped[str | None] = None
    imprecise: Mapped[str | None] = None
    military: Mapped[str | None] = None
    timezone: Mapped[str | None] = None


# Модель для хранения маршрутов
class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)
    points = Column(JSON)
