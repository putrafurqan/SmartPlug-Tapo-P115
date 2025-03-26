import tkinter as tk
from tkinter import Label, Button, Frame
import random

class UserInterface:
    def __init__(self, master):
        self.master = master
        self.master.title("Live Monitoring: TAPO P115 Smart Plug")
        self.master.geometry("400x400")
        self.master.configure(bg="#f0f0f0")

        self.create_widgets()
        self.data = {
            "power": 0,  # int: Power consumption in watts (range: 0 - 4000 W)
            "status": "OFF",  # str: Device status, "ON" or "OFF"
            "overcurrent": "Normal",  # str: Overcurrent status, "Normal" or "Warning"
            "overheat": "Normal",  # str: Overheat status, "Normal" or "Warning"
            "protection": "Normal",  # str: Protection status, "Normal" or "Triggered"
            "signal": -60  # int: Signal strength in dBm (range: -80 to -30 dBm)
        }

    def create_widgets(self):
        self.frame = Frame(self.master, bg="#f0f0f0")
        self.frame.pack(pady=10)

        self.signal_frame = Frame(self.master, bg="#f0f0f0")
        self.signal_frame.pack(anchor="ne", padx=10, pady=10)

        self.signal_label = Label(self.signal_frame, text="Signal\nStrength", font=("Arial", 7), bg="#f0f0f0")
        self.signal_label.pack(side="left")
        self.signal_dots = Label(self.signal_frame, text="● ● ●", font=("Arial", 14), bg="#f0f0f0", fg="white")
        self.signal_dots.pack(side="left")

        self.power_label = Label(self.frame, text="Power Consumption:", font=("Arial", 12), bg="#f0f0f0")
        self.power_value = Label(self.frame, text="-- W", font=("Arial", 12), bg="#f0f0f0", fg="black")

        self.status_label = Label(self.frame, text="Device Status:", font=("Arial", 12), bg="#f0f0f0")
        self.status_value = Label(self.frame, text="--", font=("Arial", 12), bg="#f0f0f0", fg="black")

        self.power_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.power_value.grid(row=0, column=1, sticky="w", padx=10, pady=5)
        self.status_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.status_value.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        self.bottom_frame = Frame(self.master, bg="#f0f0f0")
        self.bottom_frame.pack(pady=10)

        self.overcurrent_label = Label(self.bottom_frame, text="Overcurrent:", font=("Arial", 12), bg="#f0f0f0")
        self.overcurrent_dot = Label(self.bottom_frame, text="●", font=("Arial", 12), bg="green")

        self.overheat_label = Label(self.bottom_frame, text="Overheat:", font=("Arial", 12), bg="#f0f0f0")
        self.overheat_dot = Label(self.bottom_frame, text="●", font=("Arial", 12), bg="green")

        self.protection_label = Label(self.bottom_frame, text="Protection:", font=("Arial", 12), bg="#f0f0f0")
        self.protection_dot = Label(self.bottom_frame, text="●", font=("Arial", 12), bg="green")

        self.overcurrent_label.grid(row=0, column=0, padx=10, pady=5)
        self.overcurrent_dot.grid(row=1, column=0, padx=10, pady=5)

        self.overheat_label.grid(row=0, column=1, padx=10, pady=5)
        self.overheat_dot.grid(row=1, column=1, padx=10, pady=5)

        self.protection_label.grid(row=0, column=2, padx=10, pady=5)
        self.protection_dot.grid(row=1, column=2, padx=10, pady=5)

        self.power_button = Button(self.master, text="Power On/Off", font=("Arial", 14), bg="#FF0000", fg="white", activebackground="#BF0000")
        self.power_button.pack(pady=20)

        self.refresh_button = Button(self.master, text="Refresh Data", font=("Arial", 14), bg="#4CAF50", fg="white", activebackground="#45a049")
        self.refresh_button.pack(pady=20)
        


    def update_interface(self):
        self.update_power(self.data["power"])
        self.update_status(self.data["status"])
        self.update_overcurrent(self.data["overcurrent"])
        self.update_overheat(self.data["overheat"])
        self.update_protection(self.data["protection"])
        self.update_signal_strength(self.data["signal"])

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
