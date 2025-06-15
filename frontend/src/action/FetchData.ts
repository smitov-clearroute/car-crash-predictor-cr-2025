import { useQuery } from "@tanstack/react-query";

type DriverData = {
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

type DataValues = {
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
}

type Data = {
  driver_data: DriverData;
  data: DataValues;
  risk: number;
};


export const fetchData = () => {
  // eslint-disable-next-line react-hooks/rules-of-hooks
  return useQuery({
    queryKey: ["carData"],
    queryFn: async () => {
      try {
        const response = await fetch("https://c995-79-110-121-2.ngrok-free.app/stats", {
          mode: 'cors',
          headers: {
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          console.error(`HTTP error! status: ${response.status}`);
          const errorText = await response.text();
          console.error('Response text:', errorText);
          throw new Error(`HTTP error! status: ${response.status}, response: ${errorText}`);
        }

        const text = await response.text();
        try {
          const data = JSON.parse(text);
          return data as Data[];
        } catch (jsonError) {
          console.error('JSON parse error:', jsonError);
          console.error('Response text:', text);
          const errorMessage = jsonError instanceof Error ? jsonError.message : 'Unknown error';
          throw new Error(`Failed to parse JSON: ${errorMessage}, response: ${text}`);
        }
      } catch (error: any) {
        console.error('Fetch error:', error);
        throw new Error(`Failed to fetch data: ${error.message}`);
      }
    },
    refetchInterval: 1000,
  });
};
