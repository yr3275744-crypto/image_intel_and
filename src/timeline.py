import plotly.express as px
import pandas as pd
def create_timeline(images_data: list[dict]) -> str:
    """
    יוצר ציר זמן ויזואלי של התמונות.
    
    מקבל: רשימת מילונים מ-extract_all (מסנן בעצמו רק תמונות עם datetime)
    מחזיר: string של HTML (ציר הזמן כ-HTML)
    """

    images_with_datetime = [d for d in images_data if d.get('datetime')]
    if not images_with_datetime:
        return "No date/time."
            
    """המרה לטבלה לצורך עבודה עם ספריית העיצוב"""
    images_data_frame = pd.DataFrame(images_with_datetime)
    fig = px.scatter(
        images_data_frame, 
        x='datetime', 
        y=[1] * len(images_data_frame), # מציבים את כל הנקודות על אותו גובה (קו אופקי)
        hover_name='filename', # הכותרת של הבועה שתצוף
        hover_data=['latitude', 'longitude', 'camera_make', 'camera_model', 'has_gps'], # כל המטא-דאטה שתוצג
        title="Image Analysis Timeline"
    )

    fig.update_yaxes(visible=False) # עדכון ציר ה y לאפס כדי ליצור מראה יפה יותר ויזואלית

    return fig.to_html()