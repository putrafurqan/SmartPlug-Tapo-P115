import os
from datetime import datetime, timedelta, timezone
import json

class DatabaseHandler:
    def __init__(self, base_dir="database"):
        self.base_dir = base_dir
        self.ensure_directory_exists()

    def ensure_directory_exists(self):
        os.makedirs(self.base_dir, exist_ok=True)

    def generate_filename(self):
        return f"device_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    def save_device_data(self, data):
        filename = self.generate_filename()
        filepath = os.path.join(self.base_dir, filename)

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)

        return filepath

    def add_timestamps(self, data, timezone_offset=0):
        utc_now = datetime.now(timezone.utc)
        local_time = utc_now + timedelta(minutes=timezone_offset)

        if "metadata" not in data:
            data["metadata"] = {}

        data["metadata"].update({
            "timestamp_utc": utc_now.isoformat(),
            "timestamp_local": local_time.isoformat(),
            "timezone_offset": timezone_offset
        })

        return data
    
    def calculate_bill(self, power_usage):
        rate = 1699.53  # Rate in IDR per kWh
        return (power_usage/1000) * rate
            
    def process_device_data(self, device_info_json, device_usage, current_power, energy_data):
        timezone_offset = device_info_json["time_diff"]
        return {
            "device": {
                "id": device_info_json["device_id"],
                "model": device_info_json["model"],
                "nickname": device_info_json["nickname"],
                "type": device_info_json["type"],
                "status": {
                    "is_on": device_info_json["device_on"],
                    "uptime": device_info_json["on_time"]
                },
                "firmware": {
                    "version": device_info_json["fw_ver"],
                    "id": device_info_json["fw_id"]
                },
                "hardware": {
                    "version": device_info_json["hw_ver"],
                    "id": device_info_json["hw_id"]
                },
                "network": {
                    "ip": device_info_json["ip"],
                    "mac": device_info_json["mac"],
                    "ssid": device_info_json["ssid"],
                    "signal_strength": device_info_json["rssi"],
                    "signal_level": device_info_json["signal_level"]
                },
                "location": {
                    "region": device_info_json["region"],
                    "latitude": device_info_json["latitude"],
                    "longitude": device_info_json["longitude"],
                    "timezone_offset": timezone_offset
                },
                "protection_status": {
                    "overcurrent": device_info_json["overcurrent_status"],
                    "overheat": device_info_json["overheat_status"],
                    "power_protection": device_info_json["power_protection_status"]
                }
            },
            "power_usage": {
                "current_power": current_power.current_power,
                "daily": device_usage.power_usage.today,
                "weekly": device_usage.power_usage.past7,
                "monthly": device_usage.power_usage.past30
            },
            "runtime": {
                "daily": device_usage.time_usage.today,
                "weekly": device_usage.time_usage.past7,
                "monthly": device_usage.time_usage.past30
            },
            "energy_data": {
                "interval_minutes": energy_data.interval,
                "start_timestamp": energy_data.start_timestamp,
                "end_timestamp": energy_data.end_timestamp,
            },
            "bill": {
                "daily": self.calculate_bill(device_usage.power_usage.today),
                "weekly": self.calculate_bill(device_usage.power_usage.past7),
                "monthly": self.calculate_bill(device_usage.power_usage.past30)
            },
            "carbon_emission": {
                "current_emission": current_power.current_power * 0.000646
            }
        }

