import unittest
from src.calculator import CommuteCalculator
from src.models import WeatherData, TrafficData, RoadConditionsData


class TestCommuteCalculator(unittest.TestCase):

    def test_calculate_comfort_index(self):
        weather_data = WeatherData(temperature=25, humidity=40.0, wind_speed=10.0)
        result = CommuteCalculator.calculate_comfort_index(weather_data)
        expected_result = (100 - 40.0) + (30 - 25) - (0.5 * 10.0)
        self.assertAlmostEqual(result, expected_result, places=2)

    def test_calculate_traffic_flow_efficiency(self):
        traffic_data = TrafficData(average_speed=60.0, traffic_density=[20.0, 15.0, 25.0], incident_reports=2)
        result = CommuteCalculator.calculate_traffic_flow_efficiency(traffic_data)
        expected_result = 60.0 / (sum([20.0, 15.0, 25.0]) + 1) - 2 * 2
        self.assertAlmostEqual(result, expected_result, places=2)

    def test_calculate_safety_score(self):
        traffic_data = TrafficData(average_speed=60.0, traffic_density=[20.0, 15.0, 25.0], incident_reports=2)
        road_data = RoadConditionsData(road_quality=5, lighting_conditions=8, accident_history=2)
        wind_speed = 10.0
        result = CommuteCalculator.calculate_safety_score(traffic_data, road_data, wind_speed)
        expected_result = (5 * (2 + 1) * (1 / (sum([20.0, 15.0, 25.0]) + 1))) + (8 * 60.0) - 2 - 10.0
        self.assertAlmostEqual(result, expected_result, places=2)

    def test_calculate_commute_quality(self):
        comfort_index = 50.0
        traffic_flow_efficiency = 30.0
        safety_score = 70.0
        result = CommuteCalculator.calculate_commute_quality(comfort_index, traffic_flow_efficiency, safety_score)
        expected_result = (50.0 + 30.0 + 70.0) / 3
        self.assertAlmostEqual(result, expected_result, places=2)

    def test_evaluate_commute_quality(self):
        result = CommuteCalculator.evaluate_commute_quality(60.0)
        self.assertEqual(result, "Good")

        result = CommuteCalculator.evaluate_commute_quality(50.0)
        self.assertEqual(result, "Average")

        result = CommuteCalculator.evaluate_commute_quality(-10.0)
        self.assertEqual(result, "Poor")


if __name__ == '__main__':
    unittest.main()
