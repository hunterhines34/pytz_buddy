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
    print("Commands: 'history' to see recent searches, 'quit' to exit.\n")
    
    converter = TimezoneConverter()
    search_history = []  # Store recent searches
    
    while True:
        try:
            location = input("Enter location (or command): ").strip()
            
            if location.lower() in ['quit', 'exit', 'q']:
                print("Thanks for using PyTZ Buddy! 🌍")
                break
            
            # Handle history command
            if location.lower() == 'history':
                if not search_history:
                    print("📝 No search history yet. Try searching for a location first!\n")
                    continue
                
                print("\n📝 Recent Searches:")
                print("-" * 40)
                for i, hist_location in enumerate(search_history, 1):
                    print(f"{i}. {hist_location}")
                print("\nTo repeat a search, enter its number (e.g., '1')")
                print("Or enter a new location to search.\n")
                continue
            
            # Handle history number selection
            if location.isdigit():
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
                # Add to history if successful and not already the most recent
                if not search_history or search_history[-1] != location:
                    search_history.append(location)
                    # Keep only last 10 searches
                    if len(search_history) > 10:
                        search_history.pop(0)
                
                converter.display_results(results)
            else:
                print("❌ Could not find timezone information for that location.")
                print("Please try a different location or be more specific.\n")
                
            print("\n" + "-"*60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\nThanks for using PyTZ Buddy! 🌍")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            print("Please try again.\n")


if __name__ == "__main__":
    main()
