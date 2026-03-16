import math
from datetime import datetime
from src.analyzer import calc_distance,analyze

# testing analyzer function's
def test_calc_distance_with_values():
    assert calc_distance(48.8584,2.2945,40.6892,-74.0445) == 5837.415828612747

def test_calc_distance_without_values():
    assert calc_distance(48.8584,2.2945,40.6892,None) == float('inf')

def test_analyze_empty_without():
    assert analyze([{"file":"23","gsed":23}]) == {'total_images': 1, 'images_with_gps': 0, 'images_with_datetime': 0, 'unique_cameras': [], 'date_range': {'start': None, 'end': None}, 'insights': ['אזהרה: לאף תמונה אין נתוני מיקום. ייתכן שהיעד מנטרל GPS באופן יזום.']}

def get_fake_data():
    return [
        {"filename": "t1.jpg", "latitude": 32.0, "longitude": 34.7, 
         "has_gps": True, "camera_make": "Samsung", "camera_model": "Galaxy S23", 
         "datetime": "2025-01-12 08:30:00"},
        {"filename": "t2.jpg", "latitude": 31.7, "longitude": 35.2, 
         "has_gps": True, "camera_make": "Apple", "camera_model": "iPhone 15 Pro", 
         "datetime": "2025-01-13 09:00:00"},
    ]

def test_analyze_returns_dict():
    result = analyze(get_fake_data())
    assert isinstance(result, dict)

def test_analyze_has_required_fields():
    result = analyze(get_fake_data())
    assert "total_images" in result
    assert "images_with_gps" in result
    assert "unique_cameras" in result
    assert "insights" in result

def test_analyze_counts_correctly():
    result = analyze(get_fake_data())
    assert result["total_images"] == 2
    assert result["images_with_gps"] == 2

def test_analyze_handles_empty():
    result = analyze([])
    assert result["total_images"] == 0