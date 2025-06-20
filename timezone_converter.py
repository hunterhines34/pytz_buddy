#!/usr/bin/env python3
"""
PyTZ Buddy - Timezone Converter
A simple application to find timezone information for any location
and convert it to other major timezones around the world.
"""

import pytz
from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import requests

class TimezoneConverter:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="pytz_buddy")
        self.tf = TimezoneFinder()
        
        # Major timezones to display
        self.major_timezones = [
            'US/Eastern',
            'US/Central', 
            'US/Mountain',
            'US/Pacific',
            'Europe/London',
            'Europe/Paris',
            'Asia/Tokyo',
            'Asia/Shanghai',
            'Australia/Sydney',
            'UTC'
        ]
    
    def get_location_info(self, location_name):
        """Get coordinates and address for a location"""
        try:
            location = self.geolocator.geocode(location_name)
            if location:
                return {
                    'address': location.address,
                    'latitude': location.latitude,
                    'longitude': location.longitude
                }
            else:
                return None
        except Exception as e:
            print(f"Error geocoding location: {e}")
            return None
    
    def get_timezone_for_coordinates(self, lat, lng):
        """Get timezone for given coordinates"""
        try:
            timezone_str = self.tf.timezone_at(lat=lat, lng=lng)
            return timezone_str
        except Exception as e:
            print(f"Error finding timezone: {e}")
            return None
    
    def convert_to_timezones(self, source_timezone_str, dt=None):
        """Convert current time to multiple timezones"""
        if dt is None:
            dt = datetime.now()
            
        try:
            source_tz = pytz.timezone(source_timezone_str)
            # Localize the datetime to source timezone
            localized_dt = source_tz.localize(dt)
            
            conversions = {}
            conversions[source_timezone_str] = {
                'time': localized_dt.strftime('%Y-%m-%d %H:%M:%S %Z'),
                'is_source': True
            }
            
            for tz_name in self.major_timezones:
                if tz_name != source_timezone_str:
                    target_tz = pytz.timezone(tz_name)
                    converted_time = localized_dt.astimezone(target_tz)
                    conversions[tz_name] = {
                        'time': converted_time.strftime('%Y-%m-%d %H:%M:%S %Z'),
                        'is_source': False
                    }
            
            return conversions
        except Exception as e:
            print(f"Error converting timezones: {e}")
            return None
    
    def process_location(self, location_name):
        """Main method to process a location and return timezone info"""
        print(f"Looking up location: {location_name}")
        
        # Get location coordinates
        location_info = self.get_location_info(location_name)
        if not location_info:
            return None
            
        print(f"Found: {location_info['address']}")
        
        # Get timezone for coordinates
        timezone_str = self.get_timezone_for_coordinates(
            location_info['latitude'], 
            location_info['longitude']
        )
        
        if not timezone_str:
            return None
            
        print(f"Timezone: {timezone_str}")
        
        # Get current time conversions
        conversions = self.convert_to_timezones(timezone_str)
        
        return {
            'location_info': location_info,
            'timezone': timezone_str,
            'conversions': conversions
        }
    
    def display_results(self, results):
        """Display the timezone conversion results in a formatted way"""
        if not results:
            print("No results to display")
            return
            
        print("\n" + "="*60)
        print(f"TIMEZONE INFORMATION")
        print("="*60)
        print(f"Location: {results['location_info']['address']}")
        print(f"Coordinates: {results['location_info']['latitude']:.4f}, {results['location_info']['longitude']:.4f}")
        print(f"Local Timezone: {results['timezone']}")
        
        print(f"\nCURRENT TIME CONVERSIONS:")
        print("-"*60)
        
        # Display source timezone first
        for tz_name, time_info in results['conversions'].items():
            if time_info['is_source']:
                print(f"★ {tz_name:20} | {time_info['time']} (LOCAL)")
                break
        
        print()
        # Display other timezones
        for tz_name, time_info in results['conversions'].items():
            if not time_info['is_source']:
                print(f"  {tz_name:20} | {time_info['time']}")
        
        print("="*60)
