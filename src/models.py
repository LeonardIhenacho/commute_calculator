from pydantic import BaseModel, Field
from typing import Optional, List


class WeatherData(BaseModel):
    temperature: int
    humidity: float
    wind_speed: Optional[float] = None


class TrafficData(BaseModel):
    average_speed: float
    traffic_density: List[float]
    incident_reports: Optional[int] = None


class RoadConditionsData(BaseModel):
    road_quality: int
    lighting_conditions: int
    accident_history: int


class CommuteQualityInput(BaseModel):
    comfort_index: float
    traffic_flow_efficiency: float
    safety_score: float


class CommuteQualityOutput(BaseModel):
    overall_commute_quality_score: float
    commute_quality: str
