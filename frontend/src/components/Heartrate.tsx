import { HeartIcon } from '@heroicons/react/24/outline';


export default function Heartrate({heartRate} : {heartRate: number}) {
  return (
    <div className="flex flex-col items-center justify-center w-[200px] md:w-[300px] lg:w-[400px] h-[200px] rounded-lg border-[1px] border-gray-300 bg-white">
    <h1 className="uppercase text-center font-bold text-gray-700 text-sm">Heart Rate</h1>
    <div className="flex items-center">
      <HeartIcon className="h-12 w-12 text-gray-700 mr-2" />
      <div className="text-gray-700">
        <div className="text-3xl font-bold">{heartRate}</div>
        <div>bpm</div>
      </div>
    </div>
  </div>
  )
}
