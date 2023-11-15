from database import City

def getCities():
    return City.query.all()