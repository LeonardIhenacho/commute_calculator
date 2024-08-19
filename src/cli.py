import argparse
import json
from .calculator import CommuteCalculator
from .models import WeatherData, TrafficData, RoadConditionsData, CommuteQualityInput, CommuteQualityOutput
from pydantic import ValidationError


def prompt_for_weather_data() -> WeatherData:
    temperature = int(input("Enter the temperature (int): "))
    humidity = float(input("Enter the humidity (float): "))
    wind_speed = input("Enter the wind speed (float, optional, press Enter to skip): ")
    wind_speed = float(wind_speed) if wind_speed else None
    return WeatherData(temperature=temperature, humidity=humidity, wind_speed=wind_speed)


def prompt_for_traffic_data() -> TrafficData:
    average_speed = float(input("Enter the average speed (float): "))
    traffic_density = list(
        map(float, input("Enter traffic density as a list of floats (e.g., 20.0 15.0 25.0): ").split()))
    incident_reports = input("Enter the number of incident reports (optional, press Enter to skip): ")
    incident_reports = int(incident_reports) if incident_reports else None
    return TrafficData(average_speed=average_speed, traffic_density=traffic_density, incident_reports=incident_reports)


def prompt_for_road_conditions_data() -> RoadConditionsData:
    road_quality = int(input("Enter road quality (int): "))
    lighting_conditions = int(input("Enter lighting conditions (int): "))
    accident_history = int(input("Enter accident history (int): "))
    return RoadConditionsData(road_quality=road_quality, lighting_conditions=lighting_conditions,
                              accident_history=accident_history)


def generate_json_template():
    template = {
        "weather_data": {
            "temperature": "int",
            "humidity": "float",
            "wind_speed": "float (optional)"
        },
        "traffic_data": {
            "average_speed": "float",
            "traffic_density": "[float, float, float]",
            "incident_reports": "int (optional)"
        },
        "road_conditions_data": {
            "road_quality": "int",
            "lighting_conditions": "int",
            "accident_history": "int"
        }
    }
    return json.dumps(template, indent=4)


def run_cli():
    parser = argparse.ArgumentParser(description="Calculate commute quality based on input data.")
    parser.add_argument('-j', '--json', type=str, help='Input JSON string')
    parser.add_argument('-i', '--interactive', action='store_true', help='Enter inputs interactively')
    parser.add_argument('-g', '--generate-template', action='store_true', help='Generate JSON template')

    args = parser.parse_args()

    if args.generate_template:
        print("JSON Template:")
        print(generate_json_template())
        return

    calculator = CommuteCalculator()

    if args.json:
        input_data = json.loads(args.json)
        try:
            weather_data = WeatherData(**input_data["weather_data"])
            traffic_data = TrafficData(**input_data["traffic_data"])
            road_conditions_data = RoadConditionsData(**input_data["road_conditions_data"])
        except ValidationError as e:
            print(f"Input validation error: {e}")
            return

    elif args.interactive:
        weather_data = prompt_for_weather_data()
        traffic_data = prompt_for_traffic_data()
        road_conditions_data = prompt_for_road_conditions_data()

    else:
        print("Please provide input JSON string with '-j' or use interactive mode with '-i'.")
        return

    comfort_index = calculator.calculate_comfort_index(weather_data)
    traffic_flow_efficiency = calculator.calculate_traffic_flow_efficiency(traffic_data)
    safety_score = calculator.calculate_safety_score(traffic_data, road_conditions_data, weather_data.wind_speed)

    overall_score = calculator.calculate_commute_quality(comfort_index, traffic_flow_efficiency, safety_score)
    commute_quality = calculator.evaluate_commute_quality(overall_score)

    commute_quality_output = CommuteQualityOutput(
        overall_commute_quality_score=overall_score,
        commute_quality=commute_quality
    )

    print("\nCommute Quality Results:")
    print(commute_quality_output.json())


if __name__ == "__main__":
    run_cli()
