import sys
import json
import os
from jyotisha.panchaanga.spatio_temporal import City
from jyotisha.panchaanga.temporal.time import Date
from jyotisha.panchaanga.temporal import ComputationSystem
from jyotisha.panchaanga.temporal.month import LunarMonthAssigner
from jyotisha.panchaanga.temporal.zodiac import Ayanamsha
from jyotisha.panchaanga.spatio_temporal.daily import DailyPanchaanga

def main():
    if len(sys.argv) < 8:
        print("Usage: python write_daily_panchaanga_json.py <city name> <lat> <lon> <tz name> <year> <month> <day> [script]")
        sys.exit(1)
    city_name = sys.argv[1]
    lat = sys.argv[2]
    lon = sys.argv[3]
    tz = sys.argv[4]
    year = int(sys.argv[5])
    month = int(sys.argv[6])
    day = int(sys.argv[7])
    script = sys.argv[8] if len(sys.argv) > 8 else 'devanagari'

    if not lat or not lon:
        return jsonify({'error': 'Latitude and longitude are required. Please allow location access or enter coordinates.'}), 400

    print("Creating City...")
    city = City(name=city_name, latitude=lat, longitude=lon, timezone=tz)
    print("Creating Date...")
    date = Date(year=year, month=month, day=day)
    print("Creating ComputationSystem...")
    computation_system = ComputationSystem(
        lunar_month_assigner_type=LunarMonthAssigner.MULTI_NEW_MOON_SIDEREAL_MONTH_ADHIKA_AMAANTA,
        ayanaamsha_id=Ayanamsha.CHITRA_AT_180
    )
    print("Creating DailyPanchaanga...")
    daily_panchaanga = DailyPanchaanga(city=city, date=date, computation_system=computation_system)
    print("Serializing to JSON...")
    json_data = json.dumps(daily_panchaanga.to_json_map(), ensure_ascii=False, indent=2)
    output_dir = os.path.join(os.path.dirname(__file__), '../../../OUTPUT')
    os.makedirs(output_dir, exist_ok=True)
    output_filename = f"{city_name}-{year:04d}-{month:02d}-{day:02d}.json"
    output_path = os.path.join(output_dir, output_filename)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(json_data)
    sys.stdout.reconfigure(encoding='utf-8')
    print(json_data)
    print(f"JSON written to {output_path}")

if __name__ == "__main__":
    main() 