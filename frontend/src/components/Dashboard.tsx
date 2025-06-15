import CarDetails from "./CarDetails";
import TrackVisualization from "./TrackVisualization";

export default function Dashboard() {
  return (
    <div className="flex flex-col md:flex-row lg:flex-row w-full bg-black">
      <div className="w-full md:w-[40%] h-[800px] md:h-screen">
        <TrackVisualization />
      </div>
      <div className="w-full md:w-[60%] flex flex-col h-screen">
        <CarDetails />
      </div>

    </div>
  );
}
