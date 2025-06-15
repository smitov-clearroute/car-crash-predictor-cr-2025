import { BeakerIcon } from "@heroicons/react/16/solid"


interface OilTemperatureProps {
    temperature: number
  }

export default function OilTemperature({temperature}: OilTemperatureProps) {

    const getTextColor = (temp: number) => {
        if (temp > 120) return "text-red-600"
        if (temp > 100) return "text-orange-500"
        return "text-gray-900"
      }


  return (
    <div className="flex flex-col items-center justify-center w-[200px] md:w-[300px] lg:w-[400px] h-[200px] rounded-lg border-[1px] border-gray-300 bg-white">
        <BeakerIcon className="w-8 h-8 text-gray-600" />
      <div className={`text-3xl font-bold ${getTextColor(temperature)}`}>{temperature}</div>
      <div className="text-sm text-gray-500">Oil °C</div>

    </div>
  )
}
