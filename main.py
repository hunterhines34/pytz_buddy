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
    print("Type 'quit' to exit.\n")
    
    converter = TimezoneConverter()
    
    while True:
        try:
            location = input("Enter location: ").strip()
            
            if location.lower() in ['quit', 'exit', 'q']:
                print("Thanks for using PyTZ Buddy! 🌍")
                break
                
            if not location:
                print("Please enter a valid location.\n")
                continue
                
            print("\nProcessing...")
            results = converter.process_location(location)
            
            if results:
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
