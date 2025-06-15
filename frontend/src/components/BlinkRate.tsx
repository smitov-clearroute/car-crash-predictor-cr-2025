import { EyeIcon } from '@heroicons/react/24/outline';



const BlinkRate =({ blinkRate } : {blinkRate : number}) => {

  return (
    <div className="flex flex-col items-center justify-center w-[200px] md:w-[300px] lg:w-[400px] h-[200px] rounded-lg border-[1px] border-gray-300 bg-white">
      <h1 className="uppercase text-center font-bold text-gray-700 text-sm">Blink Rate</h1>
      <div className="flex items-center">
        <EyeIcon className="h-12 w-12 text-gray-700 mr-2" />
        <div className="text-gray-700">
          <div className="text-3xl font-bold">{blinkRate}</div>
          <div>blinks/min</div>
        </div>
      </div>
    </div>
  );
};

export default BlinkRate;
