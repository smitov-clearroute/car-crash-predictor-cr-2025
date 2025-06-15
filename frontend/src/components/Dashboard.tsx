import CarDetails from "./CarDetails";
import Columns from "./Columns";

import TrackVisualization from "./TrackVisualization";

export default function Dashboard() {
  return (
    <div className="flex flex-col md:flex-row lg:flex-row w-full bg-black">
      <div className="w-full md:w-[40%] h-[300px] md:h-screen">
        <TrackVisualization />
      </div>
      <div className="w-full md:w-[60%] overflow-x-auto flex flex-col h-screen">
        <CarDetails />
      </div>
    </div>
  );
}
