import { useState } from "react";
import { fetchData } from "../action/FetchData";
import { columns } from "../util/columns";
import Columns from "./Columns";
import Modal from "./Modal";

export default function CarDetails() {
  const { data, error, isLoading } = fetchData();
  const [modalData, setModalData] = useState<{ rowIndex: number; car: typeof data[0] } | null>(null);

  const handleRowClick = (rowIndex: number, car: typeof data[0]) => {
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
    <div className="w-full overflow-x-auto relative"> {/* Added overflow-x-auto */}
      <table className="table-auto w-full text-gray-400">
        <Columns />
        <tbody>
          {data?.map((car, rowIndex) => (
            <tr
              key={rowIndex}
              className={`hover:bg-gray-600 ${
                rowIndex % 2 === 0 ? "bg-gray-800" : "bg-gray-700"
              } cursor-pointer relative`}
              onClick={() => handleRowClick(rowIndex, car)}
            >
              {columns.map((col, colIndex) => (
                <td
                  key={colIndex}
                  className="px-4 py-2 text-center"
                  style={{ minWidth: col.width }}
                >
                  {col.key === "pic" ? (
                    <img
                      src={car[col.key]}
                      alt={car.driver}
                      className="h-8 w-8 rounded-full mx-auto"
                    />
                  ) : (
                    car[col.key as keyof typeof car]
                  )}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      <Modal modalData={modalData}  closeModal={closeModal} />
    </div>
  );
}
