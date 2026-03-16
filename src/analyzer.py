import math
from datetime import datetime

def calc_distance(lat1, lon1, lat2, lon2):
    if None in (lat1, lon1, lat2, lon2): 
        return float('inf')
    R = 6371.0 
    lat1_r = math.radians(lat1)
    lon1_r = math.radians(lon1)
    lat2_r = math.radians(lat2)
    lon2_r = math.radians(lon2)
    
    dlon = lon2_r - lon1_r
    dlat = lat2_r - lat1_r
    a = math.sin(dlat / 2)**2 + math.cos(lat1_r) * math.cos(lat2_r) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def analyze(images_data: list[dict]) -> dict:
    total_images = len(images_data)
    images_with_gps = sum(1 for img in images_data if img.get('has_gps'))
    images_with_datetime = sum(1 for img in images_data if img.get('datetime'))

    cameras_set = set()
    valid_dates = []

    for img in images_data:
        make = img.get('camera_make')
        model = img.get('camera_model')
        
        if make and model:
            cameras_set.add(f"{make} {model}")
        elif model:
            cameras_set.add(model)
            
        dt_str = img.get('datetime')
        if dt_str:
            valid_dates.append(dt_str)

    unique_cameras = list(cameras_set)
    
    date_range = {"start": None, "end": None}
    if valid_dates:
        valid_dates.sort()
        date_range["start"] = valid_dates[0].split(" ")[0]
        date_range["end"] = valid_dates[-1].split(" ")[0]

    insights = []
    
    if len(unique_cameras) > 1:
        insights.append(f"נמצאו {len(unique_cameras)} מכשירים שונים - ייתכן שהסוכן החליף מכשירים.")
    elif len(unique_cameras) == 1:
        insights.append("כל התמונות צולמו מאותו מכשיר.")

    chronological_images = sorted(
        [img for img in images_data if img.get("datetime")],
        key=lambda x: x["datetime"]
    )

    for i in range(1, len(chronological_images)):
        prev_cam = chronological_images[i-1].get("camera_model")
        curr_cam = chronological_images[i].get("camera_model")
        
        if prev_cam and curr_cam and prev_cam != curr_cam:
            date_full = chronological_images[i]["datetime"]
            date_formatted = f"{date_full[8:10]}/{date_full[5:7]}"
            insights.append(f"ב-{date_formatted} הסוכן עבר ממכשיר {prev_cam} ל-{curr_cam}.")

    for i in range(1, len(chronological_images)):
        try:
            dt1 = datetime.strptime(chronological_images[i-1]["datetime"], "%Y-%m-%d %H:%M:%S")
            dt2 = datetime.strptime(chronological_images[i]["datetime"], "%Y-%m-%d %H:%M:%S")
            hours_diff = (dt2 - dt1).total_seconds() / 3600
            if hours_diff >= 12:
                insights.append(f"פער זמן גדול של {int(hours_diff)} שעות זוהה בין תמונות רצופות.")
        except ValueError:
            pass

    tlv_count = 0
    jeru_count = 0
    for img in images_data:
        lat = img.get('latitude')
        lon = img.get('longitude')
        if lat and lon:
            if 31.9 < lat < 32.2 and 34.6 < lon < 34.9:
                tlv_count += 1
            elif 31.6 < lat < 31.9 and 35.1 < lon < 35.4:
                jeru_count += 1
                
    if tlv_count >= 3:
        insights.append(f"ריכוז של {tlv_count} תמונות באזור תל אביב.")
    
    if jeru_count >= 3:
        insights.append(f"ריכוז של {jeru_count} תמונות באזור ירושלים.")

    gps_images = [img for img in chronological_images if img.get('latitude') and img.get('longitude')]
    returned = False
    for i in range(2, len(gps_images)):
        curr = gps_images[i]
        for j in range(i-1):
            past = gps_images[j]
            if calc_distance(curr['latitude'], curr['longitude'], past['latitude'], past['longitude']) < 1.0:
                for k in range(j+1, i):
                    mid = gps_images[k]
                    if calc_distance(past['latitude'], past['longitude'], mid['latitude'], mid['longitude']) > 1.0:
                        date_only = curr["datetime"].split(" ")[0]
                        insights.append(f"ב-{date_only} הסוכן חזר למיקום קודם לאחר שעזב אותו.")
                        returned = True
                        break
            if returned: break
        if returned: break

    if total_images > 0 and images_with_gps == 0:
         insights.append("אזהרה: לאף תמונה אין נתוני מיקום. ייתכן שהיעד מנטרל GPS באופן יזום.")

    return {
        "total_images": total_images,
        "images_with_gps": images_with_gps,
        "images_with_datetime": images_with_datetime,
        "unique_cameras": unique_cameras,
        "date_range": date_range,
        "insights": insights
    }
