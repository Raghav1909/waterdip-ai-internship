import { useEffect, useState } from "react";
import TimeSeriesChart from "./components/TimeSeriesChart";
import SparkLineChart from "./components/SparkLineChart";
import DatePicker from 'react-datepicker';
import "react-datepicker/dist/react-datepicker.css";

import './app.css'

export default function App() {
  const [visitorsPerDay, setVisitorsPerDay] = useState<any[]>([])
  const [startDate, setStartDate] = useState('2015-07-01')
  const [endDate, setEndDate] = useState('2015-08-09')

  const [totalVisitors, setTotalVisitors] = useState<any[]>([])
  const [totalAdults, setTotalAdults] = useState<any[]>([])
  const [totalChildren, setTotalChildren] = useState<any[]>([])


  useEffect(() => {
    let fetchData = async() => {
      try{
        const response = await fetch(`${process.env.REACT_APP_API_URL}/visitors/total?startDate=${startDate}&endDate=${endDate}`)
        const data = await response.json()
        setVisitorsPerDay(data)
      }
      catch(error){
        console.error('Error fetching data', error)
        alert('Error fetching data')
      }
    }
    fetchData()
  }, [startDate, endDate])

  useEffect(() => {
    setTotalVisitors(() => Array.from(visitorsPerDay, (item) => ({
    x: new Date(item.date),
    y: item.total
  })))

    setTotalAdults(() => Array.from(visitorsPerDay, item => item.adults))
    setTotalChildren(() => Array.from(visitorsPerDay, item => item.children))  
  }, [visitorsPerDay])
  

  return (
    <div className = "container">
      <div><h1>Waterdip Internship Assignment</h1></div>
      <div>
        <DatePicker
          selected = {new Date(startDate)}
          onChange={(date: Date) => setStartDate(date.toISOString().split('T')[0])}/>
        <DatePicker
          selected = {new Date(endDate)}
          onChange={(date: Date) => setEndDate(date.toISOString().split('T')[0])}/>
      </div>
      <div>
        <TimeSeriesChart visitorsData = {totalVisitors}/>
      </div>
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
