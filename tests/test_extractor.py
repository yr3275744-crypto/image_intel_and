import sys
import os

from src.extractor import has_gps, latitude, longitude, datatime, camera_make, camera_model, extract_all, extract_metadata
#from extractor import has_gps,latitude,longitude,datatime,camera_make,camera_model,extract_all,extract_metadata

# testing extractor functions
def test_false_has_gps():
    assert has_gps({"no_gps":2}) == False

def test_latitude_without_GPSInfo():
    assert latitude({"hello":"3"}) == None

def test_latitude_insufficent_info():
    assert latitude({"GPSInfo":{5: 2.2, 6: 0.0}}) == None

def test_latitude_calculation():
    assert latitude({"GPSInfo":{1: 'N', 2: (28.0, 31.0, 43.690799), 3: 'E', 4: (34.0, 28.0, 11.645399), 5: 0, 6: 116.0}}) == 28.52880299972222

def test_longitude_without_GPSInfo():
    assert longitude({"hello":"3"}) == None

def test_longitude_insufficent_info():
    assert longitude({"GPSInfo":{5: 2.2, 6: 0.0}}) == None

def test_longitude_calculation():
    assert longitude({"GPSInfo":{1: 'S', 2: (28.0, 31.0, 43.690799), 3: 'W', 4: (34.0, 28.0, 11.645399), 5: 0, 6: 116.0}}) == -34.469901499722226

def test_no_DateTime():
    assert datatime({"hello":"3"}) == None

def test_with_CameraMake():
    assert camera_make({'Make': 'samsung\x00'}) == "samsung"

def test_without_CameraMake():
    assert camera_make({'Maker': 'samsung\x00'}) == None

def test_with_CameraModel():
    assert camera_model({'Model': 'SM-A125F','hello':'e2d'}) == "SM-A125F"

def test_without_CameraModel():
    assert camera_model({'camera_s': 'SM-A125F','hello':'e2d'}) == None

def test_extract_all_no_images():
    assert extract_all(r"C:\Users\yaako\Downloads\kodcode\finale_project_prog\image_intel_and\tools") == []

def test_extract_metadata_returns_dict():

    result = extract_metadata("images/sample_data/IMG_001.jpg")
    assert isinstance(result, dict)

def test_extract_metadata_has_required_fields():
    result = extract_metadata("images/sample_data/IMG_001.jpg")
    required = ["filename", "datetime", "latitude", "longitude", 
                "camera_make", "camera_model", "has_gps"]
    for field in required:
        assert field in result, f"Missing field: {field}"

def test_extract_metadata_gps_is_float_or_none():
    result = extract_metadata("images/sample_data/IMG_001.jpg")
    if result["has_gps"]:
        assert isinstance(result["latitude"], float)
        assert isinstance(result["longitude"], float)
    else:
        assert result["latitude"] is None
        assert result["longitude"] is None

def test_extract_all_returns_list():
    result = extract_all("images/sample_data")
    assert isinstance(result, list)
    assert len(result) > 0

def test_extract_all_handles_empty_folder(tmp_path):
    result = extract_all(str(tmp_path))
    assert isinstance(result, list)
    assert len(result) == 0