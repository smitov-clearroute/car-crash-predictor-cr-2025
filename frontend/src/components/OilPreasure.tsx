import { CircularProgress } from "./ui/circular-progress"

interface OilPressureProps {
    pressure: number
  }

export default function OilPreasure({pressure}: OilPressureProps) {

const getColor = (pressure: number) => {
        if (pressure < 20) return "#ef4444"
        if (pressure < 30) return "#f59e0b"
        return "#22c55e"
      }


  return (
    <div className="flex flex-col items-center justify-center w-[200px] md:w-[300px] lg:w-[400px] h-[200px] rounded-lg border-[1px] border-gray-300 bg-white">
        <h1 className="uppercase text-center font-bold text-gray-700 text-sm">Oil Preasure</h1>
        <CircularProgress value={pressure} maxValue={80} color={getColor(pressure)} showPercentage={false} />
      {/* <div className="text-sm text-gray-500">psi</div> */}

    </div>
  )
}
