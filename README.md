# PyTZ Buddy - Timezone Converter 🌍

A simple Python application that helps you find timezone information for any location and converts it to major timezones around the world.

## Features

- 🔍 **Location Lookup**: Enter any location (city, state, country) and get its timezone
- 🕐 **Time Conversion**: Automatically converts current time to major world timezones
- ⏱️ **Relative Time Display**: Shows "X hours ahead/behind" for easy comparison
- 🌍 **Timezone Shortcuts**: Quick access with shortcuts like 'nyc', 'london', 'tokyo'
- 📝 **Search History**: Keep track of recent searches and quickly repeat them
- 🌅 **Day/Night Indicators**: Visual icons showing time of day for each timezone
- 💾 **Persistent History**: Search history saved across sessions with location caching
- ⚡ **Smart Caching**: Geocoding results cached for faster repeat searches
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

### Smart Caching & Performance

PyTZ Buddy includes intelligent caching to improve performance and user experience:

- **Persistent History**: Your search history is automatically saved and restored between sessions
- **Location Caching**: Geocoding results are cached for 30 days to speed up repeat searches
- **Cache Indicators**: See `📋 Found in cache:` when using cached location data
- **Automatic Cleanup**: Cache automatically manages size and removes expired entries

The cache is stored in `.pytz_cache/` directory and is automatically ignored by Git.

## Example Output

**Enhanced Interface with New Features:**

```
🌍 Welcome to PyTZ Buddy - Timezone Converter!
Enter a location to see its timezone and conversions to major world timezones.
Examples: 'Duncan, Oklahoma', 'Paris, France', 'Tokyo, Japan'
Shortcuts: 'nyc', 'london', 'tokyo', 'chicago', 'la', 'sydney', etc.

📋 Available Commands:
  • Enter any location name (city, state, country)
  • Use timezone shortcuts (nyc, london, tokyo, etc.)
  • 'history' - View your recent searches
  • '1', '2', etc. - Repeat a search from history
  • 'quit', 'exit', or 'q' - Exit the program
  • Ctrl+C - Quick exit

Enter location (or command): New York City, New York

Processing...
Looking up location: New York City, New York
Found: City of New York, New York, United States
Timezone: America/New_York

======================================================================
🌍 TIMEZONE INFORMATION
======================================================================
📍 Location: City of New York, New York, United States
📌 Coordinates: 40.7127, -74.0060
🕐 Local Timezone: America/New_York

⏰ CURRENT TIME CONVERSIONS:
----------------------------------------------------------------------
⭐ America/New_York     | 2025-06-21 10:15:30 EDT (-0400) 🌅
                        | LOCAL TIME

  US/Eastern           | 2025-06-21 10:15:30 EDT (-0400) 🌅
                       | (same time)
  US/Central           | 2025-06-21 09:15:30 CDT (-0500) 🌅
                       | (1 hour behind)
  US/Mountain          | 2025-06-21 08:15:30 MDT (-0600) 🌅
                       | (2 hours behind)
  US/Pacific           | 2025-06-21 07:15:30 PDT (-0700) 🌅
                       | (3 hours behind)
  Europe/London        | 2025-06-21 15:15:30 BST (+0100) ☀️
                       | (5 hours ahead)
  Europe/Paris         | 2025-06-21 16:15:30 CEST (+0200) ☀️
                       | (6 hours ahead)
  Asia/Tokyo           | 2025-06-21 23:15:30 JST (+0900) 🌙
                       | (13 hours ahead)
  Asia/Shanghai        | 2025-06-21 22:15:30 CST (+0800) 🌙
                       | (12 hours ahead)
  Australia/Sydney     | 2025-06-22 00:15:30 AEST (+1000) 🌙
                       | (14 hours ahead)
  UTC                  | 2025-06-21 14:15:30 UTC (+0000) ☀️
                       | (4 hours ahead)
======================================================================
💡 Tip: You can use shortcuts like 'nyc', 'london', 'tokyo' for quick timezone lookups!
======================================================================

------------------------------------------------------------
💡 Next: Enter another location, type 'history' for recent searches, or 'quit' to exit
------------------------------------------------------------

Enter location (or command): Tokyo, Japan

Processing...
Looking up location: Tokyo, Japan
Found: 東京都, 日本
Timezone: Asia/Tokyo

======================================================================
🌍 TIMEZONE INFORMATION
======================================================================
📍 Location: 東京都, 日本
📌 Coordinates: 35.6769, 139.7639
🕐 Local Timezone: Asia/Tokyo

⏰ CURRENT TIME CONVERSIONS:
----------------------------------------------------------------------
⭐ Asia/Tokyo           | 2025-06-21 23:15:45 JST (+0900) 🌙
                        | LOCAL TIME

  US/Eastern           | 2025-06-21 10:15:45 EDT (-0400) 🌅
                       | (13 hours behind)
  US/Central           | 2025-06-21 09:15:45 CDT (-0500) 🌅
                       | (14 hours behind)
  US/Mountain          | 2025-06-21 08:15:45 MDT (-0600) 🌅
                       | (15 hours behind)
  US/Pacific           | 2025-06-21 07:15:45 PDT (-0700) 🌅
                       | (16 hours behind)
  Europe/London        | 2025-06-21 15:15:45 BST (+0100) ☀️
                       | (8 hours behind)
  Europe/Paris         | 2025-06-21 16:15:45 CEST (+0200) ☀️
                       | (7 hours behind)
  Asia/Shanghai        | 2025-06-21 22:15:45 CST (+0800) 🌙
                       | (1 hour behind)
  Australia/Sydney     | 2025-06-22 01:15:45 AEST (+1000) 🌙
                       | (1 hour ahead)
  UTC                  | 2025-06-21 14:15:45 UTC (+0000) ☀️
                       | (9 hours behind)
======================================================================
💡 Tip: You can use shortcuts like 'nyc', 'london', 'tokyo' for quick timezone lookups!
======================================================================

------------------------------------------------------------
💡 Next: Enter another location, type 'history' for recent searches, or 'quit' to exit
------------------------------------------------------------

Enter location (or command): history

📝 Recent Searches:
----------------------------------------
1. New York City, New York
2. Tokyo, Japan

💡 Tip: Type a number (1-2) to repeat that search
Or enter a new location to search.

Enter location (or command): 1
🔄 Repeating search for: New York City, New York

Processing...
Looking up location: New York City, New York
Found: City of New York, New York, United States
Timezone: America/New_York

======================================================================
🌍 TIMEZONE INFORMATION
======================================================================
📍 Location: City of New York, New York, United States
📌 Coordinates: 40.7127, -74.0060
🕐 Local Timezone: America/New_York

⏰ CURRENT TIME CONVERSIONS:
----------------------------------------------------------------------
⭐ America/New_York     | 2025-06-21 10:16:12 EDT (-0400) 🌅
                        | LOCAL TIME

  US/Eastern           | 2025-06-21 10:16:12 EDT (-0400) 🌅
                       | (same time)
  [... other timezones shown ...]
======================================================================

Enter location (or command): quit
Thanks for using PyTZ Buddy! 🌍
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
