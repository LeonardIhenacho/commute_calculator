from .models import WeatherData, TrafficData, RoadConditionsData
from typing import Optional


class CommuteCalculator:

    @staticmethod
    def calculate_comfort_index(weather: WeatherData) -> float:
        result = (100 - weather.humidity) + (30 - weather.temperature)
        if weather.wind_speed:
            result -= 0.5 * weather.wind_speed
        return result

    @staticmethod
    def calculate_traffic_flow_efficiency(traffic: TrafficData) -> float:
        traffic_density_sum = sum(traffic.traffic_density) + 1
        result = traffic.average_speed / traffic_density_sum
        if traffic.incident_reports:
            result -= 2 * traffic.incident_reports
        return result

    @staticmethod
    def calculate_safety_score(traffic: TrafficData, road: RoadConditionsData, wind_speed: Optional[float]) -> float:
        inverse_density_sum = 1 / (sum(traffic.traffic_density) + 1)
        safety_component = road.road_quality * (road.accident_history + 1) * inverse_density_sum
        lighting_speed_component = road.lighting_conditions * traffic.average_speed
        result = safety_component + lighting_speed_component
        if traffic.incident_reports:
            result -= traffic.incident_reports
        if wind_speed is not None:
            result -= wind_speed
        return result

    @staticmethod
    def calculate_commute_quality(comfort_index: float, traffic_flow_efficiency: float, safety_score: float) -> float:
        overall_score = (comfort_index + traffic_flow_efficiency + safety_score) / 3
        return overall_score

    @staticmethod
    def evaluate_commute_quality(overall_score: float) -> str:
        if overall_score < 0:
            return "Poor"
        elif 0 <= overall_score <= 50:
            return "Average"
        else:
            return "Good"
