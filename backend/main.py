from fastapi import FastAPI
import race_data_simulator
from calculate_risk import calculate_risk

app = FastAPI()

race_data_simulator.initialize_race_data_stream()

@app.get("/")
def get_realtime_risk():
    data = race_data_simulator.generate_next_data_point()
    risk = calculate_risk()
    return {"data": data, "risk": risk}
