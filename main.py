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

async def power_switch_callback(ui_instance):
    if ui_instance.device is None:
        return
        
    if ui_instance.data["status"] == "ON":
        await ui_instance.device.off()
    else:
        await ui_instance.device.on()
    # Refresh the device status immediately
    await ui_instance.device.refresh_session()

async def refresh_callback(ui_instance):
    if ui_instance.device is None:
        return
    await ui_instance.device.refresh_session()

def sync_power_switch(ui_instance):
    """Wrapper to run async callback in a new thread"""
    def callback():
        asyncio.run(power_switch_callback(ui_instance))
    threading.Thread(target=callback, daemon=True).start()

def sync_refresh(ui_instance):
    """Wrapper to run async callback in a new thread"""
    def callback():
        asyncio.run(refresh_callback(ui_instance))
    threading.Thread(target=callback, daemon=True).start()

async def fetch_smartplug_data(ui_instance):
    env_directory = "development.env"
    load_dotenv(env_directory) 
    tapo_username = os.getenv("TAPO_USERNAME")
    tapo_password = os.getenv("TAPO_PASSWORD")
    ip_address = os.getenv("SMARTPLUG_IP")

    client = ApiClient(tapo_username, tapo_password)
    device = await client.p115(ip_address)
    await device.refresh_session()
    
    # Update the UI with the device reference
    ui_instance.set_device(device)

    while True:
        try:
            device_info_json = await device.get_device_info_json()
            device_usage = await device.get_device_usage()
            current_power = await device.get_current_power()

            start_date = datetime.now() - timedelta(days=7)
            end_date = datetime.now()

            energy_data = await device.get_energy_data(EnergyDataInterval.Daily, start_date, end_date)

            db_handler = DatabaseHandler()
            structured_data = db_handler.process_device_data(device_info_json, device_usage, current_power, energy_data)
            
            db_handler.add_timestamps(structured_data, device_info_json["time_diff"])
            db_handler.save_device_data(structured_data)

            ui_instance.data["power"] = structured_data["power_usage"]["current_power"]
            ui_instance.data["status"] = "ON" if structured_data["device"]["status"]["is_on"] else "OFF"
            ui_instance.data["signal"] = structured_data["device"]["network"]["signal_strength"]

            ui_instance.update_interface()
        except Exception as e:
            print(f"Error fetching data: {e}")
        
        await asyncio.sleep(5)

def start_async_loop(ui_instance):
    asyncio.run(fetch_smartplug_data(ui_instance))

if __name__ == "__main__":
    root = tk.Tk()
    # Pass the callbacks with the ui_instance as partial
    ui_instance = UserInterface(root, None, {}, 
                              lambda: sync_power_switch(ui_instance), 
                              lambda: sync_refresh(ui_instance))

    threading.Thread(target=start_async_loop, args=(ui_instance,), daemon=True).start()
    root.mainloop()