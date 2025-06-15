import { CircularProgress } from "./ui/circular-progress"


interface CoolantTemperatureProps {
    temperature: number
  }


export default function CoolantTemperature({temperature}: CoolantTemperatureProps) {

    const getColor = (temp: number) => {
        if (temp > 100) return "#ef4444"
        if (temp > 90) return "#f59e0b"
        return "#60a5fa"
      }

  return (
    <div className="flex flex-col items-center justify-center w-[200px] md:w-[300px] lg:w-[400px] h-[200px] rounded-lg border-[1px] border-gray-300 bg-white">
       <CircularProgress value={temperature} maxValue={120} color={getColor(temperature)} showPercentage={false} />
       <div className="text-sm text-gray-500">Coolant °C</div>
    </div>
  )
}
