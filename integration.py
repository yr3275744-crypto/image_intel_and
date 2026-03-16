import os
import glob
from src.extractor import extract_metadata, extract_all
from src.map_view import create_map
from src.timeline import create_timeline
from src.analyzer import analyze
from src.report import create_report

def main():

    folder_path = "images" 
    output_file = "final_report.html"
    
    if not os.path.isdir(folder_path):
        print(f"Error: Folder '{folder_path}' not found.")
        return

    print("--- Starting Full Intel Analysis ---")

    # Extraction
    print("Extracting metadata...")
    # using extract all from extractor.py and so on for the rest of the functions 
    images_data = extract_all(folder_path) 
    
    if not images_data:
        print("No image data found.")
        return

    print("Generating interactive map...")
    try:
        map_html = create_map(images_data)
    except Exception:
        map_html = "<h2>Map Placeholder (Error loading map_view)</h2>"

    print("Creating timeline...")
    try:
        timeline_html = create_timeline(images_data)
    except Exception:
        timeline_html = "<p>Timeline not available.</p>"

    print("Running data analysis...")
    try:
        analysis = analyze(images_data)
    except Exception:
        # Fallback if analyzer.py isn't ready
        analysis = {"total_images": len(images_data), "insights": ["Basic analysis only."]}

    print("Assembling final report...")
    report_html = create_report(images_data, map_html, timeline_html, analysis)

    # saving to file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report_html)
    
    print(f"\n--- SUCCESS! ---")
    print(f"Full report created: {os.path.abspath(output_file)}")

if __name__ == "__main__":
    main()