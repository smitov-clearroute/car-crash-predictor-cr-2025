import React from 'react';

interface CrashprobabilityProps {
  crashProbability: number;
}

const Crashprobability: React.FC<CrashprobabilityProps> = ({ crashProbability }) => {
  const radius = 45;
  const circumference = 2 * Math.PI * radius;


  return (
    <div className="flex flex-col items-center justify-center w-[200px] md:w-[250px] lg:w-[300px] xl:w-[400px]  h-[200px] rounded-lg border-[1px] border-gray-300 bg-white">
      <h1 className="uppercase text-center font-bold text-gray-700 text-sm">Crash Probability</h1>
      <div className="relative">
        <svg width="100" height="100">
          <circle
            cx="50"
            cy="50"
            r={radius}
            className="stroke-current text-blue-300"
            strokeWidth="8"
            fill="none"
          />
          <circle
            cx="50"
            cy="50"
            r={radius}
            className="stroke-current text-blue-500 transform -rotate-90"
            strokeWidth="8"
            fill="none"
            strokeDasharray={circumference}
            strokeDashoffset={(1 - crashProbability / 100) * circumference}
            strokeLinecap="round"
          />
          <text
            x="50"
            y="50"
            className="text-gray-700 font-bold text-xl"
            textAnchor="middle"
            dominantBaseline="middle"
          >
            {crashProbability}%
          </text>
        </svg>
      </div>
    </div>
  );
};

export default Crashprobability;
