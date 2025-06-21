# PyTZ Buddy - Timezone Converter 🌍

A simple Python application that helps you find timezone information for any location and converts it to major timezones around the world.

## Features

### Core Features
- 🔍 **Location Lookup**: Enter any location (city, state, country) and get its timezone
- 🕐 **Time Conversion**: Automatically converts current time to major world timezones
- ⏰ **Specific Time Conversion**: Convert any specific time (not just current time)
- ⏱️ **Relative Time Display**: Shows "X hours ahead/behind" for easy comparison
- 🌍 **Timezone Shortcuts**: Quick access with shortcuts like 'nyc', 'london', 'tokyo'

### Advanced Features
- 🗓️ **Meeting Time Scheduler**: Find optimal meeting times across multiple timezones
- 🕐 **Business Hours Overlap**: Analyze working hours overlap between locations
- 📊 **Enhanced Search**: Smart suggestions when location isn't found
- 💾 **Export Results**: Save timezone conversions to TXT or JSON files
- ⚙️ **User Configuration**: Customizable business hours and timezone preferences

### User Experience
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

### Basic Location Lookup
Enter any location when prompted:
- `Duncan, Oklahoma`
- `Paris, France`
- `Tokyo, Japan`
- `New York, NY`

The app will show:
- The exact location found
- Local timezone information
- Current time in that timezone
- Converted times for major world timezones

### Advanced Commands

#### Time Conversion
Convert specific times across timezones:
```bash
convert 14:30 EST              # Convert 2:30 PM EST to all timezones
convert 9:00 AM PST 2025-07-04 # Convert with specific date
convert 15:45 UTC              # Convert UTC time
```

#### Meeting Planning
Find optimal meeting times for multiple locations:
```bash
meeting nyc london tokyo       # 3-way meeting planning
meeting New York London        # 2-way meeting planning
meeting EST PST CST            # Using timezone shortcuts
```

#### Business Hours Analysis
Analyze working hours overlap between locations:
```bash
overlap nyc london sydney      # Check business hours overlap
overlap EST PST                # US coast overlap analysis
overlap tokyo beijing singapore # Asia-Pacific overlap
```

#### Export & Configuration
```bash
export txt                     # Export last result as text file
export json                    # Export last result as JSON file
help                          # Show detailed command help
```

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

### Advanced Features

#### Meeting Time Scheduler
Perfect for coordinating across global teams:
- Finds optimal meeting times during business hours (9 AM - 5 PM local time)
- Supports multiple locations simultaneously
- Shows up to 7 days of meeting opportunities
- Visual indicators for time of day at each location

#### Business Hours Overlap Analysis
Analyze working hours compatibility:
- Calculate overlapping business hours between locations
- Customizable business hours (default 9 AM - 5 PM)
- Recommendations based on overlap duration
- Perfect for planning collaboration strategies

#### Export & Integration
Save and share your timezone analysis:
- Export results in TXT or JSON format
- Timestamped files for record keeping
- JSON format perfect for integration with other tools
- Automatic filename generation with timestamps

#### Enhanced Search
Smart location suggestions when searches fail:
- Suggests similar locations for typos
- Provides specific formatting examples
- Recommends timezone shortcuts
- Contextual help based on input patterns

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
  • 'convert [time] [timezone]' - Convert specific time (e.g., 'convert 14:30 EST')
  • 'meeting [location1] [location2] ...' - Find meeting times
  • 'overlap [location1] [location2] ...' - Business hours overlap
  • 'history' - View your recent searches
  • 'export [format]' - Export last result (txt/json)
  • 'help' - Show detailed command help
  • '1', '2', etc. - Repeat a search from history
  • 'quit', 'exit', or 'q' - Exit the program
  • Ctrl+C - Quick exit

Enter location (or command): convert 14:30 EST

🔄 Converting 14:30 from EST...

