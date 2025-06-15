import { useQuery } from "@tanstack/react-query";
import mockData from "../api/mockData.ts";

type Data = {
  position: number;
  number: number;
  driver: string;
  car: string;
  pic: string;
  laps: number;
  gap: string;
  bestLap: string;
  maxSpeed: string;
  pits: number;
};

const typedMockData: Data[] = mockData as Data[]; // Explicitly type the mockData

export const fetchData = () => {
  return useQuery({
    queryKey: ["carData"],
    queryFn: () => {
      return Promise.resolve(typedMockData);
    },
    refetchInterval: 1000,
  });
};
