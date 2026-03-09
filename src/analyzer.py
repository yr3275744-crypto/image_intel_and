def analyze(images_data: list[dict]) -> dict:
    total_images = len(images_data)
    images_with_gps = sum(1 for img in images_data if img.get('has_gps'))
    
    cameras_set = set()
    valid_dates = []
    timeline_devices = []
    
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
            if make and model:
                timeline_devices.append((dt_str, f"{make} {model}"))

    unique_cameras = list(cameras_set)
    
    date_range = {"start": None, "end": None}
    if valid_dates:
        valid_dates.sort()
        date_range["start"] = valid_dates[0].split(" ")[0]
        date_range["end"] = valid_dates[-1].split(" ")[0]

    insights = []
    
    if len(unique_cameras) > 1:
        insights.append(f"נמצאו {len(unique_cameras)} מכשירים שונים.")
    elif len(unique_cameras) == 1:
        insights.append("כל התמונות צולמו מאותו מכשיר.")
        
    if len(unique_cameras) > 1 and timeline_devices:
        timeline_devices.sort(key=lambda x: x[0])
        first_device = timeline_devices[0][1]
        for dt, device in timeline_devices:
            if device != first_device:
                date_only = dt.split(" ")[0]
                insights.append(f"הסוכן החליף מכשיר ב-{date_only} (מ-{first_device} ל-{device}).")
                break

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
                
    if tlv_count > 0:
        insights.append(f"ריכוז של {tlv_count} תמונות באזור תל אביב/גוש דן.")
    if jeru_count > 0:
        insights.append(f"ריכוז של {jeru_count} תמונות באזור ירושלים.")

    if total_images > 0 and images_with_gps == 0:
         insights.append("אזהרה: לאף תמונה אין נתוני מיקום. ייתכן שהיעד מנטרל GPS באופן יזום.")

    return {
        "total_images": total_images,
        "images_with_gps": images_with_gps,
        "unique_cameras": unique_cameras,
        "date_range": date_range,
        "insights": insights
    }