import LeMansRace from '../../static/LeMansRace';

export default function TrackVisualization() {

  return (
    <div className="bg-black text-white p-4 h-[600px] md:h-screen flex flex-col items-center">
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
      <LeMansRace />
    </div>
  );
}
