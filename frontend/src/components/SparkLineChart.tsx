import ReactApexChart from "react-apexcharts";
import { ApexOptions } from 'apexcharts';

interface Props {
  name: string
  data: number[]
}

const SparkLineChart: React.FC<Props> = ({name, data}) => {
  const options: ApexOptions = {
    chart: {
      type: 'line',
      height: 350,
      width:'100%',
      sparkline: {
        enabled: true
      },
    },
    stroke: {
      curve: 'straight'
    },
    fill: {
      opacity: 0.3
    },
    title: {
      text: `Total ${name}: ${data.reduce((acc, curr) => acc + curr, 0)}`,
      style: {
        fontSize: '24px',
      }
    }

  }

  const series = [
    {
      name: name,
      data: data
    }
  ]
  
  return (
    <>
      <ReactApexChart
        options = {options}
        series={series}
        type="line"
        width={'100%'}
        height={350}/>
    </>
  );
}

export default SparkLineChart;