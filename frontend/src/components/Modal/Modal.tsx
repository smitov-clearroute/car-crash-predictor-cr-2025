
import type { Car } from "../../util/carType";
import CarModal from "./CarModal";
import DriverModal from "./DriverModal";

interface ModalProps {
  modalData: { car: Car } | null;
  closeModal: () => void;
}

const Modal = ({ modalData, closeModal }: ModalProps) => {
  if (!modalData || !modalData.car) {
    return null;
  }


  return (
    <div
      className="fixed top-0 overflow-x-scroll left-0 w-full h-full flex items-center justify-center bg-black bg-opacity-50 z-50"
      onClick={closeModal}
    >
      <div
        className="bg-white rounded-lg h-full flex flex-col items-center  md:h-[90%] w-2/3 md:w-2/3 p-8 mx-auto"
        onClick={(e) => e.stopPropagation()}
      >
        <h2 className="text-xl flex flex-col text-center font-bold mb-4 text-gray-800">
          Driver: {modalData.car.driver_data.driver_name}
            <span className="text-gray-600  text/-sm">{modalData.car.driver_data.car_name}</span>
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <DriverModal carData={modalData.car} />
        <CarModal carData={modalData.car} />
        </div>
      <div className="flex">
          <button
            className=" px-4  py-2 bg-black text-white rounded hover:bg-gray-600 transition-colors duration-300"
            onClick={closeModal}
          >
            Close
          </button>
          </div>
      </div>
    </div>
  );
};

export default Modal;
