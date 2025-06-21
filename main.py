#!/usr/bin/env python3
"""
PyTZ Buddy - Main Entry Point
A simple timezone converter application

Usage:
    python main.py
    
Then enter a location when prompted (e.g., "Duncan, Oklahoma")
"""

from timezone_converter import TimezoneConverter

def main():
    print("\n")
    print("🌍 Welcome to PyTZ Buddy - Timezone Converter!")
    print("Enter a location to see its timezone and conversions to major world timezones.")
    print("Examples: 'Duncan, Oklahoma', 'Paris, France', 'Tokyo, Japan'")
    print("Shortcuts: 'nyc', 'london', 'tokyo', 'chicago', 'la', 'sydney', etc.")
    print()
    print("📋 Available Commands:")
    print("  • Enter any location name (city, state, country)")
    print("  • Use timezone shortcuts (nyc, london, tokyo, etc.)")
    print("  • 'convert [time] [timezone]' - Convert specific time (e.g., 'convert 14:30 EST')")
    print("  • 'meeting [location1] [location2] ...' - Find meeting times")
    print("  • 'overlap [location1] [location2] ...' - Business hours overlap")
    print("  • 'history' - View your recent searches")
    print("  • 'export [format]' - Export last result (txt/json)")
    print("  • 'help' - Show detailed command help")
    print("  • '1', '2', etc. - Repeat a search from history")
    print("  • 'quit', 'exit', or 'q' - Exit the program")
    print("  • Ctrl+C - Quick exit")
    print()
    
    # Initialize converter with integrated cache manager
    from cache_manager import CacheManager
    cache_manager = CacheManager()
    converter = TimezoneConverter(cache_manager)
    
    # Store last results for export functionality
    last_results = None
    
    while True:
        try:
            location = input("Enter location (or command): ").strip()
            
            if location.lower() in ['quit', 'exit', 'q']:
                print("Thanks for using PyTZ Buddy! 🌍")
                break
            
            # Handle help command
            if location.lower() == 'help':
                print("\n📖 DETAILED COMMAND HELP")
                print("="*70)
                print("🌍 BASIC LOCATION LOOKUP:")
                print("  • Type any location: 'New York', 'Paris, France', 'Tokyo, Japan'")
                print("  • Use shortcuts: 'nyc', 'london', 'tokyo', 'chicago', 'la', etc.")
                print()
                print("⏰ TIME CONVERSION:")
                print("  • convert [time] [timezone] [date] - Convert specific time")
                print("    Examples:")
                print("      'convert 14:30 EST' - Convert 2:30 PM EST to all timezones")
                print("      'convert 9:00 AM PST 2025-07-04' - With specific date")
                print("      'convert 15:45 UTC' - Convert UTC time")
                print()
                print("🗓️ MEETING PLANNING:")
                print("  • meeting [location1] [location2] ... - Find optimal meeting times")
                print("    Examples:")
                print("      'meeting nyc london tokyo' - 3-way meeting")
                print("      'meeting New York London' - 2-way meeting")
                print()
                print("🕐 BUSINESS HOURS OVERLAP:")
                print("  • overlap [location1] [location2] ... - Analyze working hours overlap")
                print("    Examples:")
                print("      'overlap nyc london sydney' - Check overlap")
                print("      'overlap EST PST' - US coast overlap")
                print()
                print("📋 HISTORY & EXPORT:")
                print("  • history - Show recent searches")
                print("  • 1, 2, 3... - Repeat numbered search from history")
                print("  • export txt - Export last result as text file")
                print("  • export json - Export last result as JSON file")
                print()
                print("🎯 TIMEZONE SHORTCUTS:")
                print("  nyc/ny/east → US/Eastern    |  london/uk → Europe/London")
                print("  chicago/central → US/Central|  paris → Europe/Paris")
                print("  denver/mountain → US/Mountain| tokyo/japan → Asia/Tokyo")
                print("  la/west/pacific → US/Pacific|  sydney/australia → Australia/Sydney")
                print("  beijing/china → Asia/Shanghai| utc/gmt → UTC")
                print("="*70)
                print("💡 Tip: Commands are case-insensitive and flexible!")
                print()
                continue
            
            # Handle history command
            if location.lower() == 'history':
                search_history = cache_manager.get_search_history()
                if not search_history:
                    print("📝 No search history yet. Try searching for a location first!\n")
                    continue
                
                print("\n📝 Recent Searches:")
                print("-" * 40)
                for i, hist_location in enumerate(search_history, 1):
                    print(f"{i}. {hist_location}")
                print(f"\n💡 Tip: Type a number (1-{len(search_history)}) to repeat that search")
                print("Or enter a new location to search.\n")
                continue
            
            # Handle export command
            if location.lower().startswith('export'):
                if not last_results:
                    print("❌ No recent results to export. Search for a location first!")
                    print()
                    continue
                
                parts = location.split()
                export_format = 'txt'
                if len(parts) > 1:
                    export_format = parts[1].lower()
                    if export_format not in ['txt', 'json']:
                        print("❌ Supported formats: txt, json")
                        print()
                        continue
                
                success, result = converter.export_results(last_results, export_format)
                if success:
                    print(f"✅ Results exported to: {result}")
                else:
                    print(f"❌ Export failed: {result}")
                print()
                continue
                
                print("\n📝 Recent Searches:")
                print("-" * 40)
                for i, hist_location in enumerate(search_history, 1):
                    print(f"{i}. {hist_location}")
                print(f"\n💡 Tip: Type a number (1-{len(search_history)}) to repeat that search")
                print("Or enter a new location to search.\n")
                continue
            
            # Handle history number selection
            if location.isdigit():
                search_history = cache_manager.get_search_history()
                index = int(location) - 1
                if 0 <= index < len(search_history):
                    location = search_history[index]
                    print(f"🔄 Repeating search for: {location}")
                else:
                    print("❌ Invalid history number. Use 'history' to see available options.\n")
                    continue
            
            # Handle convert command
            if location.lower().startswith('convert '):
                parts = location.split(' ', 2)
                if len(parts) >= 3:
                    time_str = parts[1]
                    timezone_str = parts[2]
                    date_str = None
                    
                    # Check if there's a date part
                    if len(parts) == 4:
                        date_str = parts[3]
                    
                    print(f"\n🔄 Converting {time_str} from {timezone_str}...")
                    conversions, error = converter.convert_specific_time(time_str, timezone_str, date_str)
                    
                    if error:
                        print(f"❌ {error}")
                    elif conversions:
                        converter.display_specific_time_results(conversions, time_str, timezone_str, date_str)
                    else:
                        print("❌ Could not convert the specified time")
                else:
                    print("❌ Usage: convert [time] [timezone] [optional: date]")
                    print("   Examples: 'convert 14:30 EST', 'convert 2:30 PM PST 2025-06-25'")
                print("\n" + "-"*60)
                print("💡 Next: Enter another command or 'quit' to exit")
                print("-"*60 + "\n")
                continue
            
            # Handle meeting command
            if location.lower().startswith('meeting '):
                locations = location.split()[1:]  # Remove 'meeting' from the list
                if len(locations) >= 2:
                    print(f"\n🗓️ Finding meeting times for: {', '.join(locations)}")
                    suggestions = converter.find_meeting_times(locations)
                    converter.display_meeting_suggestions(suggestions, locations)
                else:
                    print("❌ Need at least 2 locations for meeting planning")
                    print("   Example: 'meeting nyc london tokyo'")
                print("\n" + "-"*60)
                print("💡 Next: Enter another command or 'quit' to exit")
                print("-"*60 + "\n")
                continue
            
            # Handle overlap command
            if location.lower().startswith('overlap '):
                locations = location.split()[1:]  # Remove 'overlap' from the list
                if len(locations) >= 2:
                    print(f"\n🕐 Analyzing business hours overlap for: {', '.join(locations)}")
                    overlap_data = converter.calculate_business_hours_overlap(locations)
                    converter.display_business_hours_overlap(overlap_data, locations)
                else:
                    print("❌ Need at least 2 locations for overlap analysis")
                    print("   Example: 'overlap nyc london tokyo'")
                print("\n" + "-"*60)
                print("💡 Next: Enter another command or 'quit' to exit")
                print("-"*60 + "\n")
                continue
                
            if not location:
                print("Please enter a valid location.\n")
                continue
                
            print("\nProcessing...")
            results, error_msg = converter.enhanced_location_lookup(location)
            
            if results:
                # Store results for export functionality
                last_results = results
                # Add to persistent history
                cache_manager.add_to_history(location)
                converter.display_results(results)
            else:
                print(f"❌ {error_msg}")
                print()
                
            # Show helpful commands after each search
            print("\n" + "-"*60)
            print("💡 Next: Enter another location, type 'history' for recent searches, or 'quit' to exit")
            print("-"*60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\nThanks for using PyTZ Buddy! 🌍")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            print("Please try again.\n")




if __name__ == "__main__":
    main()
