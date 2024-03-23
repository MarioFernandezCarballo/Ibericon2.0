from database import City

def getCities():
    return City.query.order_by(City.name).all()