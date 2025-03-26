import tkinter as tk
from tkinter import Label, Button, Frame
import random

class UserInterface:
    def __init__(self, master, device, data, callback_power, callback_refresh):
        self.master = master
        self.master.title("Live Monitoring: TAPO P115 Smart Plug")
        self.master.geometry("400x400")
        self.master.configure(bg="#f0f0f0")

        self.callback_power = callback_power
        self.callback_refresh = callback_refresh

        self.device = device
        self.data = data

        self.create_widgets()
        self.data = {
            "power": 0,  # int: Power consumption in watts (range: 0 - 4000 W)
            "status": "OFF",  # str: Device status, "ON" or "OFF"
            "overcurrent": "Normal",  # str: Overcurrent status, "Normal" or "Warning"
            "overheat": "Normal",  # str: Overheat status, "Normal" or "Warning"
            "protection": "Normal",  # str: Protection status, "Normal" or "Triggered"
            "signal": -60,  # int: Signal strength in dBm (range: -80 to -30 dBm)
            "bill": 0,
            "power_usage": 0,
            "carbon_emission": 0
        }

    def set_device(self, device):
        self.device = device

    def create_widgets(self):
        # Main frame for most content
        self.frame = Frame(self.master, bg="#f0f0f0")
        self.frame.pack(pady=10, fill="x", expand=True)
        
        # Signal frame in top-right corner
        self.signal_frame = Frame(self.master, bg="#f0f0f0")
        self.signal_frame.place(relx=1.0, rely=0, anchor="ne", x=-10, y=10) 
        
        self.signal_label = Label(self.signal_frame, text="Signal Strength", 
                                font=("Arial", 8), bg="#f0f0f0")
        self.signal_label.pack(side="top", anchor="e")
        
        self.signal_dots = Label(self.signal_frame, text="● ● ●", 
                            font=("Arial", 14), bg="#f0f0f0", fg="white")
        self.signal_dots.pack(side="top", anchor="e")

        # Main content using grid
        self.power_label = Label(self.frame, text="Power Consumption:", 
                            font=("Arial", 12), bg="#f0f0f0")
        self.power_value = Label(self.frame, text="-- W", 
                            font=("Arial", 12), bg="#f0f0f0", fg="black")

        self.status_label = Label(self.frame, text="Device Status:", 
                                font=("Arial", 12), bg="#f0f0f0")
        self.status_value = Label(self.frame, text="--", 
                                font=("Arial", 12), bg="#f0f0f0", fg="black")

        self.billing_label = Label(self.frame, text="Bill (monthly):", 
                                font=("Arial", 12), bg="#f0f0f0")
        self.billing_value = Label(self.frame, text="Rp.0.00", 
                                font=("Arial", 12), bg="#f0f0f0", fg="black")

        self.power_usage_label = Label(self.frame, text="Usage (monthly):", 
                                    font=("Arial", 12), bg="#f0f0f0")
        self.power_usage_value = Label(self.frame, text="0 W", 
                                    font=("Arial", 12), bg="#f0f0f0", fg="black")

        self.carbon_emission_label = Label(self.frame, text="Carbon Emission:", 
                                        font=("Arial", 12), bg="#f0f0f0")
        self.carbon_emission_value = Label(self.frame, text="0 gCO2", 
                                        font=("Arial", 12), bg="#f0f0f0", fg="black")

        # Grid layout for main content
        self.power_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.power_value.grid(row=0, column=1, sticky="w", padx=10, pady=5)
        self.status_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.status_value.grid(row=1, column=1, sticky="w", padx=10, pady=5)
        self.billing_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.billing_value.grid(row=2, column=1, sticky="w", padx=10, pady=5)
        self.power_usage_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.power_usage_value.grid(row=3, column=1, sticky="w", padx=10, pady=5)
        self.carbon_emission_label.grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.carbon_emission_value.grid(row=4, column=1, sticky="w", padx=10, pady=5)

        # Bottom frame for status indicators
        self.bottom_frame = Frame(self.master, bg="#f0f0f0")
        self.bottom_frame.pack(side="bottom", pady=10, fill="x")

        self.overcurrent_label = Label(self.bottom_frame, text="Overcurrent:", 
                                    font=("Arial", 12), bg="#f0f0f0")
        self.overcurrent_dot = Label(self.bottom_frame, text="●", 
                                font=("Arial", 12), bg="green")

        self.overheat_label = Label(self.bottom_frame, text="Overheat:", 
                                font=("Arial", 12), bg="#f0f0f0")
        self.overheat_dot = Label(self.bottom_frame, text="●", 
                                font=("Arial", 12), bg="green")

        self.protection_label = Label(self.bottom_frame, text="Protection:", 
                                    font=("Arial", 12), bg="#f0f0f0")
        self.protection_dot = Label(self.bottom_frame, text="●", 
                                font=("Arial", 12), bg="green")

        # Grid layout for status indicators
        self.overcurrent_label.grid(row=0, column=0, padx=10, pady=5)
        self.overcurrent_dot.grid(row=1, column=0, padx=10, pady=5)
        self.overheat_label.grid(row=0, column=1, padx=10, pady=5)
        self.overheat_dot.grid(row=1, column=1, padx=10, pady=5)
        self.protection_label.grid(row=0, column=2, padx=10, pady=5)
        self.protection_dot.grid(row=1, column=2, padx=10, pady=5)

        # Buttons
        self.power_button = Button(self.master, text="Power On/Off", 
                                font=("Arial", 14), bg="#FF0000", fg="white", 
                                activebackground="#BF0000", command=self.callback_power)
        self.power_button.pack(pady=10)

        self.refresh_button = Button(self.master, text="Refresh Data", 
                                font=("Arial", 14), bg="#4CAF50", fg="white", 
                                activebackground="#45a049", command=self.callback_refresh)
        self.refresh_button.pack(pady=10)

    def update_interface(self):
        self.update_power(self.data["power"])
        self.update_status(self.data["status"])
        self.update_overcurrent(self.data["overcurrent"])
        self.update_overheat(self.data["overheat"])
        self.update_protection(self.data["protection"])
        self.update_signal_strength(self.data["signal"])
        self.update_bill(self.data["bill"])
        self.update_power_usage(self.data["power_usage"])
        self.update_carbon_emission(self.data["carbon_emission"])

    def update_power(self, power):
        if power > 1000:
            color = "red"
        elif power >= 200:
            color = "orange"
        else:
            color = "green"

        self.power_value.config(text=f"{power} W", fg=color)

    def update_status(self, status):
        if status == "ON":
            color = "green"
        else:
            color = "red"

        self.status_value.config(text=status, fg=color)

    def update_overcurrent(self, status):
        if status == "Normal":
            color = "green"
        else:
            color = "yellow"

        self.overcurrent_dot.config(bg=color)

    def update_overheat(self, status):
        if status == "Normal":
            color = "green"
        else:
            color = "yellow"

        self.overheat_dot.config(bg=color)

    def update_protection(self, status):
        if status == "Normal":
            color = "green"
        else:
            color = "yellow"

        self.protection_dot.config(bg=color)

    def update_signal_strength(self, signal):
        if signal > -50:
            self.signal_dots.config(text="● ● ●", fg="green")
        elif -70 <= signal <= -50:
            self.signal_dots.config(text="● ● ○", fg="yellow")
        else:
            self.signal_dots.config(text="● ○ ○", fg="red")

    def update_bill(self, bill):
        formatted_bill = f"Rp.{bill:,.2f}"
        self.billing_value.config(text=formatted_bill)

    def update_power_usage(self, power_usage):
        self.power_usage_value.config(text=f"{power_usage} W")

    def update_carbon_emission(self, carbon_emission):
        self.carbon_emission_value.config(text=f"{carbon_emission} gCO2")
