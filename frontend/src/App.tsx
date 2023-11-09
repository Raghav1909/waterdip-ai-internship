import { useEffect, useState } from "react";
import TimeSeriesChart from "./components/TimeSeriesChart";
import SparkLineChart from "./components/SparkLineChart";
import ColumnChart from "./components/ColumnChart";
import DatePicker from 'react-datepicker';
import "react-datepicker/dist/react-datepicker.css";

import './app.css'

export default function App() {
  const [startDate, setStartDate] = useState('2015-07-01')
  const [endDate, setEndDate] = useState('2015-08-09')
  
  const [totalVisitors, setTotalVisitors] = useState<any[]>([])
  const [totalAdults, setTotalAdults] = useState<any[]>([])
  const [totalChildren, setTotalChildren] = useState<any[]>([])

  const [countries, setCountries] = useState<string[]>([])
  const [visitorPercentage, setVisitorPercentage] = useState<number[]>([])

  const fetchTotalPeople = async () => {
    try{
      const response = await fetch(`${process.env.REACT_APP_API_URL}/visitors?start_date=${startDate}&end_date=${endDate}`);
      const data = await response.json();
      setTotalVisitors(data.total);
      setTotalAdults(data.adults);
      setTotalChildren(data.children);
    }
    catch(error){
      console.error('Error fetching data', error);
      alert('Error fetching data');
    }
  }

  const fetchCountries = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/visitors/country?start_date=${startDate}&end_date=${endDate}`);
      
      if(response.status === 400){
        alert('Date out of range!');
        window.location.reload()
        return
      }
      if(response.ok){
        const data = await response.json();
        setCountries(data.countries);
        setVisitorPercentage(data.visitorPercentage);
      }
      
    } catch (error) {
      console.error('Error fetching data', error);
      alert('Error fetching data');
    }
  };

  useEffect(() => {
    fetchCountries();
    fetchTotalPeople();
  }, [startDate, endDate]);

  return (
    <div className = "container">
      <h1>Waterdip Internship Assignment</h1>
      <div className="date-container">
        <div className="date-picker">
          <p>Start Date: {startDate}</p>
          <DatePicker
            selected = {new Date(startDate)}
            onChange={(date: Date) => setStartDate(date.toISOString().split('T')[0])}/>
        </div>
        <div className="date-picker">
          <p>End Date: {endDate}</p>
          <DatePicker
            selected = {new Date(endDate)}
            onChange={(date: Date) => setEndDate(date.toISOString().split('T')[0])}/>
        </div>
      </div>
      <div><TimeSeriesChart visitorsData = {totalVisitors}/></div>
      <div><ColumnChart countries={countries} visitorPercentage={visitorPercentage}/></div>
      <div className="sparkline">
        <SparkLineChart
          name = "Adults"
          data = {totalAdults}/>
        <SparkLineChart
          name = "Children"
          data = {totalChildren}/>
      </div>
    </div>
  )
}