⏰ TIME CONVERSION: 14:30 EST (today)
======================================================================
⭐ US/Eastern           | 2025-06-21 14:30:00 EST (-0500) ☀️
   ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ | SOURCE TIME

  US/Central           | 2025-06-21 13:30:00 CST (-0600) ☀️
  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ | (1 hour behind)
  US/Mountain          | 2025-06-21 12:30:00 MST (-0700) ☀️
  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ | (2 hours behind)
  US/Pacific           | 2025-06-21 11:30:00 PST (-0800) 🌅
  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ | (3 hours behind)
  Europe/London        | 2025-06-21 19:30:00 GMT (+0000) 🌆
  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ | (5 hours ahead)
  Asia/Tokyo           | 2025-06-22 04:30:00 JST (+0900) 🌙
  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ | (14 hours ahead)
======================================================================

Enter location (or command): meeting nyc london tokyo

🗓️ Finding meeting times for: nyc, london, tokyo

🗓️ MEETING TIME SUGGESTIONS
======================================================================
📍 Locations: nyc, london, tokyo
⏰ Business Hours: 8:00 AM - 6:00 PM (local time)  
🔍 Found 3 optimal meeting times:

🕐 Option 1: Monday, 2025-06-23
--------------------------------------------------
  📍 nyc             | 08:00 EST 🌅
  📍 london          | 13:00 GMT ☀️  
  📍 tokyo           | 22:00 JST 🌙

🕐 Option 2: Monday, 2025-06-23
--------------------------------------------------
  📍 nyc             | 09:00 EST 🌅
  📍 london          | 14:00 GMT ☀️
  📍 tokyo           | 23:00 JST 🌙

💡 Tip: These times work within standard business hours for all locations!
======================================================================

Enter location (or command): overlap nyc london

🕐 Analyzing business hours overlap for: nyc, london

🕐 BUSINESS HOURS OVERLAP ANALYSIS
======================================================================
📍 Locations: nyc, london
⏰ Business Hours: 9:00-17:00 (local time)
✅ Overlap Found: 3 hours per day

🌍 OVERLAPPING BUSINESS HOURS:
--------------------------------------------------
UTC 14:00 - 15:00
  📍 nyc             | 09:00 EST ✅
  📍 london          | 14:00 GMT ✅

UTC 15:00 - 16:00  
  📍 nyc             | 10:00 EST ✅
  📍 london          | 15:00 GMT ✅

UTC 16:00 - 17:00
  📍 nyc             | 11:00 EST ✅
  📍 london           | 16:00 GMT ✅

💡 Recommendation: 👍 Good overlap! Schedule important meetings during these hours.
======================================================================

Enter location (or command): export json
✅ Results exported to: timezone_results_20250621_160530.json

Enter location (or command): help

📖 DETAILED COMMAND HELP
======================================================================
🌍 BASIC LOCATION LOOKUP:
  • Type any location: 'New York', 'Paris, France', 'Tokyo, Japan'
  • Use shortcuts: 'nyc', 'london', 'tokyo', 'chicago', 'la', etc.

⏰ TIME CONVERSION:
  • convert [time] [timezone] [date] - Convert specific time
    Examples:
      'convert 14:30 EST' - Convert 2:30 PM EST to all timezones
      'convert 9:00 AM PST 2025-07-04' - With specific date
      'convert 15:45 UTC' - Convert UTC time

🗓️ MEETING PLANNING:
  • meeting [location1] [location2] ... - Find optimal meeting times
    Examples:
      'meeting nyc london tokyo' - 3-way meeting
      'meeting New York London' - 2-way meeting

🕐 BUSINESS HOURS OVERLAP:
  • overlap [location1] [location2] ... - Analyze working hours overlap
    Examples:
      'overlap nyc london sydney' - Check overlap
      'overlap EST PST' - US coast overlap

📋 HISTORY & EXPORT:
  • history - Show recent searches
  • 1, 2, 3... - Repeat numbered search from history
  • export txt - Export last result as text file
  • export json - Export last result as JSON file

🎯 TIMEZONE SHORTCUTS:
  nyc/ny/east → US/Eastern    |  london/uk → Europe/London
  chicago/central → US/Central|  paris → Europe/Paris
  denver/mountain → US/Mountain| tokyo/japan → Asia/Tokyo
  la/west/pacific → US/Pacific|  sydney/australia → Australia/Sydney
  beijing/china → Asia/Shanghai| utc/gmt → UTC
======================================================================
💡 Tip: Commands are case-insensitive and flexible!

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
