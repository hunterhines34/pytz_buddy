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
    def __init__(self, cache_manager=None):
            self.geolocator = Nominatim(user_agent="pytz_buddy")
            self.tf = TimezoneFinder()
            
            # Import and initialize cache manager
            if cache_manager is None:
                from cache_manager import CacheManager
                self.cache_manager = CacheManager()
            else:
                self.cache_manager = cache_manager
            
            # Load user configuration and use preferred timezones
            user_config = self.cache_manager.get_user_config()
            self.major_timezones = user_config.get('preferred_timezones', [
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
            ])
            
            # Store user config for use in other methods
            self.user_config = user_config
            
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
    
    def find_meeting_times(self, locations, start_hour=None, end_hour=None, duration_hours=1):
        """Find optimal meeting times across multiple locations during business hours"""
        # Use user configuration for business hours if not specified
        if start_hour is None or end_hour is None:
            business_hours = self.user_config.get('business_hours', {'start': 8, 'end': 18})
            start_hour = business_hours.get('start', 8)
            end_hour = business_hours.get('end', 18)
            
        if len(locations) < 2:
            return None
            
        # Process all locations to get timezone info
        location_timezones = []
        for location in locations:
            if location.lower() in self.timezone_shortcuts:
                tz_str = self.timezone_shortcuts[location.lower()]
                location_data = {
                    'input': location,
                    'address': f"Timezone: {tz_str}",
                    'timezone': tz_str
                }
            else:
                location_info = self.get_location_info(location)
                if not location_info:
                    continue
                timezone_str = self.get_timezone_for_coordinates(
                    location_info['latitude'], 
                    location_info['longitude']
                )
                if not timezone_str:
                    continue
                location_data = {
                    'input': location,
                    'address': location_info['address'],
                    'timezone': timezone_str
                }
            location_timezones.append(location_data)
        
        if len(location_timezones) < 2:
            return None
            
        # Find overlapping business hours
        meeting_suggestions = []
        
        # Check next 7 days for meeting opportunities
        from datetime import datetime, timedelta
        today = datetime.now().date()
        
        for day_offset in range(7):
            check_date = today + timedelta(days=day_offset)
            
            # For each hour in the day, check if it's business hours for all locations
            for hour in range(24):
                meeting_time = datetime.combine(check_date, datetime.min.time().replace(hour=hour))
                
                valid_for_all = True
                time_details = []
                
                for location_data in location_timezones:
                    try:
                        tz = pytz.timezone(location_data['timezone'])
                        # Convert meeting time to this timezone
                        utc_time = pytz.utc.localize(meeting_time)
                        local_time = utc_time.astimezone(tz)
                        
                        # Check if it's within business hours
                        if not (start_hour <= local_time.hour < end_hour):
                            valid_for_all = False
                            break
                            
                        time_details.append({
                            'location': location_data['input'],
                            'address': location_data['address'],
                            'local_time': local_time,
                            'timezone': location_data['timezone']
                        })
                    except Exception:
                        valid_for_all = False
                        break
                
                if valid_for_all and len(time_details) == len(location_timezones):
                    meeting_suggestions.append({
                        'utc_time': meeting_time,
                        'locations': time_details
                    })
        
        return meeting_suggestions[:10]  # Return top 10 suggestions
  # Return top 10 suggestions
        
    def display_meeting_suggestions(self, suggestions, locations):
            """Display meeting time suggestions in a formatted way"""
            if not suggestions:
                print("❌ No suitable meeting times found during business hours")
                print("   Try adjusting the business hours or timezone requirements")
                return
                
            print(f"\n🗓️ MEETING TIME SUGGESTIONS")
            print("="*70)
            print(f"📍 Locations: {', '.join(locations)}")
            print(f"⏰ Business Hours: 8:00 AM - 6:00 PM (local time)")
            print(f"🔍 Found {len(suggestions)} optimal meeting times:")
            print()
            
            for i, suggestion in enumerate(suggestions, 1):
                utc_time = suggestion['utc_time']
                day_name = utc_time.strftime('%A')
                date_str = utc_time.strftime('%Y-%m-%d')
                
                print(f"🕐 Option {i}: {day_name}, {date_str}")
                print("-" * 50)
                
                for location_info in suggestion['locations']:
                    local_time = location_info['local_time']
                    time_str = local_time.strftime('%H:%M %Z')
                    # Add day indicator
                    day_indicator = "🌅" if 6 <= local_time.hour < 12 else "☀️" if 12 <= local_time.hour < 18 else "🌆" if 18 <= local_time.hour < 22 else "🌙"
                    
                    print(f"  📍 {location_info['location']:15} | {time_str} {day_indicator}")
                    
                print()
            
            print("💡 Tip: These times work within standard business hours for all locations!")
            print("="*70)
        
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
        """Get coordinates and address for a location with caching"""
        # Try to get from cache first
        cached_result = self.cache_manager.get_cached_location(location_name)
        if cached_result:
            print(f"📋 Found in cache: {cached_result['address']}")
            return cached_result
        
        # Not in cache, perform geocoding
        try:
            location = self.geolocator.geocode(location_name)
            if location:
                location_data = {
                    'address': location.address,
                    'latitude': location.latitude,
                    'longitude': location.longitude
                }
                # Cache the result for future use
                self.cache_manager.cache_location(location_name, location_data)
                return location_data
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
    
    def convert_specific_time(self, time_str, source_timezone_str, date_str=None):
            """Convert a specific time from source timezone to all major timezones"""
            try:
                from datetime import datetime
                
                # Parse time string (supports formats like "14:30", "2:30 PM", "14:30:00")
                time_formats = [
                    '%H:%M',
                    '%H:%M:%S', 
                    '%I:%M %p',
                    '%I:%M:%S %p'
                ]
                
                parsed_time = None
                for fmt in time_formats:
                    try:
                        parsed_time = datetime.strptime(time_str, fmt).time()
                        break
                    except ValueError:
                        continue
                
                if not parsed_time:
                    return None, "Invalid time format. Use formats like '14:30', '2:30 PM', or '14:30:00'"
                
                # Parse date if provided, otherwise use today
                if date_str:
                    date_formats = ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%m-%d-%Y']
                    parsed_date = None
                    for fmt in date_formats:
                        try:
                            parsed_date = datetime.strptime(date_str, fmt).date()
                            break
                        except ValueError:
                            continue
                    if not parsed_date:
                        return None, "Invalid date format. Use formats like '2025-06-21', '06/21/2025', or '21/06/2025'"
                else:
                    parsed_date = datetime.now().date()
                
                # Combine date and time
                dt = datetime.combine(parsed_date, parsed_time)
                
                # Convert using existing method
                conversions = self.convert_to_timezones(source_timezone_str, dt)
                
                return conversions, None
                
            except Exception as e:
                return None, f"Error converting time: {str(e)}"
        
    def display_specific_time_results(self, conversions, original_time, original_timezone, date_str=None):
            """Display specific time conversion results"""
            if not conversions:
                return
                
            date_info = f" on {date_str}" if date_str else " (today)"
            print(f"\n⏰ TIME CONVERSION: {original_time} {original_timezone}{date_info}")
            print("="*70)
            
            # Display source timezone first
            for tz_name, time_info in conversions.items():
                if time_info['is_source']:
                    dt_obj = time_info['datetime_obj']
                    day_indicator = "🌅" if 6 <= dt_obj.hour < 12 else "☀️" if 12 <= dt_obj.hour < 18 else "🌆" if 18 <= dt_obj.hour < 22 else "🌙"
                    print(f"⭐ {tz_name:20} | {time_info['time']} ({time_info['utc_offset']}) {day_indicator}")
                    print(f"   {'':20} | SOURCE TIME")
                    break
            
            print()
            # Display other timezones
            for tz_name, time_info in conversions.items():
                if not time_info['is_source']:
                    dt_obj = time_info['datetime_obj']
                    day_indicator = "🌅" if 6 <= dt_obj.hour < 12 else "☀️" if 12 <= dt_obj.hour < 18 else "🌆" if 18 <= dt_obj.hour < 22 else "🌙"
                    print(f"  {tz_name:20} | {time_info['time']} ({time_info['utc_offset']}) {day_indicator}")
                    print(f"  {'':20} | ({time_info['relative_diff']})")
            
            print("="*70)
        
    def calculate_business_hours_overlap(self, locations, start_hour=None, end_hour=None):
        """Calculate overlapping business hours between multiple locations"""
        # Use user configuration for business hours if not specified
        if start_hour is None or end_hour is None:
            business_hours = self.user_config.get('business_hours', {'start': 9, 'end': 17})
            start_hour = business_hours.get('start', 9)
            end_hour = business_hours.get('end', 17)
            
        if len(locations) < 2:
            return None
            
        # Get timezone info for all locations
        location_timezones = []
        for location in locations:
            if location.lower() in self.timezone_shortcuts:
                tz_str = self.timezone_shortcuts[location.lower()]
                location_data = {
                    'input': location,
                    'address': f"Timezone: {tz_str}",
                    'timezone': tz_str
                }
            else:
                location_info = self.get_location_info(location)
                if not location_info:
                    continue
                timezone_str = self.get_timezone_for_coordinates(
                    location_info['latitude'], 
                    location_info['longitude']
                )
                if not timezone_str:
                    continue
                location_data = {
                    'input': location,
                    'address': location_info['address'],
                    'timezone': timezone_str
                }
            location_timezones.append(location_data)
        
        if len(location_timezones) < 2:
            return None
            
        # Calculate overlap for each hour of the day
        overlap_hours = []
        
        from datetime import datetime, time
        now = datetime.now()
        
        for hour in range(24):
            all_in_business_hours = True
            hour_details = []
            
            for location_data in location_timezones:
                try:
                    # Create a datetime for this hour in UTC
                    utc_dt = datetime.combine(now.date(), time(hour=hour))
                    utc_dt = pytz.utc.localize(utc_dt)
                    
                    # Convert to local timezone
                    local_tz = pytz.timezone(location_data['timezone'])
                    local_dt = utc_dt.astimezone(local_tz)
                    
                    # Check if within business hours
                    is_business_hour = start_hour <= local_dt.hour < end_hour
                    
                    hour_details.append({
                        'location': location_data['input'],
                        'timezone': location_data['timezone'],
                        'local_hour': local_dt.hour,
                        'is_business': is_business_hour,
                        'local_time': local_dt.strftime('%H:%M %Z')
                    })
                    
                    if not is_business_hour:
                        all_in_business_hours = False
                        
                except Exception:
                    all_in_business_hours = False
                    break
            
            if all_in_business_hours and len(hour_details) == len(location_timezones):
                overlap_hours.append({
                    'utc_hour': hour,
                    'locations': hour_details
                })
        
        return {
            'overlap_hours': overlap_hours,
            'total_overlap': len(overlap_hours),
            'business_hours': f"{start_hour}:00-{end_hour}:00",
            'locations': location_timezones
        }
    
    def display_business_hours_overlap(self, overlap_data, locations):
                """Display business hours overlap analysis"""
                if not overlap_data or not overlap_data['overlap_hours']:
                    print("\n❌ NO BUSINESS HOURS OVERLAP")
                    print("="*70)
                    print(f"📍 Locations: {', '.join(locations)}")
                    print(f"⏰ Business Hours: {overlap_data['business_hours'] if overlap_data else '9:00-17:00'} (local time)")
                    print("💡 Try adjusting business hours or consider asynchronous communication")
                    return
                    
                print(f"\n🕐 BUSINESS HOURS OVERLAP ANALYSIS")
                print("="*70)
                print(f"📍 Locations: {', '.join(locations)}")
                print(f"⏰ Business Hours: {overlap_data['business_hours']} (local time)")
                print(f"✅ Overlap Found: {overlap_data['total_overlap']} hours per day")
                print()
                
                if overlap_data['total_overlap'] > 0:
                    print("🌍 OVERLAPPING BUSINESS HOURS:")
                    print("-" * 50)
                    
                    for overlap in overlap_data['overlap_hours']:
                        utc_hour = overlap['utc_hour']
                        print(f"UTC {utc_hour:02d}:00 - {utc_hour+1:02d}:00")
                        
                        for location_info in overlap['locations']:
                            business_indicator = "✅" if location_info['is_business'] else "❌"
                            print(f"  📍 {location_info['location']:15} | {location_info['local_time']} {business_indicator}")
                        print()
                
                # Provide recommendations
                total_hours = overlap_data['total_overlap']
                if total_hours >= 6:
                    recommendation = "🎯 Excellent overlap! Great for real-time collaboration."
                elif total_hours >= 3:
                    recommendation = "👍 Good overlap! Schedule important meetings during these hours."
                elif total_hours >= 1:
                    recommendation = "⚠️ Limited overlap. Consider flexible meeting times."
                else:
                    recommendation = "🔄 No overlap. Async communication recommended."
                
                print(f"💡 Recommendation: {recommendation}")
                print("="*70)
            
    def export_results(self, results, export_format=None, filename=None):
        """Export timezone conversion results to file"""
        if not results:
            return False, "No results to export"
            
        # Use user configuration for default export format if not specified
        if export_format is None:
            export_format = self.user_config.get('export_format', 'txt')
            
        try:
            import json
            from datetime import datetime
            
            if not filename:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"timezone_results_{timestamp}.{export_format}"
            
            if export_format.lower() == 'json':
                # Convert datetime objects to strings for JSON serialization
                export_data = {
                    'location_info': results['location_info'],
                    'timezone': results['timezone'],
                    'conversions': {},
                    'exported_at': datetime.now().isoformat()
                }
                
                for tz_name, time_info in results['conversions'].items():
                    export_data['conversions'][tz_name] = {
                        'time': time_info['time'],
                        'utc_offset': time_info['utc_offset'],
                        'is_source': time_info['is_source'],
                        'relative_diff': time_info['relative_diff']
                    }
                
                with open(filename, 'w') as f:
                    json.dump(export_data, f, indent=2)
                    
            else:  # Default to text format
                with open(filename, 'w') as f:
                    f.write("PyTZ Buddy - Timezone Conversion Results\n")
                    f.write("=" * 50 + "\n")
                    f.write(f"Location: {results['location_info']['address']}\n")
                    f.write(f"Coordinates: {results['location_info']['latitude']:.4f}, {results['location_info']['longitude']:.4f}\n")
                    f.write(f"Timezone: {results['timezone']}\n")
                    f.write(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    
                    f.write("Time Conversions:\n")
                    f.write("-" * 30 + "\n")
                    
                    # Write source timezone first
                    for tz_name, time_info in results['conversions'].items():
                        if time_info['is_source']:
                            f.write(f"* {tz_name:20} | {time_info['time']} ({time_info['utc_offset']}) [SOURCE]\n")
                            break
                    
                    # Write other timezones
                    for tz_name, time_info in results['conversions'].items():
                        if not time_info['is_source']:
                            f.write(f"  {tz_name:20} | {time_info['time']} ({time_info['utc_offset']}) [{time_info['relative_diff']}]\n")
            
            return True, filename
            
        except Exception as e:
            return False, f"Export failed: {str(e)}"
    
    def suggest_similar_locations(self, failed_location):
        """Suggest similar locations when search fails"""
        suggestions = []
        
        # Common location suggestions based on partial matches
        location_lower = failed_location.lower()
        
        # City suggestions
        city_suggestions = {
            'new york': ['New York, NY', 'NYC', 'Manhattan'],
            'los angeles': ['Los Angeles, CA', 'LA', 'California'],
            'san francisco': ['San Francisco, CA', 'SF Bay Area'],
            'chicago': ['Chicago, IL', 'Illinois'],
            'miami': ['Miami, FL', 'Florida'],
            'seattle': ['Seattle, WA', 'Washington'],
            'boston': ['Boston, MA', 'Massachusetts'],
            'denver': ['Denver, CO', 'Colorado'],
            'atlanta': ['Atlanta, GA', 'Georgia'],
            'london': ['London, UK', 'London, England'],
            'paris': ['Paris, France'],
            'tokyo': ['Tokyo, Japan'],
            'beijing': ['Beijing, China'],
            'sydney': ['Sydney, Australia'],
            'mumbai': ['Mumbai, India'],
            'singapore': ['Singapore'],
            'dubai': ['Dubai, UAE'],
            'toronto': ['Toronto, Canada'],
            'mexico city': ['Mexico City, Mexico']
        }
        
        # Check for partial matches
        for key, values in city_suggestions.items():
            if key in location_lower or any(part in location_lower for part in key.split()):
                suggestions.extend(values)
        
        # Check timezone shortcuts
        for shortcut in self.timezone_shortcuts.keys():
            if shortcut in location_lower:
                suggestions.append(shortcut)
        
        # Remove duplicates and limit suggestions
        suggestions = list(set(suggestions))[:5]
        
        return suggestions
    
    def enhanced_location_lookup(self, location_name):
        """Enhanced location lookup with better error handling and suggestions"""
        # First try the normal lookup
        result = self.process_location(location_name)
        
        if result:
            return result, None
        
        # If failed, provide helpful suggestions
        suggestions = self.suggest_similar_locations(location_name)
        
        error_msg = f"Could not find timezone information for '{location_name}'"
        if suggestions:
            error_msg += f"\n\n💡 Did you mean one of these?\n"
            for i, suggestion in enumerate(suggestions, 1):
                error_msg += f"   {i}. {suggestion}\n"
            error_msg += "\nTip: Try being more specific (e.g., add country or state)"
        else:
            error_msg += "\n\n💡 Try:\n"
            error_msg += "   • Being more specific (e.g., 'Paris, France' instead of 'Paris')\n"
            error_msg += "   • Using timezone shortcuts like 'nyc', 'london', 'tokyo'\n"
            error_msg += "   • Checking spelling\n"
            error_msg += "   • Using 'help' command for examples"
        
        return None, error_msg

