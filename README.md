# TAPO P115 Smart Plug Monitor

A Python application that monitors and records energy usage data from TAPO P115 smart plugs, featuring both a graphical user interface and data logging capabilities.

## Features

- Real-time monitoring of power consumption
- Device status tracking (ON/OFF)
- Network signal strength visualization
- Safety status indicators (overcurrent, overheat, protection)
- Automatic data logging with timestamps
- Historical energy data collection
- Simple graphical interface

## Requirements

- Python 3.7+
- TAPO P115 Smart Plug
- Network connectivity to the smart plug

## Installation

1. Clone this repository:
   ```bash
   git clone git@github.com:putrafurqan/SmartPlug-Tapo-P115.git
   cd tapo-p115-monitor
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file based on the `development.env` template and fill in your credentials:
   ```
   TAPO_USERNAME=your_tapo_email
   TAPO_PASSWORD=your_tapo_password
   SMARTPLUG_IP=your_plug_ip_address
   ```

## Usage

Run the application:
```bash
python main.py
```

The application will:
1. Connect to your TAPO P115 smart plug
2. Display real-time monitoring data in a graphical interface
3. Continuously save device data to JSON files in the `database/` directory

### Interface Explanation

![image](https://github.com/user-attachments/assets/04a727e9-d493-4b4d-984d-d6dd4607bc93)


1. **Signal Strength**: Visual indicator of WiFi signal quality (green = good, yellow = fair, red = poor)
2. **Power Consumption**: Current power draw in watts with color coding:
   - Green: <200W
   - Orange: 200-1000W
   - Red: >1000W
3. **Device Status**: ON (green) or OFF (red)
4. **Status Indicators**: 
   - Overcurrent (green/yellow)
   - Overheat (green/yellow)
   - Protection (green/yellow)
5. **Refresh Button**: Manually refresh device data

## Data Storage

The application saves data in JSON format to the `database/` directory with filenames following the pattern `device_data_YYYYMMDD_HHMMSS.json`.

## File Structure

```
tapo-p115-monitor/
├── database/                # Directory for stored data files
│   └── sample/              # Example data files
├── .env                     # Environment variables (template)
├── .gitignore
├── DatabaseHandler.py       # Data processing and storage logic
├── development.env          # Development environment template
├── main.py                  # Main application entry point
├── README.md                # This documentation
├── requirements.txt         # Python dependencies
└── UserInterface.py         # GUI implementation
```

## Dependencies

- `python-tapo` - Official TAPO API client
- `python-dotenv` - Environment variable management
- `tkinter` - Built-in Python GUI toolkit
- `asyncio` - For asynchronous operations
