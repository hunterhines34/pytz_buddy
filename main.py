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
    print("  • 'history' - View your recent searches")
    print("  • '1', '2', etc. - Repeat a search from history")
    print("  • 'quit', 'exit', or 'q' - Exit the program")
    print("  • Ctrl+C - Quick exit")
    print()
    
    # Initialize converter with integrated cache manager
    from cache_manager import CacheManager
    cache_manager = CacheManager()
    converter = TimezoneConverter(cache_manager)
    
    while True:
        try:
            location = input("Enter location (or command): ").strip()
            
            if location.lower() in ['quit', 'exit', 'q']:
                print("Thanks for using PyTZ Buddy! 🌍")
                break
            
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
                
            if not location:
                print("Please enter a valid location.\n")
                continue
                
            print("\nProcessing...")
            results = converter.process_location(location)
            
            if results:
                # Add to persistent history
                cache_manager.add_to_history(location)
                converter.display_results(results)
            else:
                print("❌ Could not find timezone information for that location.")
                print("Please try a different location or be more specific.\n")
                
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
