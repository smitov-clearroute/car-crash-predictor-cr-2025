import { useState } from "react";
import { fetchData } from "../action/FetchData";
import { columns } from "../util/columns";
import Columns from "./Columns";
import Modal from "./Modal/Modal";

type Car = {
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

export default function CarDetails() {
  const { data, error, isLoading } = fetchData();
  const [modalData, setModalData] = useState<{ rowIndex: number; car: Car } | null>(null);

  const handleRowClick = (rowIndex: number, car: Car) => {
    setModalData({ rowIndex, car });
  };

  const closeModal = () => {
    setModalData(null);
  };

  if (isLoading)
    return <div className="text-center text-white">Loading...</div>;
  if (error)
    return <div className="text-center text-red-500">Error: {error.message}</div>;

  if (!Array.isArray(data)) {
    return <div className="text-center text-red-500">Data is not an array</div>;
  }

  return (
    <div className="w-full overflow-x-auto relative">
      <table className="table-auto w-full text-white">
        <Columns />
        <tbody>
          {data.map((car, rowIndex) => (
            <tr
              key={rowIndex}
              className={`hover:bg-gray-600 ${
                rowIndex % 2 === 0 ? "bg-gray-800" : "bg-black"
              } cursor-pointer relative`}
              onClick={() => handleRowClick(rowIndex, car)}
            >
              {columns.map((col, colIndex) => {
                let cellContent;
                if (col.key === "teamDriver") {
                  cellContent = (
                    <div>
                      <div>{car.driver_data.car_name}</div>
                      <div className="text-gray-400">{car.driver_data.driver_name}</div>
                    </div>
                  );
                } else {
                  // Use the original data for other columns
                  cellContent = car.driver_data[col.key as keyof typeof car["driver_data"]];
                }

                return (
                  <td
                    key={colIndex}
                    className="px-4 py-2 text-center"
                    style={{ minWidth: col.width }}
                  >
                    {cellContent !== undefined && cellContent !== null ? cellContent.toString() : ''}
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
      <Modal modalData={modalData} closeModal={closeModal} />
    </div>
  );
}
