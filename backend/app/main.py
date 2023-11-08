from fastapi import FastAPI
from database import engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, HTTPException, status, Response
import models, csv
from datetime import datetime
from sqlalchemy.orm import Session
from database import get_db
from pydantic import BaseModel

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/initDB", status_code=status.HTTP_200_OK)
def initialize_database(db:  Session = Depends(get_db)):
    months = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}

    with open('../hotel_bookings_1000.csv') as csvfile:
        header = next(csvfile)
        reader = csv.reader(csvfile)

        hotels = []
        for row in reader:
            if int(row[3]) < 10:
                row[3] = "0" + row[3]
            
            month = str(months[row[2]])
            if int(month) < 10:
                month = "0" + month

            date = row[1] + "-" + month + "-" + row[3]

            hotel = models.Hotel(
                hotel=row[0],
                arrival_date = date,
                adults=row[4],
                children=row[5],
                babies=row[6],
                country=row[7]
            )
            hotels.append(hotel)

        db.add_all(hotels)
        db.commit()

    return Response(status_code=status.HTTP_200_OK)



# Schema
class Hotel(BaseModel):
    hotel: str
    arrival_date: str
    adults: int
    children: int
    babies: int
    country: str

@app.get("/hotels", response_model=list[Hotel])
def get_hotels_by_date_range(start_date: str = "2015-07-01", end_date: str = "2015-08-09", db: Session = Depends(get_db)):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    hotels = db.query(models.Hotel).filter(models.Hotel.arrival_date.between(start_date, end_date)).all()
    return hotels

