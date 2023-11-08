from sqlalchemy import Column, Integer, String
from database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)
    hotel = Column(String)
    arrival_date = Column(String)
    adults = Column(Integer)
    children = Column(Integer)
    babies = Column(Integer)
    country = Column(String)