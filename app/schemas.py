from typing import Union
from pydantic import BaseModel, ConfigDict


class RoutePointCreate(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)

    zip: int
    lat: Union[float, None] = None
    lng: Union[float, None] = None
    city: Union[str, None] = None
    state_id: Union[str, None] = None
    state_name: Union[str, None] = None
    zcta: Union[str, None] = None
    parent_zcta: Union[str, None] = None
    population: Union[int, None] = None
    density: Union[float, None] = None
    county_fips: Union[int, None] = None
    county_name: Union[str, None] = None
    county_weights: Union[str, None] = None
    county_names_all: Union[str, None] = None
    county_fips_all: Union[str, None] = None
    imprecise: Union[str, None] = None
    military: Union[str, None] = None
    timezone: Union[str, None] = None


# Схема для данных точки маршрута
class RoutePoints(BaseModel):
    lat: float
    lng: float


# Схема для данных маршрута
class RouteData(BaseModel):
    id: int
    points: list[
        RoutePoints
    ]
