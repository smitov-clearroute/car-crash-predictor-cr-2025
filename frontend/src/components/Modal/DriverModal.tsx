
import Crashprobability from '../Crashprobability';
import BlinkRate from '../BlinkRate';
import Gsr from '../Gsr';
import Heartrate from '../Heartrate';

type CarModalProps = {
  carData: {
    driver_data: {
      Pic: number;
      car_name: string;
      laps: number;
      last_lap: number;
      best_lap: number;
      gap: number;
      pits: number;
      max_speed: number;
      driver_name: string;
      race_time: string;
      status: string;
      pit_time_remaining: number;
      next_pit_in: number;
    };
    data: {
      engine_rpm: number;
      brake_pedal_pressure: number;
      brake_disc_temp_FL: number;
      brake_disc_temp_FR: number;
      brake_disc_temp_RL: number;
      brake_disc_temp_RR: number;
      tire_temp_FL: number;
      tire_pressure_FL: number;
      tire_temp_FR: number;
      tire_pressure_FR: number;
      tire_temp_RL: number;
      tire_pressure_RL: number;
      tire_temp_RR: number;
      tire_pressure_RR: number;
      tire_wear_rate: number;
      coolant_temperature: number;
      coolant_pressure: number;
      oil_temperature: number;
      oil_level: number;
      heart_rate: number;
      gsr: number;
      pupil_dilation: number;
      blink_rate: number;
      track_temperature: number;
      rainfall_intensity: number;
      ambient_light: number;
    };
    risk: number;
  };
};

export default function CarModal({ carData }: CarModalProps) {
  return (
    <div className="text-gray-700 flex flex-col gap-y-2 h-[95%] md:h-[90%] md:w-full lg:w-[80%]">
      <Crashprobability crashProbability={carData.risk} />
      <Heartrate heartRate={carData.data.heart_rate} />
      <Gsr gsr={carData.data.gsr} />
      <BlinkRate blinkRate={carData.data.blink_rate} />
    </div>
  );
}
