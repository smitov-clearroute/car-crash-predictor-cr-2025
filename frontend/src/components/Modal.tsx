
import Crashprobability from "./Crashprobability";
import type { Car } from "../util/carType";
import Heartrate from "./Heartrate";
import Gsr from "./Gsr";
import BlinkRate from "./BlinkRate";

interface ModalProps {
  modalData: { rowIndex: number; car: Car } | null;
  closeModal: () => void;
}

const Modal = ({ modalData,closeModal }: ModalProps) => {
  if (!modalData || !modalData.car) {
    return null;
  }
  return (
    <div
      className="fixed top-0 left-0 w-full h-full flex items-center justify-center bg-black bg-opacity-50 z-50"
      onClick={closeModal}
    >
      <div
        className="bg-white rounded-lg h-full flex flex-col items-center  md:h-2/3 w-2/3 md:w-2/3 p-8 mx-auto"
        onClick={(e) => e.stopPropagation()}
      >
        <h2 className="text-xl font-bold mb-4 text-gray-800">
          Driver: {modalData.car.driver}
        </h2>
        <div className="text-gray-700 grid grid-cols-1 md:grid-cols-2 gap-y-2 h-[95%] md:h-[90%] md:w-full lg:w-[80%]">
          <Crashprobability crashProbability={0} />
          <Heartrate heartRate={0}/>
          <Gsr gsr={20}/>
          <BlinkRate blinkRate={0}/>
        </div>
      <div className="flex items-end">
          <button
            className="mt-6 px-4 py-2 bg-black text-white rounded hover:bg-gray-600 transition-colors duration-300"
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
