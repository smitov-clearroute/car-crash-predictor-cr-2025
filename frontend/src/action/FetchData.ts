import { useQuery } from "@tanstack/react-query";
import mockData from "../api/mockData.ts";

type Data = {
  position: number;
  number: number;
  driver: string;
  team : string;
  car: string;
  laps: number;
  gap: string;
  bestLap: string;
  maxSpeed: string;
  pits: number;
};

const typedMockData: Data[] = mockData as Data[];

export const fetchData = () => {
  // eslint-disable-next-line react-hooks/rules-of-hooks
  return useQuery({
    queryKey: ["carData"],
    queryFn: () => {
      return Promise.resolve(typedMockData);
    },
    refetchInterval: 1000,
  });
};
