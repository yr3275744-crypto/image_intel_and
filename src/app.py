import os
from flask import Flask, render_template, request, flash, redirect
from werkzeug.utils import secure_filename
import tempfile
import shutil

# Import our modules
import extractor
import map_view

# Note: These might not exist yet, so we use dummy functions or try-except
try:
    import timeline
except ImportError:
    timeline = None

try:
    import analyzer
except ImportError:
    analyzer = None

try:
    import report
except ImportError:
    report = None

app = Flask(__name__)
app.secret_key = "supersecretkey"

UPLOAD_FOLDER = tempfile.mkdtemp()
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'tiff'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def do_analyze():
    if 'photos' not in request.files:
        return redirect(request.url)
    
    files = request.files.getlist('photos')
    
    # Create a temporary directory for this session's photos
    session_dir = tempfile.mkdtemp(dir=UPLOAD_FOLDER)
    
    images_data = []
    
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(session_dir, filename)
            file.save(file_path)
            
            # Extract metadata using our extractor
            data = extractor.extract_metadata(file_path)
            images_data.append(data)
    
    if not images_data:
        return "No valid images uploaded", 400

    # 1. Generate Map
    map_html = map_view.create_map(images_data)
    
    # 2. Generate Timeline (with fallback)
    if timeline:
        timeline_html = timeline.create_timeline(images_data)
    else:
        timeline_html = "<div style='color: #94a3b8; padding: 20px;'>Timeline module not implemented yet</div>"
    
    # 3. Perform Analysis (with fallback)
    if analyzer:
        analysis_results = analyzer.analyze(images_data)
    else:
        # Dummy analysis
        analysis_results = {
            "total_images": len(images_data),
            "images_with_gps": len([img for img in images_data if img['has_gps']]),
            "insights": ["Analyzer module not implemented yet"]
        }
    
    # 4. Generate Final Report (with fallback)
    if report:
        final_report_html = report.create_report(images_data, map_html, timeline_html, analysis_results)
        return final_report_html
    else:
        # Fallback view if report module is missing
        insights_list = "".join(f"<li>{i}</li>" for i in analysis_results['insights'])
        return f"""
        <html>
            <head>
                <title>Image Intel Report</title>
                <style>
                    body {{ font-family: 'Segoe UI', sans-serif; padding: 40px; background: #0f172a; color: #f8fafc; line-height: 1.6; }}
                    h1 {{ color: #38bdf8; border-bottom: 2px solid #1e293b; padding-bottom: 10px; }}
                    h2 {{ color: #94a3b8; margin-top: 30px; }}
                    .card {{ background: #1e293b; padding: 20px; border-radius: 12px; margin-bottom: 20px; border: 1px solid #334155; }}
                    ul {{ list-style-type: square; color: #38bdf8; }}
                    li {{ color: #cbd5e1; margin-bottom: 5px; }}
                    .map-container {{ height: 500px; width: 100%; border-radius: 12px; overflow: hidden; border: 1px solid #475569; }}
                    iframe {{ width: 100%; height: 100%; border: none; }}
                </style>
            </head>
            <body>
                <h1>Image Intel - דוח מודיעיני ראשוני</h1>
                
                <div class="card">
                    <h2>סיכום ניתוח</h2>
                    <p>סה"כ תמונות שנסרקו: <strong>{analysis_results['total_images']}</strong></p>
                    <p>תמונות עם נתוני מיקום: <strong>{analysis_results['images_with_gps']}</strong></p>
                    <h3>תובנות:</h3>
                    <ul>{insights_list}</ul>
                </div>

                <h2>מפת מיקומים</h2>
                <div class="card map-container">
                    <iframe srcdoc="{map_html.replace('"', '&quot;')}"></iframe>
                </div>

                <h2>ציר זמן</h2>
                <div class="card">
                    {timeline_html}
                </div>
            </body>
        </html>
        """

if __name__ == '__main__':
    app.run(debug=True, port=5000)
