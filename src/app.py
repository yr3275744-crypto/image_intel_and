from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/')
def index():
    """דף הבית - טופס לבחירת תיקייה"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_images():
    """מקבל נתיב תיקייה, מריץ את כל המודולים, מחזיר דו"ח"""
    folder_path = request.form.get('folder_path')
    
    if not folder_path or not os.path.isdir(folder_path):
        return "תיקייה לא נמצאה", 400
    
    # שלב 1: שליפת נתונים
    from extractor import extract_all
    images_data = extract_all(folder_path)
    
    # שלב 2: יצירת מפה
    from map_view import create_map
    map_html = create_map(images_data)
    
    # שלב 3: ציר זמן
    from timeline import create_timeline
    timeline_html = create_timeline(images_data)

    # שלב 4: ניתוח
    from analyzer import analyze
    analysis = analyze(images_data)
    
    # שלב 5: הרכבת דו"ח
    from report import create_report
    report_html = create_report(images_data, map_html, timeline_html, analysis)
    
    return report_html

if __name__ == '__main__':
    app.run(debug=True)


### טיפ קריטי
##**אל תחכו לצוותים האחרים!** בשלב ראשון, צרו פונקציות דמה:
def fake_extract_all(folder):
    return [{'filename': 'test2.jpg', 'latitude': 31.7683, 'longitude': 35.2137, 'has_gps': True, 'camera_make': 'Apple', 'camera_model': 'iPhone 15 Pro', 'datetime': None},
            {'filename': 'test1.jpg', 'latitude': 32.0853, 'longitude': 34.7818, 'has_gps': True, 'camera_make': 'Samsung', 'camera_model': 'Galaxy S23', 'datetime': '2025-01-12 08:30:00'},
            {'filename': 'test2.jpg', 'latitude': 31.7683, 'longitude': 35.2137, 'has_gps': True, 'camera_make': 'Apple', 'camera_model': 'iPhone 15 Pro', 'datetime': '2025-01-13 09:00:00'}]

def fake_create_map(data):
    return "<h2>Map placeholder</h2>"
