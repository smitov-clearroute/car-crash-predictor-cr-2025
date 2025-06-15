interface CircularProgressProps {
    value: number
    maxValue?: number
    size?: number
    strokeWidth?: number
    color?: string
    showPercentage?: boolean
  }

  export function CircularProgress({
    value,
    maxValue = 100,
    size = 120,
    strokeWidth = 8,
    color = "#60a5fa",
    showPercentage = true,
  }: CircularProgressProps) {
    const radius = (size - strokeWidth) / 2
    const circumference = radius * 2 * Math.PI
    const progress = (value / maxValue) * circumference

    return (
      <div className="relative inline-flex items-center justify-center">
        <svg width={size} height={size} className="transform -rotate-90">
          <circle cx={size / 2} cy={size / 2} r={radius} stroke="#e5e7eb" strokeWidth={strokeWidth} fill="none" />
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke={color}
            strokeWidth={strokeWidth}
            fill="none"
            strokeDasharray={circumference}
            strokeDashoffset={circumference - progress}
            strokeLinecap="round"
          />
        </svg>
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-2xl font-bold text-gray-900">
            {value}
            {showPercentage && maxValue === 100 ? "%" : ""}
          </span>
        </div>
      </div>
    )
  }
