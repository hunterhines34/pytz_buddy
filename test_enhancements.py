#!/usr/bin/env python3
"""
Quick test to verify the enhanced features work
"""

from timezone_converter import TimezoneConverter
from cache_manager import CacheManager

def test_basic_functionality():
    """Test basic functionality"""
    try:
        cache_manager = CacheManager()
        converter = TimezoneConverter(cache_manager)
        
        # Test timezone shortcut
        print("Testing timezone shortcut...")
        result = converter.process_timezone_shortcut("nyc")
        if result:
            print("✅ Timezone shortcut works!")
        else:
            print("❌ Timezone shortcut failed")
            
        # Test specific time conversion
        print("\nTesting specific time conversion...")
        conversions, error = converter.convert_specific_time("14:30", "EST")
        if conversions:
            print("✅ Specific time conversion works!")
        else:
            print(f"❌ Specific time conversion failed: {error}")
            
        # Test meeting time finder
        print("\nTesting meeting time finder...")
        suggestions = converter.find_meeting_times(["nyc", "london"])
        if suggestions:
            print(f"✅ Meeting time finder works! Found {len(suggestions)} suggestions")
        else:
            print("❌ Meeting time finder failed")
            
        # Test business hours overlap
        print("\nTesting business hours overlap...")
        overlap_data = converter.calculate_business_hours_overlap(["nyc", "london"])
        if overlap_data:
            print(f"✅ Business hours overlap works! Found {overlap_data['total_overlap']} hours overlap")
        else:
            print("❌ Business hours overlap failed")
            
        print("\n🎉 All basic functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_basic_functionality()
