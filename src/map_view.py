"""
map_view.py - יצירת מפה אינטראקטיבית
צוות 1, זוג B

ראו docs/api_contract.md לפורמט הקלט והפלט.

=== תיקונים ===
1. חישוב מרכז המפה - היה עובר על images_data (כולל תמונות בלי GPS) במקום gps_image, נופל עם None
2. הסרת CustomIcon שלא עובד (filename זה לא נתיב שהדפדפן מכיר)
3. הסרת m.save() - לפי API contract צריך להחזיר HTML string, לא לשמור קובץ
4. הסרת fake_data מגוף הקובץ - הועבר ל-if __name__
5. תיקון color_index - היה מתקדם על כל תמונה במקום רק על מכשיר חדש
6. הוספת מקרא מכשירים
"""

import folium


def sort_by_time(arr):
    pass


def create_map(images_data):
    """
    יוצר מפה אינטראקטיבית עם כל המיקומים.

    Args:
        images_data: רשימת מילונים מ-extract_all

    Returns:
        string של HTML (המפה)
    """
    gps_images = [img for img in images_data if img["has_gps"] and img["latitude"] and img["longitude"]]
    
    if not gps_images:
        return "<h2>No GPS data found</h2>"
    
    center_lat = sum(img["latitude"] for img in gps_images) / len(gps_images)
    center_lon = sum(img["longitude"] for img in gps_images) / len(gps_images)
    
    m = folium.Map(location=[center_lat, center_lon], zoom_start=8)
    colors = ['black', 'beige', 'lightblue', 
              'gray', 'blue', 'darkred', 
              'lightgreen', 'purple', 'red', 
              'green', 'lightred', 'white', 
              'darkblue', 'darkpurple', 'cadetblue', 
              'orange', 'pink', 'lightgray', 'darkgreen']
    cameras = set([img['camera_model'] for img in gps_images if img['camera_model']])
    #בודק אם יש מספיק צבעים לכל סוגי המצלמות
    if len(cameras) <= len(colors):
        color_for_camera = {camera:colors.pop() for camera in cameras}
        for img in gps_images:
            if img['camera_model']:
                folium.Marker(
                    location=[img["latitude"], img["longitude"]],
                    popup=f"{img['filename']}<br>{img['datetime']}<br>{img['camera_model']}",
                    icon= folium.Icon(color_for_camera[img['camera_model']])
                ).add_to(m)
            else:
                            folium.Marker(
                location=[img["latitude"], img["longitude"]],
                popup=f"{img['filename']}<br>{img['datetime']}<br>{img['camera_model']}",
            ).add_to(m)
    else:
        for img in gps_images:
            folium.Marker(
                location=[img["latitude"], img["longitude"]],
                popup=f"{img['filename']}<br>{img['datetime']}<br>{img['camera_model']}",
            ).add_to(m)
    
    return m._repr_html_()
