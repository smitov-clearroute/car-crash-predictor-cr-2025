export default function TrackVisualization() {
  return (
        <div className="bg-black text-white p-4 h-[300px] md:h-screen flex flex-col items-center">
      <div className="flex justify-between w-full max-w-md mb-4 text-xs md:text-base">
        <div className="text-center">
          <div className="opacity-50">ELAPSED</div>
          <div className="font-bold">04:02:36</div>
        </div>
        <div className="text-center">
          <div className="opacity-50">REMAINING</div>
          <div className="font-bold">19:57:24</div>
        </div>
      </div>

      <svg
        width="400"
        height="600"
        viewBox="0 0 400 600"
        xmlns="http://www.w3.org/2000/svg"
      >

        <path
          d="M100 500 Q80 450 100 400 Q120 350 100 300 Q80 250 120 200 Q140 180 180 150 Q220 120 250 100 Q300 80 350 100 Q370 120 360 150 Q350 200 340 250 Q330 300 320 350 Q310 400 300 450 Q290 500 250 520 Q200 540 150 520 Q120 510 100 500 Z"
          fill="none"
          stroke="#e11d48"
          strokeWidth="4"
        />

        {/* Start/Finish Line */}
        <rect x="98" y="495" width="4" height="10" fill="#fff" />

        {/* Position marker 6 (Red) */}
        <circle cx="100" cy="500" r="12" fill="#e11d48" />
        <text
          x="100"
          y="504"
          textAnchor="middle"
          fill="#fff"
          fontSize="10"
          fontWeight="bold"
        >
          6
        </text>

        {/* Position marker 57 (Green) */}
        <circle cx="340" cy="250" r="12" fill="#22c55e" />
        <text
          x="340"
          y="254"
          textAnchor="middle"
          fill="#fff"
          fontSize="10"
          fontWeight="bold"
        >
          57
        </text>
      </svg>
    </div>

  )
}
