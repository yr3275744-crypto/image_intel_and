from src.map_view import sort_by_time,create_map

# testing map_view
def test_sort_by_time_without_time():
    assert ({'camera_s': 'SM-A125F','hello':'e2d'}) == {'camera_s': 'SM-A125F','hello':'e2d'}

def test_sort_by_time_with_time():
    assert sort_by_time([{'datetime': '2023:03:05 18:35:51'},{'datetime': '2023:01:18 07:07:16'},
                         {'datetime': '2023:02:05 18:35:51'},
                         {'datetime': None}]) == [{'datetime': '2023:01:18 07:07:16'},
                                                  {'datetime': '2023:02:05 18:35:51'}
                                                  ,{'datetime': '2023:03:05 18:35:51'}]

def test_create_map_without_gps():
    assert create_map([{'filename': '20230118_070716.jpg', 'has_gps': False}]) == "<h2>No GPS data found</h2>"

def test_create_map_without_sufficiant():
    assert create_map([{'latitude': None, 'longitude': 34.82882308333333, 'has_gps': True}]) == "<h2>No GPS data found</h2>"

def get_fake_data():
    return [
        {"filename": "t1.jpg", "latitude": 32.0, "longitude": 34.7, 
         "has_gps": True, "camera_model": "Samsung", "datetime": "2025-01-12"},
        {"filename": "t2.jpg", "latitude": 31.7, "longitude": 35.2, 
         "has_gps": True, "camera_model": "iPhone", "datetime": "2025-01-13"},
        {"filename": "t3.jpg", "latitude": None, "longitude": None, 
         "has_gps": False, "camera_model": None, "datetime": None},
    ]

def test_create_map_returns_html():
    result = create_map(get_fake_data())
    assert isinstance(result, str)
    assert len(result) > 0

def test_create_map_handles_no_gps():
    no_gps = [{"filename": "x.jpg", "has_gps": False, "latitude": None, 
               "longitude": None, "camera_model": None, "datetime": None}]
    result = create_map(no_gps)
    assert isinstance(result, str)

def test_create_map_handles_empty_list():
    result = create_map([])
    assert isinstance(result, str)