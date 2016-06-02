from sqlalchemy import Column, Integer, String
from connection import Base

class Temperature(Base):
    __tablename__ = 'Tempreatures'

    id = Column(Integer, primary_key=True)
    sensor_id = Column(String(120), unique=True)
    mean_temperature = Column(Float)

    def __init__(self, sensor_id=None, mean_temperature=None):
        self.sensor_id = sensor_id
        self.mean_temperature = mean_temperature

    def __repr__(self):
        return '<Temperature %r>' % (self.mean_temperature)
