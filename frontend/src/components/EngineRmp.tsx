import { CogIcon } from "@heroicons/react/24/outline"

interface EngineRpmProps {
  rpm: number
}

export function EngineRpm({ rpm }: EngineRpmProps) {
  return (
    <div className="flex flex-col items-center justify-center w-[200px] md:w-[300px] lg:w-[400px] h-[200px] rounded-lg border-[1px] border-gray-300 bg-white">
        <h1 className="uppercase text-center font-bold text-gray-700 text-sm">Engine RPM</h1>
       <CogIcon className="w-8 h-8 text-gray-600" />
      <div className="text-3xl font-bold text-gray-900">{rpm}</div>
      <div className="text-sm text-gray-500">rpm</div>

    </div>
  )
}
