import React from 'react'

export default function Gsr({gsr} : {gsr: number}) {
    const radius = 45;
    const circumference = 2 * Math.PI * radius;
    const strokeDashOffset = circumference - (gsr / 1) * circumference;

    return (
      <div className="flex flex-col items-center justify-center w-[200px] md:w-[300px] lg:w-[400px] h-[200px] rounded-lg border-[1px] border-gray-300 bg-white">
        <h1 className="uppercase text-center font-bold text-gray-700 text-sm">GSR Stress</h1>
        <div className="relative">
          <svg width="100" height="100">
            <circle
              cx="50"
              cy="50"
              r={radius}
              className="stroke-current text-gray-300"
              strokeWidth="8"
              fill="none"
            />
            <circle
              cx="50"
              cy="50"
              r={radius}
              className="stroke-current text-gray-500 transform -rotate-90"
              strokeWidth="8"
              fill="none"
              strokeDasharray={circumference}
              strokeDashoffset={strokeDashOffset}
              strokeLinecap="round"
            />
            <text
              x="50"
              y="50"
              className="text-gray-700 font-bold text-xl"
              textAnchor="middle"
              dominantBaseline="middle"
            >
              {gsr.toFixed(2)}
            </text>
          </svg>
        </div>
      </div>
  )
}
