from PIL import Image
from PIL.ExifTags import TAGS
from pathlib import Path
import os

"""
extractor.py - שליפת EXIF מתמונות
צוות 1, זוג A

ראו docs/api_contract.md לפורמט המדויק של הפלט.

"""


def has_gps(data: dict):
    if not "GPSInfo" in data.keys():
        return False
    else:
        return True


def latitude(data: dict):
    if not "N" or not "S" in data.values():
        return None
    dms = data["GPSInfo"]
    gps_latitude = dms["2"]
    the_latitude = gps_latitude[0]+gps_latitude[1]/60+gps_latitude[2]/3600
    if dms["3"] == "W":
        the_latitude = -the_latitude
    return the_latitude

def longitude(data: dict):
    if not "E" or not "W" in data.values():
        return None 
    dms = data["GPSInfo"]
    gps_longitude = dms["4"]
    the_longitude = gps_longitude[0]+gps_longitude[1]/60+gps_longitude[2]/3600
    if dms["1"] == "S":
        the_longitude = -the_longitude
    return the_longitude

def datatime(data: dict):
    if type(data)== dict:
        return data["DateTime"]
    else:
        return None

def camera_make(data: dict):
    if type(data)== dict:
        return data["Make"]
    else:
        return None

def camera_model(data: dict):
    if type(data)== dict:
        return data["Model"]
    else:
        return None


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

    # תיקון: טיפול בתמונה בלי EXIF - בלי זה, exif.items() נופל עם AttributeError
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

    # תיקון: הוסר print(data) שהיה כאן - הדפיס את כל ה-EXIF הגולמי על כל תמונה

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
    path_object = Path(folder_path)
    if not path_object.exists() or not path_object.is_dir():
        return []
    
    image_data = []
    valid_extensions = [".jpg", ".jpeg", ".png"]
    
    for file_path in path_object.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in valid_extensions:
            image_data.append(extract_metadata(file_path))
    return image_data