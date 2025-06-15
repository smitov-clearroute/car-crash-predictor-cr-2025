import { useState } from "react";
import { fetchData } from "../action/FetchData";
import { columns } from "../util/columns";
import Columns from "./Columns";
import Modal from "./Modal/Modal";
import type { Car } from "../util/carType";

export default function CarDetails() {
  const { data, error, isLoading } = fetchData() as unknown as { data: Car[] | null; error: Error | null; isLoading: boolean };
  const [modalData, setModalData] = useState<{ rowIndex: number; car: NonNullable<typeof data>[0] } | null>(null);

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

  return (
    <div className="w-full overflow-x-auto relative">
      <table className="table-auto w-full text-white">
        <Columns />
        <tbody>
          {data?.map((car, rowIndex) => (
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
                      <div>{car.team}</div>
                      <div className="text-gray-400">{car.driver}</div>
                    </div>
                  );
                } else {
                  // Use the original data for other columns
                  cellContent = car[col.key as keyof Car];
                }

                return (
                  <td
                    key={colIndex}
                    className="px-4 py-2 text-center"
                    style={{ minWidth: col.width }}
                  >
                    {cellContent}
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
