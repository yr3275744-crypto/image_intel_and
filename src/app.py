from flask import Flask, render_template, request
import os
import sys

# מוודאים שתיקיית src נמצאת בנתיב כדי שהייבוא יעבוד בצורה חלקה
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# ייבוא מהמודולים של הצוותים השונים (חייבים להיות באותה תיקיית src)
from extractor import extract_all
from map_view import create_map
from timeline import create_timeline
from analyzer import analyze
from report import create_report

app = Flask(__name__)

@app.route('/')
def index():
    """דף הבית - טופס לבחירת תיקייה"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_images():
    print("aaaaaa")
    """מקבל נתיב תיקייה, מריץ את כל המודולים, ומחזיר דו"ח מלא"""
    folder_path = request.form.get('images')
    
    # 1. אימות קלט - צוות 3 זוג A
    if not folder_path or not os.path.isdir(folder_path):
        return "שגיאה: התיקייה לא נמצאה או שהנתיב אינו חוקי.", 400
    
    print(f"--- Starting Full Intel Analysis on: {folder_path} ---")

    # 2. חילוץ נתונים - צוות 1 זוג A
    print("Extracting metadata...")
    try:
        images_data = extract_all(folder_path) 
    except Exception as e:
        return f"שגיאה בחילוץ הנתונים (extractor.py): {str(e)}", 500

    if not images_data:
        return "לא נמצאו תמונות תקינות או נתוני EXIF בתיקייה שסופקה."

    # 3. יצירת מפה - צוות 1 זוג B
    print("Generating interactive map...")
    try:
        map_html = create_map(images_data)
    except Exception as e:
        print(f"Map Error: {e}")
        map_html = "<div style='color: red; padding: 10px; border: 1px solid red;'>שגיאה בטעינת המפה (map_view.py)</div>"

    # 4. ציר זמן - צוות 2 זוג A
    print("Creating timeline...")
    try:
        timeline_html = create_timeline(images_data)
    except Exception as e:
        print(f"Timeline Error: {e}")
        timeline_html = "<div style='color: red; padding: 10px; border: 1px solid red;'>שגיאה בטעינת ציר הזמן (timeline.py)</div>"

    # 5. ניתוח דפוסים - צוות 2 זוג B
    print("Running data analysis...")
    try:
        analysis = analyze(images_data)
    except Exception as e:
        print(f"Analyzer Error: {e}")
        analysis = {"total_images": len(images_data), "insights": ["אירעה שגיאה בניתוח הנתונים (analyzer.py)"]}

    # 6. הרכבת הדו"ח הסופי - צוות 3 זוג B
    print("Assembling final report...")
    try:
        report_html = create_report(images_data, map_html, timeline_html, analysis)
        return report_html
    except Exception as e:
        return f"שגיאה בהפקת הדו\"ח (report.py): {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)