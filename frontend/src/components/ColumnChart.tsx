import ReactApexChart from "react-apexcharts";
import { ApexOptions } from 'apexcharts';


interface Props{
	countries: string[],
	visitorPercentage: number[]
}

const ColumnChart: React.FC<Props> = ({countries, visitorPercentage}) => {
	const options: ApexOptions = {
		chart: {
				type: 'bar',
				height: 350,
				width:'100%'
		},
		plotOptions: {
		bar: {
			borderRadius: 10,
			dataLabels: {
				position: 'top', // top, center, bottom
				},
			}
		},
		dataLabels: {
			enabled: true,
			offsetY: -20,
			formatter: function (val) {
				return val + "%";
			},
			style: {
				fontSize: '12px',
				colors: ["#304758"]
			}
		},
		title: {
			text: 'Total Visitors',
			align: 'center',
			style: {
				fontSize: '24px',
				}
		},
		xaxis: {
			categories: countries,
			position: 'top',
			axisBorder: {
				show: false
			},
			axisTicks: {
				show: false
			},
			crosshairs: {
				fill: {
					type: 'gradient',
					gradient: {
						colorFrom: '#D8E3F0',
						colorTo: '#BED1E6',
						stops: [0, 100],
						opacityFrom: 0.4,
						opacityTo: 0.5,
					}
				}
			},
			tooltip: {
				enabled: true,
			}
		},
		yaxis: {
			axisBorder: {
				show: false
			},
			axisTicks: {
				show: false,
			},
		},
	}
    
	const series = [
		{
			name: 'visitors',
			data: visitorPercentage
		}
  ]

	return (
		<>
			<ReactApexChart options={options} series={series} type="bar" height={350} />
		</>
	)
}

export default ColumnChart;