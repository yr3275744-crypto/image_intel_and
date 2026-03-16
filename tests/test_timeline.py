from src.timeline import create_timeline

# testing timeline's function
data = [{'filename': '20230118_070716.jpg', 'datetime': '2023:01:18 07:07:16', 'latitude': None, 'longitude': None, 'camera_make': 'samsung', 'camera_model': 'SM-A125F', 'has_gps': False},
{'filename': '20230205_183551.jpg', 'datetime': '2023:02:05 18:35:51', 'latitude': None, 'longitude': None, 'camera_make': 'samsung', 'camera_model': 'SM-A125F', 'has_gps': False}, 
{'filename': '20230207_155449.jpg', 'datetime': '2023:02:07 15:54:48', 'latitude': None, 'longitude': None, 'camera_make': 'LG Electronics', 'camera_model': 'LM-X210(G)', 'has_gps': True},
{'filename': '20230317_100725.jpg', 'datetime': '2023:03:17 10:07:24', 'latitude': None, 'longitude': None, 'camera_make': 'samsung', 'camera_model': 'SM-A125F', 'has_gps': False}, 
{'filename': '20230801_190044.jpg', 'datetime': '2023:08:01 19:00:44', 'latitude': None, 'longitude': None, 'camera_make': 'samsung', 'camera_model': 'Galaxy A24', 'has_gps': False},
{'filename': '20230803_114132.jpg', 'datetime': '2023:08:03 11:41:33', 'latitude': 28.528802999722224, 'longitude': 34.46990149972222, 'camera_make': 'samsung', 'camera_model': 'Galaxy A24', 'has_gps': True}, 
{'filename': '20230803_125716.jpg', 'datetime': '2023:08:03 12:57:16', 'latitude': 29.433605166666666, 'longitude': 34.82882308333333, 'camera_make': 'samsung', 'camera_model': 'Galaxy A24', 'has_gps': True}, 
{'filename': 'תהלוכה.jpg', 'datetime': None, 'latitude': None, 'longitude': None, 'camera_make': None, 'camera_model': None, 'has_gps': False}, 
{'filename': 'תמונה של WhatsApp\u200f 2024-02-29 בשעה 21.06.20_9ba8ad59.jpg', 'datetime': None, 'latitude': None, 'longitude': None, 'camera_make': None, 'camera_model': None, 'has_gps': False}, 
{'filename': 'תמונה של WhatsApp\u200f 2024-03-07 בשעה 16.46.37_38b91f13.jpg', 'datetime': None, 'latitude': None, 'longitude': None, 'camera_make': None, 'camera_model': None, 'has_gps': False}, 
{'filename': 'תמונה של WhatsApp\u200f 2024-05-25 בשעה 23.26.41_fb540559 - Copy.jpg', 'datetime': None, 'latitude': None, 'longitude': None, 'camera_make': None, 'camera_model': None, 'has_gps': False}, 
{'filename': 'תמונה של WhatsApp\u200f 2024-06-08 בשעה 22.25.21_39231de9.jpg', 'datetime': None, 'latitude': None, 'longitude': None, 'camera_make': None, 'camera_model': None, 'has_gps': False},
{'filename': '20230207_155449.jpg', 'datetime': '2023:02:07 15:54:48', 'latitude': None, 'longitude': None, 'camera_make': 'LG Electronics', 'camera_model': 'LM-X210(G)', 'has_gps': True},
{'filename': '20230803_125716.jpg', 'datetime': '2023:08:03 12:57:16', 'latitude': 29.433605166666666, 'longitude': 34.82882308333333, 'camera_make': 'samsung', 'camera_model': 'Galaxy A24', 'has_gps': True}
]

def test_create_timeline_without_dateTime():
    assert create_timeline([{'file': '2'},{'fije': '2023'}]) == "No date/time."

def test_create_timeline_with_dateTime():
    assert type(create_timeline(data)) == str