
def datatime(data: dict):
    if type(data)== dict:
        return data["DateTime"]
    else:
        return None
    
def camera_make(data: dict):
    if type(data)== dict:
        return data["Make"]
    else:
        return None
    
def camera_model(data: dict):
    if type(data)== dict:
        return data["Model"]
    else:
        return None