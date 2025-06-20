# PyTZ Buddy - Timezone Converter 🌍

A simple Python application that helps you find timezone information for any location and converts it to major timezones around the world.

## Features

- 🔍 **Location Lookup**: Enter any location (city, state, country) and get its timezone
- 🕐 **Time Conversion**: Automatically converts current time to major world timezones
- 🆓 **Free APIs**: Uses only free services (OpenStreetMap Nominatim for geocoding)
- 🎯 **Simple Interface**: Clean command-line interface that's easy to use

## Installation

1. **Clone or download** this project to your local machine
2. **Navigate** to the project directory:
   ```bash
   cd pytz_buddy
   ```
3. **Activate** the virtual environment:
   ```bash
   source pytz_venv/bin/activate
   ```
4. **Install dependencies** (if not already installed):
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
python main.py
```

Then enter any location when prompted:
- `Duncan, Oklahoma`
- `Paris, France`
- `Tokyo, Japan`
- `New York, NY`

The app will show:
- The exact location found
- Local timezone information
- Current time in that timezone
- Converted times for major world timezones

## Example Output

```
🌍 Welcome to PyTZ Buddy - Timezone Converter!
Enter location: Duncan, Oklahoma

Looking up location: Duncan, Oklahoma
Found: Duncan, Stephens County, Oklahoma, United States
Timezone: America/Chicago

============================================================
TIMEZONE INFORMATION
============================================================
Location: Duncan, Stephens County, Oklahoma, United States
Coordinates: 34.5015, -97.9578
Local Timezone: America/Chicago

CURRENT TIME CONVERSIONS:
------------------------------------------------------------
★ America/Chicago      | 2025-06-20 15:30:45 CST (LOCAL)

  US/Eastern            | 2025-06-20 16:30:45 EST
  US/Mountain           | 2025-06-20 14:30:45 MST
  US/Pacific            | 2025-06-20 13:30:45 PST
  Europe/London         | 2025-06-20 21:30:45 GMT
  Europe/Paris          | 2025-06-20 22:30:45 CET
  Asia/Tokyo            | 2025-06-21 06:30:45 JST
  Asia/Shanghai         | 2025-06-21 05:30:45 CST
  Australia/Sydney      | 2025-06-21 07:30:45 AEDT
  UTC                   | 2025-06-20 21:30:45 UTC
============================================================
```

## Dependencies

- **requests**: For HTTP requests
- **pytz**: For timezone handling
- **geopy**: For geocoding locations
- **timezonefinder**: For finding timezones from coordinates

## Technical Details

- Uses OpenStreetMap Nominatim API (free) for geocoding
- Uses offline timezone data for coordinate-to-timezone mapping
- Handles daylight saving time automatically
- No API keys required

## Troubleshooting

- **Location not found**: Try being more specific (add state/country)
- **Network errors**: Check your internet connection
- **Import errors**: Make sure virtual environment is activated and dependencies are installed

Type `quit` or press Ctrl+C to exit the application.
