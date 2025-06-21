# PyTZ Buddy - Timezone Converter 🌍

A simple Python application that helps you find timezone information for any location and converts it to major timezones around the world.

## Features

- 🔍 **Location Lookup**: Enter any location (city, state, country) and get its timezone
- 🕐 **Time Conversion**: Automatically converts current time to major world timezones
- ⏱️ **Relative Time Display**: Shows "X hours ahead/behind" for easy comparison
- 🌍 **Timezone Shortcuts**: Quick access with shortcuts like 'nyc', 'london', 'tokyo'
- 📝 **Search History**: Keep track of recent searches and quickly repeat them
- 🌅 **Day/Night Indicators**: Visual icons showing time of day for each timezone
- 🆓 **Free APIs**: Uses only free services (OpenStreetMap Nominatim for geocoding)
- 🎯 **Enhanced Interface**: Clean, informative command-line interface

## Real-World Use Cases

**Business Applications:**
* **Meeting Schedulers**: Auto-suggest meeting times across global teams
* **Travel Apps**: Show arrival times in local timezones
* **E-commerce**: Display delivery windows in customer's timezone
* **Event Management**: Multi-timezone event coordination
* **Remote Work Tools**: Team availability across timezones

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

### History Commands

- Type `history` to see your recent searches (up to 10)
- Type a number (e.g., `1`, `2`) to repeat a previous search
- Recent searches are automatically saved when successful

### Timezone Shortcuts

For quick timezone lookups, you can use these shortcuts instead of searching for cities:

| Shortcut | Timezone | Region |
|----------|----------|---------|
| `nyc`, `ny`, `east` | US/Eastern | New York, Eastern US |
| `chicago`, `central` | US/Central | Chicago, Central US |
| `denver`, `mountain` | US/Mountain | Denver, Mountain US |
| `la`, `west`, `pacific` | US/Pacific | Los Angeles, Pacific US |
| `london`, `uk` | Europe/London | London, UK |
| `paris` | Europe/Paris | Paris, France |
| `tokyo`, `japan` | Asia/Tokyo | Tokyo, Japan |
| `beijing`, `china` | Asia/Shanghai | Beijing, China |
| `sydney`, `australia` | Australia/Sydney | Sydney, Australia |
| `utc`, `gmt` | UTC | Coordinated Universal Time |

Example: Type `nyc` instead of searching for "New York, NY"

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
