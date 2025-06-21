#!/usr/bin/env python3
"""
Cache Manager for PyTZ Buddy
Handles persistent storage of search history and location geocoding results
"""

import json
import os
from datetime import datetime, timedelta

class CacheManager:
    def __init__(self, cache_dir=".pytz_cache"):
        """Initialize cache manager with specified cache directory"""
        self.cache_dir = cache_dir
        self.history_file = os.path.join(cache_dir, "search_history.json")
        self.location_cache_file = os.path.join(cache_dir, "location_cache.json")
        self.cache_duration_days = 30  # Cache geocoding results for 30 days
        
        # Create cache directory if it doesn't exist
        os.makedirs(cache_dir, exist_ok=True)
        
        # Initialize cache files if they don't exist
        self._init_cache_files()
    
    def _init_cache_files(self):
        """Initialize cache files with empty structures if they don't exist"""
        if not os.path.exists(self.history_file):
            self._write_json(self.history_file, [])
        
        if not os.path.exists(self.location_cache_file):
            self._write_json(self.location_cache_file, {})
    
    def _read_json(self, filepath):
        """Safely read JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError, PermissionError):
            return {} if filepath == self.location_cache_file else []
    
    def _write_json(self, filepath, data):
        """Safely write JSON file"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except (PermissionError, OSError):
            # Silently fail if we can't write (e.g., read-only filesystem)
            return False
    
    def get_search_history(self):
        """Get persistent search history"""
        return self._read_json(self.history_file)
    
    def add_to_history(self, location):
        """Add location to persistent search history"""
        history = self.get_search_history()
        
        # Remove if already exists to avoid duplicates
        if location in history:
            history.remove(location)
        
        # Add to beginning of list
        history.insert(0, location)
        
        # Keep only last 20 searches (increased from 10 for persistence)
        if len(history) > 20:
            history = history[:20]
        
        self._write_json(self.history_file, history)
        return history
    
    def get_cached_location(self, location_name):
        """Get cached geocoding result for a location"""
        cache = self._read_json(self.location_cache_file)
        location_key = location_name.lower().strip()
        
        if location_key in cache:
            cached_item = cache[location_key]
            # Check if cache entry is still valid
            cache_date = datetime.fromisoformat(cached_item['cached_at'])
            if datetime.now() - cache_date < timedelta(days=self.cache_duration_days):
                return cached_item['data']
            else:
                # Remove expired cache entry
                del cache[location_key]
                self._write_json(self.location_cache_file, cache)
        
        return None
    
    def cache_location(self, location_name, location_data):
        """Cache geocoding result for a location"""
        cache = self._read_json(self.location_cache_file)
        location_key = location_name.lower().strip()
        
        cache[location_key] = {
            'data': location_data,
            'cached_at': datetime.now().isoformat()
        }
        
        # Clean up old cache entries (keep max 100 entries)
        if len(cache) > 100:
            # Sort by cache date and keep only the 100 most recent
            sorted_items = sorted(
                cache.items(), 
                key=lambda x: x[1]['cached_at'], 
                reverse=True
            )
            cache = dict(sorted_items[:100])
        
        self._write_json(self.location_cache_file, cache)
    
    def clear_cache(self):
        """Clear all cached data"""
        self._write_json(self.history_file, [])
        self._write_json(self.location_cache_file, {})
        return True
    
    def get_cache_stats(self):
        """Get cache statistics for debugging"""
        history = self.get_search_history()
        cache = self._read_json(self.location_cache_file)
        
        return {
            'history_count': len(history),
            'cached_locations': len(cache),
            'cache_dir': self.cache_dir,
            'cache_size_mb': self._get_cache_size_mb()
        }
    
    def _get_cache_size_mb(self):
        """Calculate total cache size in MB"""
        total_size = 0
        try:
            for filename in [self.history_file, self.location_cache_file]:
                if os.path.exists(filename):
                    total_size += os.path.getsize(filename)
            return round(total_size / (1024 * 1024), 2)
        except OSError:
            return 0
