from fastapi import FastAPI, HTTPException, File, UploadFile
from sklearn.neighbors import NearestNeighbors
import csv
from .database import Base, SessionLocal, engine
from .models import RoutePoint, Route
from .schemas import RoutePointCreate, RouteData

app = FastAPI()

# Создаем таблицы в базе данных
Base.metadata.create_all(bind=engine)


def find_nearest_neighbors(points: list[dict[str, float]], n_neighbors: int = 2) -> dict[tuple[float, float]]:
    coordinates = [(point["lat"], point["lng"]) for point in points]
    # Инициализация модели ближайших соседей
    nbrs = NearestNeighbors(n_neighbors=n_neighbors, algorithm='auto').fit(coordinates)
    # Поиск ближайших соседей для каждой точки
    distances, indices = nbrs.kneighbors(coordinates)

    # Составление результата в нужном формате
    nearest_neighbors = []
    for i, point in enumerate(points):
        nearest_neighbors.append([(points[j]["lat"], points[j]["lng"]) for j in indices[i]])
    return nearest_neighbors


@app.post("/api/routes")
def create_route(csv_file: UploadFile = File(...)):
    points = []
    session = SessionLocal(autoflush=False, bind=engine)

    contents = csv_file.file.read()
    decoded_content = contents.decode("utf-8").splitlines()
    csv_reader = csv.DictReader(decoded_content)

    # Обработка каждой строки CSV файла
    columns_to_check = ['population', 'density', 'county_fips']
    for row in csv_reader:
        for column in columns_to_check:
            if isinstance(row[column], str) and len(row[column]) == 0:
                row[column] = None
        # Создание объекта RoutePointCreate из данных строки
        route_point_data = RoutePointCreate(**row)
        # Создание объекта точки маршрута
        points.append(
            {"lat": route_point_data.lat, "lng": route_point_data.lng}
        )
        with (session as db):
            db.add(RoutePoint(**route_point_data.dict()))
            db.commit()

    results = find_nearest_neighbors(points)

    # Преобразование каждой пары координат в формат {"lat": ..., "lng": ...}
    formatted_results = [[{"lat": lat, "lng": lng} for lat, lng in route] for route in results]
    all_points = [point for route in formatted_results for point in route]
    output = {"points": all_points}

    # Сохранение маршрута в базе данных
    with session as db:
        route = Route(**output)
        db.add(route)
        db.commit()

    return {"message": "Route created successfully"}


# Реализуем обработчик для получения маршрута по его ID
@app.get("/api/routes/{route_id}", response_model=RouteData)
async def get_route(route_id: int):
    db = SessionLocal()
    route = db.query(Route).filter(Route.id == route_id).first()
    db.close()
    if route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    return route


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
