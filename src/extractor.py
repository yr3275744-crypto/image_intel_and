from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from pathlib import Path
import os
from datetime import datetime

"""
extractor.py - שליפת EXIF מתמונות
צוות 1, זוג A

ראו docs/api_contract.md לפורמט המדויק של הפלט.
"""


def _get_if_exist(data, key):
    if key in data:
        return data[key]
    return None


def _convert_to_degrees(value):
    """
    Helper function to convert the GPS coordinates stored in the EXIF to degress in float format
    """
    d = float(value[0])
    m = float(value[1])
    s = float(value[2])
    return d + (m / 60.0) + (s / 3600.0)


def has_gps(data: dict):
    return 'GPSInfo' in data


def latitude(data: dict):
    if 'GPSInfo' in data:
        gps_info = data['GPSInfo']
        gps_latitude = _get_if_exist(gps_info, 2)
        gps_latitude_ref = _get_if_exist(gps_info, 1)
        if gps_latitude and gps_latitude_ref:
            lat = _convert_to_degrees(gps_latitude)
            if gps_latitude_ref != 'N':
                lat = 0 - lat
            return lat
    return None


def longitude(data: dict):
    if 'GPSInfo' in data:
        gps_info = data['GPSInfo']
        gps_longitude = _get_if_exist(gps_info, 4)
        gps_longitude_ref = _get_if_exist(gps_info, 3)
        if gps_longitude and gps_longitude_ref:
            lon = _convert_to_degrees(gps_longitude)
            if gps_longitude_ref != 'E':
                lon = 0 - lon
            return lon
    return None


def datatime(data: dict):
    dt_str = _get_if_exist(data, 'DateTimeOriginal') or _get_if_exist(data, 'DateTime')
    if dt_str:
        try:
            # Common EXIF format: YYYY:MM:DD HH:MM:SS
            return datetime.strptime(dt_str, '%Y:%m:%d %H:%M:%S').isoformat()
        except ValueError:
            return dt_str
    return None


def camera_make(data: dict):
    return _get_if_exist(data, 'Make')


def camera_model(data: dict):
    return _get_if_exist(data, 'Model')


def extract_metadata(image_path):
    """
    שולף EXIF מתמונה בודדת.

    Args:
        image_path: נתיב לקובץ תמונה

    Returns:
        dict עם: filename, datetime, latitude, longitude,
              camera_make, camera_model, has_gps
    """
    path = Path(image_path)

    try:
        img = Image.open(image_path)
        exif = img._getexif()
    except Exception:
        exif = None

    if exif is None:
        return {
            "filename": path.name,
            "datetime": None,
            "latitude": None,
            "longitude": None,
            "camera_make": None,
            "camera_model": None,
            "has_gps": False
        }

    data = {}
    for tag_id, value in exif.items():
        tag = TAGS.get(tag_id, tag_id)
        data[tag] = value

    exif_dict = {
        "filename": path.name,
        "datetime": datatime(data),
        "latitude": latitude(data),
        "longitude": longitude(data),
        "camera_make": camera_make(data),
        "camera_model": camera_model(data),
        "has_gps": has_gps(data)
    }
    return exif_dict


def extract_all(folder_path):
    """
    שולף EXIF מכל התמונות בתיקייה.

    Args:
        folder_path: נתיב לתיקייה

    Returns:
        list של dicts (כמו extract_metadata)
    """
    results = []
    folder = Path(folder_path)
    
    # Common image extensions
    extensions = ('.jpg', '.jpeg', '.png', '.tiff', '.webp')
    
    if not folder.exists():
        return results

    for file_path in folder.iterdir():
        if file_path.suffix.lower() in extensions:
            results.append(extract_metadata(str(file_path)))
            
    return results
