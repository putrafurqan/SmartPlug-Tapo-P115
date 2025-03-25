import os
from dotenv import load_dotenv
import asyncio
from datetime import datetime, timedelta
from tapo import ApiClient
from tapo.requests import EnergyDataInterval

load_dotenv("development.env")

async def main():
    tapo_username = os.getenv("TAPO_USERNAME")
    tapo_password = os.getenv("TAPO_PASSWORD")
    ip_address = os.getenv("SMARTPLUG_IP")

    client = ApiClient(tapo_username, tapo_password)
    device = await client.p115(ip_address)

    print("Refreshing session...")
    await device.refresh_session()

    print("Turning device on...")
    await device.on()
    await asyncio.sleep(2)

    print("Turning device off...")
    await device.off()
    await asyncio.sleep(2)

    print("Getting device info...")
    device_info = await device.get_device_info()
    print(f"Device info: {device_info.to_dict()}")

    print("Getting device info (JSON)...")
    device_info_json = await device.get_device_info_json()
    print(f"Device info JSON: {device_info_json}")

    print("Getting device usage...")
    device_usage = await device.get_device_usage()
    print(f"Device usage: {device_usage.to_dict()}")

    print("Getting current power...")
    current_power = await device.get_current_power()
    print(f"Current power: {current_power.to_dict()}")

    print("Getting energy usage...")
    energy_usage = await device.get_energy_usage()
    print(f"Energy usage: {energy_usage.to_dict()}")

    print("Getting energy data...")
    start_date = datetime.now() - timedelta(days=7)
    end_date = datetime.now()
    energy_data = await device.get_energy_data(EnergyDataInterval.Daily, start_date, end_date)
    print(f"Energy data: {energy_data.to_dict()}")

if __name__ == "__main__":
    asyncio.run(main())