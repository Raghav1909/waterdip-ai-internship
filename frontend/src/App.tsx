import { useEffect, useState } from "react";
import TimeSeriesChart from "./components/TimeSeriesChart";

import './app.css'

export default function App() {
  const [visitorsPerDay, setVisitorsPerDay] = useState<any[]>([])
  const [startDate, setStartDate] = useState('2015-07-01')
  const[endDate, setEndDate] = useState('2015-08-09')

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
  
  let totalVisitors: any = Array.from(visitorsPerDay, (item) => ({
    x: new Date(item.date),
    y: item.total
  }))

  return (
    <div className = "container">
      <h1>Waterdip Internship Assignment</h1>
      <TimeSeriesChart visitorsData = {totalVisitors}/>
    </div>
  )
}
