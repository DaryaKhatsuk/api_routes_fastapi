from fastapi import FastAPI, HTTPException, Query, File, UploadFile
from database import Base, SessionLocal, engine

from sklearn.neighbors import NearestNeighbors
import numpy as np

from models import RoutePoint, Route
from schemas import RoutePointCreate, RoutePoint, RouteData
import csv


app = FastAPI()

# Создаем таблицы в базе данных
Base.metadata.create_all(bind=engine)


# def convert_points_to_array(points: list[dict[str, float]]) -> np.ndarray:
#     return np.array([[point["lat"], point["lng"]] for point in points])

def find_nearest_neighbors(points: list[dict[str, float]], n_neighbors: int = 2) -> dict[tuple[float, float]]:
    # # Преобразование списка точек в numpy массив
    coordinates = [(point["lat"], point["lng"]) for point in points]

    # Инициализация модели ближайших соседей
    nbrs = NearestNeighbors(n_neighbors=n_neighbors, algorithm='auto').fit(coordinates)

    # Поиск ближайших соседей для каждой точки
    distances, indices = nbrs.kneighbors(coordinates)

    # Составление результата в нужном формате
    nearest_neighbors = []
    for i, point in enumerate(points):
        nearest_neighbors.append([(points[j]["lat"], points[j]["lng"]) for j in indices[i]])
        # nearest_neighbors.append({
        #     "lat": point["lat"],
        #     "lng": point["lng"],
        #     "neighbors": [
        #         {"lat": points[idx]["lat"], "lng": points[idx]["lng"]}
        #         for idx in indices[i][1:]  # Исключаем саму точку, ближайший сосед будет на позиции 1
        #     ]
        # })
    print('nearest_neighbors', nearest_neighbors)
    return nearest_neighbors


@app.post("/api/routes")
def create_route(
        # session: SessionLocal(autoflush=False, bind=engine),
        csv_file: UploadFile = File(...)):
    # Список точек маршрута
    points = []

    print('reading...')

    # Чтение CSV файла
    contents = csv_file.file.read()
    decoded_content = contents.decode("utf-8").splitlines()
    csv_reader = csv.DictReader(decoded_content)

    # # Создание объекта маршрута
    # route = Route()

    # Обработка каждой строки CSV файла
    for row in csv_reader:

        if type((row['population'])) is str:
            row['population'] = None
        if type(row['density']) is str:
            row['density'] = None
        if type(row['county_fips']) is str:
            row['county_fips'] = None
        print(row['zip'])
        # Создание объекта RoutePointCreate из данных строки
        route_point_data = RoutePointCreate(**row)
        # Создание объекта точки маршрута
        # with session as db:
        points.append(
            {"lat": route_point_data.lat, "lng": route_point_data.lng}
        )
        # points.append(
        #     {"points": [{"lat": route_point_data.lat, "lng": route_point_data.lng}]
        #      }
        # )
            # route_point = RoutePoint(**route_point_data.dict())
            # db.add(route_point)
            # db.commit()
            # db.refresh(route_point)
        #     print(route_point.id)
        # print(route_point_data, '\n')
    print('points', points)

    results = find_nearest_neighbors(points)
    print('result', results)
    for idx, item in enumerate(results):
        print(f"Route {idx + 1}: {item}")

    # Преобразование каждой пары координат в формат {"lat": ..., "lng": ...}
    formatted_results = [[{"lat": lat, "lng": lng} for lat, lng in route] for route in results]
    # # Создание списка маршрутов с их идентификаторами
    # routes = [{"id": idx + 1, "points": route} for idx, route in enumerate(formatted_results)]
    # Создание общего словаря с ключом "routes"
    output = {"points": formatted_results}
    print(output)
    # result = find_nearest_neighbors_2(points)
    # print('result 2', result)
    # for idx, item in enumerate(result):
    #     print(f"Route {idx + 1}: {item}")

    # # Сохранение маршрута в базе данных
    # with session as db:
    #     route = Route(*points)
    #     db.add_all([route])
    #     db.commit()
    #     db.refresh(route_point)
    # async with engine.begin() as conn:
    #     await conn.run_sync(Route.metadata.create_all.values(points=points))

    # with engine.connect() as conn:
    #     query = Route.insert().values(points=points)
    #     result = conn.execute(query)
    # route = Route(points=points)
    # db.add(route)
    # db.commit()
    # db.refresh(route)
    return {"message": "Route created successfully"}


# Реализуем обработчик для получения маршрута по его ID
@app.get("/api/routes/{route_id}", response_model=RouteData)
def get_route(route_id: int):
    db = SessionLocal()
    route = db.query(Route).filter(Route.id == route_id).first()
    db.close()
    if route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    return route
# @app.post("/api/routes/", response_model=RoutePointResponse)
# def create_route_point(route_point: RoutePointCreate, file: UploadFile = File(...)):
#     # Проверяем, что файл имеет расширение CSV
#     if not file.filename.endswith(".csv"):
#         raise HTTPException(status_code=400, detail="Файл должен быть в формате CSV")
#
#     db = SessionLocal()
#     db_route_point = RoutePoint(**route_point.dict())
#     db.add(db_route_point)
#     db.commit()
#     db.refresh(db_route_point)
#     return db_route_point


# # Получаем маршрут по его идентификатору
# @app.get("/api/routes/{id}", response_model=RoutePoint)
# def get_route_point(id: int):
#     # Проверяем, существует ли маршрут с указанным идентификатором
#     # В данном примере возвращаем пример данных из CSV файла
#     if id < 1 or id > 3:
#         raise HTTPException(status_code=404, detail="Маршрут не найден")
#
#     # Пример: возвращаем данные из CSV файла
#     data = sample_csv_data.strip().split("\n")[id - 1]
#     data_list = data.split(",")
#     return RoutePoint(
#         zip=int(data_list[0]),
#         lat=float(data_list[1]),
#         lng=float(data_list[2]),
#         city=data_list[3],
#         state_id=data_list[4],
#         state_name=data_list[5],
#         zcta=data_list[6],
#         parent_zcta=data_list[7],
#         population=int(data_list[8]),
#         density=float(data_list[9]),
#         county_fips=int(data_list[10]),
#         county_name=data_list[11],
#         county_weights=data_list[12],
#         county_names_all=data_list[13],
#         county_fips_all=data_list[14],
#         imprecise=data_list[15],
#         military=data_list[16],
#         timezone=data_list[17],
#     )

if __name__ == "__main__":
    import uvicorn
    print('start')
    uvicorn.run(app, host="0.0.0.0", port=8000)
