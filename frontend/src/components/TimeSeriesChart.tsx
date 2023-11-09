import React from 'react';
import ReactApexChart from 'react-apexcharts';
import { ApexOptions } from 'apexcharts';


interface Props {
  visitorsData: {x: Date, y: number}[];
}


const TimeSeriesChart: React.FC<Props> = ({ visitorsData }) => {
  const options: ApexOptions = {
    chart: {
      type: 'area',
      height: 350,
      width:'100%'
    },
    title: {
      text: 'Number of Visitors per day',
      align: 'center',
      style: {
        fontSize: '24px',
      }
    },
    yaxis: {
      title: {
        text: 'No of Visitors',
      },
    },
    xaxis: {
      type: 'datetime',
    },
  };

  const series = [
    {
      name: 'Visitors',
      data: visitorsData,
    },
  ];

  return (
    <ReactApexChart options={options} series={series} type="area" height={350} width='100%'/>
  );
};

export default TimeSeriesChart;
