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
            
            # Popular timezone shortcuts for quick access
            self.timezone_shortcuts = {
                'nyc': 'US/Eastern',
                'ny': 'US/Eastern',
                'east': 'US/Eastern',
                'chicago': 'US/Central',
                'central': 'US/Central',
                'denver': 'US/Mountain',
                'mountain': 'US/Mountain',
                'la': 'US/Pacific',
                'west': 'US/Pacific',
                'pacific': 'US/Pacific',
                'london': 'Europe/London',
                'uk': 'Europe/London',
                'paris': 'Europe/Paris',
                'tokyo': 'Asia/Tokyo',
                'japan': 'Asia/Tokyo',
                'beijing': 'Asia/Shanghai',
                'china': 'Asia/Shanghai',
                'sydney': 'Australia/Sydney',
                'australia': 'Australia/Sydney',
                'utc': 'UTC',
                'gmt': 'UTC'
            }
    
    def resolve_timezone_shortcut(self, input_tz):
        """Resolve timezone shortcuts to full timezone names"""
        if input_tz.lower() in self.timezone_shortcuts:
            return self.timezone_shortcuts[input_tz.lower()]
        return input_tz
    
    def calculate_time_difference(self, source_dt, target_dt):
        """Calculate relative time difference between two timezone-aware datetimes"""
        diff_seconds = (target_dt.utcoffset() - source_dt.utcoffset()).total_seconds()
        diff_hours = int(diff_seconds / 3600)
        
        if diff_hours == 0:
            return "same time"
        elif diff_hours > 0:
            return f"{diff_hours} hour{'s' if abs(diff_hours) != 1 else ''} ahead"
        else:
            return f"{abs(diff_hours)} hour{'s' if abs(diff_hours) != 1 else ''} behind"
    
    def process_timezone_shortcut(self, shortcut):
        """Process a timezone shortcut directly without location lookup"""
        print(f"Using timezone shortcut: {shortcut} → {self.timezone_shortcuts[shortcut.lower()]}")
        
        timezone_str = self.timezone_shortcuts[shortcut.lower()]
        
        # Get current time conversions
        conversions = self.convert_to_timezones(timezone_str)
        
        return {
            'location_info': {
                'address': f"Timezone: {timezone_str}",
                'latitude': 0.0,
                'longitude': 0.0
            },
            'timezone': timezone_str,
            'conversions': conversions
        }    
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
        """Convert current time to multiple timezones with relative differences"""
        if dt is None:
            dt = datetime.now()
            
        try:
            # Resolve any shortcuts
            source_timezone_str = self.resolve_timezone_shortcut(source_timezone_str)
            
            source_tz = pytz.timezone(source_timezone_str)
            # Localize the datetime to source timezone
            localized_dt = source_tz.localize(dt)
            
            conversions = {}
            conversions[source_timezone_str] = {
                'time': localized_dt.strftime('%Y-%m-%d %H:%M:%S %Z'),
                'utc_offset': localized_dt.strftime('%z'),
                'is_source': True,
                'relative_diff': 'local time',
                'datetime_obj': localized_dt
            }
            
            for tz_name in self.major_timezones:
                if tz_name != source_timezone_str:
                    target_tz = pytz.timezone(tz_name)
                    converted_time = localized_dt.astimezone(target_tz)
                    relative_diff = self.calculate_time_difference(localized_dt, converted_time)
                    
                    conversions[tz_name] = {
                        'time': converted_time.strftime('%Y-%m-%d %H:%M:%S %Z'),
                        'utc_offset': converted_time.strftime('%z'),
                        'is_source': False,
                        'relative_diff': relative_diff,
                        'datetime_obj': converted_time
                    }
            
            return conversions
        except Exception as e:
            print(f"Error converting timezones: {e}")
            return None

    
    def process_location(self, location_name):
        """Main method to process a location and return timezone info"""
        
        # Check if it's a timezone shortcut first
        if location_name.lower() in self.timezone_shortcuts:
            return self.process_timezone_shortcut(location_name)
        
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
        """Display the timezone conversion results in a formatted way with enhancements"""
        if not results:
            print("No results to display")
            return
            
        print("\n" + "="*70)
        print(f"🌍 TIMEZONE INFORMATION")
        print("="*70)
        print(f"📍 Location: {results['location_info']['address']}")
        print(f"📌 Coordinates: {results['location_info']['latitude']:.4f}, {results['location_info']['longitude']:.4f}")
        print(f"🕐 Local Timezone: {results['timezone']}")
        
        print(f"\n⏰ CURRENT TIME CONVERSIONS:")
        print("-"*70)
        
        # Display source timezone first
        for tz_name, time_info in results['conversions'].items():
            if time_info['is_source']:
                dt_obj = time_info['datetime_obj']
                day_indicator = "🌅" if 6 <= dt_obj.hour < 12 else "☀️" if 12 <= dt_obj.hour < 18 else "🌆" if 18 <= dt_obj.hour < 22 else "🌙"
                print(f"⭐ {tz_name:20} | {time_info['time']} ({time_info['utc_offset']}) {day_indicator}")
                print(f"   {'':20} | LOCAL TIME")
                break
        
        print()
        # Display other timezones with relative differences - improved alignment
        for tz_name, time_info in results['conversions'].items():
            if not time_info['is_source']:
                dt_obj = time_info['datetime_obj']
                day_indicator = "🌅" if 6 <= dt_obj.hour < 12 else "☀️" if 12 <= dt_obj.hour < 18 else "🌆" if 18 <= dt_obj.hour < 22 else "🌙"
                print(f"  {tz_name:20} | {time_info['time']} ({time_info['utc_offset']}) {day_indicator}")
                print(f"  {'':20} | ({time_info['relative_diff']})")
        
        print("="*70)
        print("💡 Tip: You can use shortcuts like 'nyc', 'london', 'tokyo' for quick timezone lookups!")
        print("="*70)


