import os
from dotenv import load_dotenv

import threading
import tkinter as tk

import asyncio
from tapo import ApiClient
from tapo.requests import EnergyDataInterval
from datetime import datetime, timedelta, timezone

from DatabaseHandler import DatabaseHandler
from UserInterface import UserInterface 


# Function to fetch data asynchronously
async def fetch_smartplug_data(ui_instance):
    env_directory = "development.env"   # Customize this to your own .env file
    load_dotenv(env_directory) 
    tapo_username = os.getenv("TAPO_USERNAME")
    tapo_password = os.getenv("TAPO_PASSWORD")
    ip_address = os.getenv("SMARTPLUG_IP")

    client = ApiClient(tapo_username, tapo_password)
    device = await client.p115(ip_address)
    await device.refresh_session()

    while True:
        # Fetch raw device data
        device_info_json = await device.get_device_info_json()
        device_usage = await device.get_device_usage()
        current_power = await device.get_current_power()

        # Set the start and end date for the energy data
        start_date = datetime.now() - timedelta(days=7)
        end_date = datetime.now()

        # Fetch raw energy data
        energy_data = await device.get_energy_data(EnergyDataInterval.Daily, start_date, end_date)

        # Initialize the database handler
        db_handler = DatabaseHandler()

        # Process the raw data
        structured_data = db_handler.process_device_data(device_info_json, device_usage, current_power, energy_data)
        
        db_handler.add_timestamps(structured_data, device_info_json["time_diff"])
        db_handler.save_device_data(structured_data)

        # Extract data from structured_data to update the UI
        ui_instance.data["power"] = structured_data["power_usage"]["current_power"]
        ui_instance.data["status"] = "ON" if structured_data["device"]["status"]["is_on"] else "OFF"
        ui_instance.data["signal"] = structured_data["device"]["network"]["signal_strength"]

        # Update the UI in the main thread
        ui_instance.update_interface()

        await asyncio.sleep()  # Fetch data every 5 seconds


def start_async_loop(ui_instance):
    asyncio.run(fetch_smartplug_data(ui_instance))


if __name__ == "__main__":
    # Initialize TKinter and UI
    root = tk.Tk()
    ui_instance = UserInterface(root)

    # Start the Tapo API async loop in a separate thread
    threading.Thread(target=start_async_loop, args=(ui_instance,), daemon=True).start()

    # Start the Tkinter main loop
    root.mainloop()
