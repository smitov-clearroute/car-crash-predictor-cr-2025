from fastapi import FastAPI
import race_data_simulator
import race_simulator
from calculate_risk import calculate_risk

drivers = [
    ("Max Verstappen", "Red Bull RB20 #1", 1),
    ("Lando Norris", "McLaren MCL38 #4", 2),
    ("Charles Leclerc", "Ferrari SF-24 #16", 3),
    ("Oscar Piastri", "McLaren MCL38 #81", 4),
    ("Carlos Sainz", "Ferrari SF-24 #55", 5),
    ("George Russell", "Mercedes W15 #63", 6),
    ("Lewis Hamilton", "Mercedes W15 #44", 7),
    ("Sergio Pérez", "Red Bull RB20 #11", 8),
    ("Fernando Alonso", "Aston Martin AMR24 #14", 9),
    ("Lance Stroll", "Aston Martin AMR24 #18", 10)
]

app = FastAPI()

driver_simulators = []
race_simulators = []
for driver_name, car_name, position in drivers:
    driver_sim = race_simulator.DriverRaceSimulator(driver_name, car_name, position)
    driver_simulators.append(driver_sim)
    race_sim = race_data_simulator.RaceDataSimulator() 
    race_simulators.append(race_sim)

@app.get("/stats")
def get_realtime_risk():
    data = []
    for i in range(len(driver_simulators)):
        driver_data = driver_simulators[i].generate_next_data_point()
        race_data = race_simulators[i].generate_next_data_point()
        data.append({"driver_data": driver_data, "data": race_data, "risk": calculate_risk()})

    return data
