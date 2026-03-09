from PIL import Image
from PIL.ExifTags import TAGS
from pathlib import Path
import os

"""
extractor.py - שליפת EXIF מתמונות
צוות 1, זוג A

ראו docs/api_contract.md לפורמט המדויק של הפלט.

"""

# checks if has any gps info
def has_gps(data: dict):
    if not "GPSInfo" in data.keys():
        return False
    else:
        return True

# calculates latitude
def latitude(data: dict):
    # checks if there is sufficnet info in GPSInfo to calculate latitude
    if "GPSInfo" in data.keys():
        gps_info = data["GPSInfo"]
        if not "N" or not "S" in gps_info.values():
            return None
    else:
        return None
    dms = data["GPSInfo"] # store the value from GPSInfo which is a dict
    gps_latitude = dms["2"] # stores the tuple (containg three values) which has the coordinates for latitude
    # the formula
    the_latitude = gps_latitude[0]+gps_latitude[1]/60+gps_latitude[2]/3600 
    if dms["3"] == "W":
        the_latitude = -the_latitude
    return the_latitude

# calculates latitude
def longitude(data: dict):
    # checks if there is sufficnet info in GPSInfo to calculate latitude
    if "GPSInfo" in data.keys():
        gps_info = data["GPSInfo"]
        if not "N" or not "S" in gps_info.values():
            return None
    else:
        return None
    dms = data["GPSInfo"] # store the value from GPSInfo which is a dict
    gps_longitude = dms["4"] # stores the tuple (containg three values) which has the coordinates for longitude
    # the formula
    the_longitude = gps_longitude[0]+gps_longitude[1]/60+gps_longitude[2]/3600
    if dms["1"] == "S":
        the_longitude = -the_longitude
    return the_longitude
# returns the value of the key DateTime
def datatime(data: dict):
    if type(data)== dict:
        return data["DateTime"]
    else:
        return None
# returns the value of the key Make
def camera_make(data: dict):
    if type(data)== dict:
        return data["Make"].strip("\x00")
    else:
        return None
# returns the value of the key Model
def camera_model(data: dict):
    if type(data)== dict:
        return data["Model"].strip("\x00")
    else:
        return None

# this function was premade
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

# returns a list containg all of the dicts which contain the data of the pics of the given folder
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