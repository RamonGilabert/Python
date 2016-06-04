from sqlalchemy import Column, Integer, String, Float
from connection import Base

class Temperature(Base):
    __tablename__ = 'Tempreatures'

    # sensor_id needs to be unique in order for the sensor to be created.
    id = Column(Integer, primary_key=True, autoincrement=True)
    sensor_id = Column(String(120), unique=True)
    mean_temperature = Column(Float)

    def __init__(self, sensor_id=None, mean_temperature=None):
        self.sensor_id = sensor_id
        self.mean_temperature = mean_temperature

    def __repr__(self):
        return '<Temperature %r>' % (self.mean_temperature)

    # Serialize returns and object with the self instance.
    def serialize(self):
        return {
            'id': self.id,
            'sensor_id': self.sensor_id,
            'mean_temperature': self.mean_temperature
        }
