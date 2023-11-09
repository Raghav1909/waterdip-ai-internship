from fastapi import FastAPI
from database import engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, HTTPException, status, Response
import models, csv
from datetime import datetime, timedelta
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

        bookings = []
        for row in reader:
            if int(row[3]) < 10:
                row[3] = "0" + row[3]
            
            month = str(months[row[2]])
            if int(month) < 10:
                month = "0" + month

            date = row[1] + "-" + month + "-" + row[3]

            booking = models.Booking(
                hotel=row[0],
                arrival_date = date,
                adults=row[4],
                children=row[5],
                babies=row[6],
                country=row[7]
            )
            bookings.append(booking)

        db.add_all(bookings)
        db.commit()

    return Response(status_code=status.HTTP_200_OK)


@app.get("/visitors")
def get_total_visitors_in_range(start_date: str = "2015-07-01", end_date: str = "2015-08-09", db: Session = Depends(get_db)):
    start_year, start_month, start_day = list(map(int,start_date.split('-')))
    start_date = datetime(start_year, start_month, start_day).date()
    
    end_year, end_month, end_day = list(map(int,end_date.split('-')))
    end_date = datetime(end_year, end_month, end_day).date()

    if start_date < datetime(2015, 7, 1).date():
        start_date = datetime(2015, 7, 1).date()
    
    if end_date > datetime(2015, 8, 9).date():
        end_date = datetime(2015, 8, 9).date()
    
    if start_date > end_date:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Start date cannot be greater than end date")
    
    current_date = start_date

    adults, children, babies, total = [], [], [], []

    while current_date <= end_date:
        total_adults, total_children, total_babies, total_people = 0, 0, 0, 0
        bookings = db.query(models.Booking).filter(models.Booking.arrival_date == current_date.strftime("%Y-%m-%d")).all()
        
        
        for i in range(len(bookings)):
            booking = bookings[i]
            total_people += booking.adults + booking.children + booking.babies
            total_adults += booking.adults
            total_children += booking.children
            total_babies += booking.babies
        

        adults.append(total_adults)
        children.append(total_children)
        babies.append(total_babies)
        total.append({
            "x": current_date,
            "y": total_people
        })
        current_date += timedelta(days=1)

    return {
        "adults": adults,
        "children": children,
        "babies": babies,
        "total": total
    }
    

class VisitorsByCountry(BaseModel):
    countries: list[str]
    visitorPercentage: list[float]


@app.get("/visitors/country", response_model=VisitorsByCountry)
def get_visitors_by_country(start_date: str = "2015-07-01", end_date: str = "2015-08-09", db: Session = Depends(get_db)):
    start_year, start_month, start_day = list(map(int,start_date.split('-')))
    start_date = datetime(start_year, start_month, start_day).date()
    
    end_year, end_month, end_day = list(map(int,end_date.split('-')))
    end_date = datetime(end_year, end_month, end_day).date()

    if start_date < datetime(2015, 7, 1).date():
        start_date = datetime(2015, 7, 1).date()
    
    if end_date > datetime(2015, 8, 9).date():
        end_date = datetime(2015, 8, 9).date()
    
    if start_date > end_date:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Start date cannot be greater than end date")
    
    current_date = start_date

    total_visitors_by_country = {}

    while current_date <= end_date:
        total_people = 0
        bookings = db.query(models.Booking).filter(models.Booking.arrival_date == current_date.strftime("%Y-%m-%d")).all()
        
        for i in range(len(bookings)):
            booking = bookings[i]
            total_visitors_by_country[booking.country] = total_visitors_by_country.get(booking.country, 0) + booking.adults + booking.children + booking.babies
    
        current_date += timedelta(days=1)

    total_visitors = sum(total_visitors_by_country.values())
    countries = list(total_visitors_by_country.keys())
    percentage_of_visitors = []
    for country in countries:
        percentage_of_visitors.append(round(total_visitors_by_country[country] / total_visitors * 100, 1))

    for country in total_visitors_by_country:
        total_visitors_by_country[country] = total_visitors_by_country[country] / total_visitors
    
    return VisitorsByCountry(
        countries=countries,
        visitorPercentage=percentage_of_visitors
    )