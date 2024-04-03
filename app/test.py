import unittest
from .main import find_nearest_neighbors


class TestFindNearestNeighbors(unittest.TestCase):
    def test_find_nearest_neighbors_simple(self):
        # Создаем список простых точек с координатами
        points = [
            {"lat": 0, "lng": 0},
            {"lat": 1, "lng": 1},
            {"lat": 2, "lng": 2},
        ]

        # Вызываем функцию для поиска ближайших соседей
        nearest_neighbors = find_nearest_neighbors(points, n_neighbors=2)

        # Проверяем, что результат соответствует ожидаемому
        self.assertEqual(len(nearest_neighbors), 3)
        self.assertEqual(len(nearest_neighbors[0]), 2)
        self.assertEqual(len(nearest_neighbors[1]), 2)
        self.assertEqual(len(nearest_neighbors[2]), 2)

    def test_find_nearest_neighbors_complex(self):
        # Создаем список более сложных точек с координатами
        points = [
            {"lat": 37.7749, "lng": -122.4194},
            {"lat": 34.0522, "lng": -118.2437},
            {"lat": 41.8781, "lng": -87.6298},
            {"lat": 40.7128, "lng": -74.0060},
            {"lat": 29.7604, "lng": -95.3698}
        ]

        # Вызываем функцию для поиска ближайших соседей
        nearest_neighbors = find_nearest_neighbors(points, n_neighbors=2)

        # Проверяем, что результат соответствует ожидаемому
        self.assertIsInstance(nearest_neighbors, list)
        self.assertEqual(len(nearest_neighbors), len(points))
        for route in nearest_neighbors:
            self.assertIsInstance(route, list)
            self.assertEqual(len(route), 2)
            for point in route:
                self.assertIsInstance(point, tuple)
                self.assertEqual(len(point), 2)
                self.assertIsInstance(point[0], float)
                self.assertIsInstance(point[1], float)


if __name__ == '__main__':
    unittest.main()
