
import Crashprobability from '../Crashprobability'
import BlinkRate from '../BlinkRate'
import Gsr from '../Gsr'
import Heartrate from '../Heartrate'

export default function DriverModal() {
  return (
    <div className="text-gray-700 flex flex-col gap-y-2 h-[95%] md:h-[90%] md:w-full lg:w-[80%]">
    <Crashprobability crashProbability={0} />
    <Heartrate heartRate={0}/>
    <Gsr gsr={20}/>
    <BlinkRate blinkRate={0}/>
  </div>
)

}
