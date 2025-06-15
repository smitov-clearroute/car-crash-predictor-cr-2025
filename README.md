# 🏁 Le Mans Car Track Visualizer & Risk Prediction Dashboard

A real-time race visualization and predictive analytics platform for the **24 Hours of Le Mans**.
This project combines a visual canvas showing car movement on the **Circuit de la Sarthe** with telemetry-driven crash risk estimation.

---

## ✨ Features

* 🗺️ Interactive canvas rendering of the Le Mans track
* 🏎️ 30+ animated race cars moving live along the path
* 📈 Modular telemetry input (engine, brake, tire, biometric data)
* ⚠️ Risk prediction system estimating crash/failure likelihood
* 📊 Extendable dashboard to visualize metrics, telemetry, and predictions

---

## 🗂 Project Structure

```
├── app.py                  # Optional Flask backend for serving map + API
├── requirements.txt        # Python dependencies
├── frontend/
│   ├── static/
│   │   └── map.js          # Core animation & simulation logic
│   ├── public/
│   │   └── Circuit_de_la_Sarthe_map.webp  # Background image
│   └── index.html          # HTML entry point (canvas container)
```

---

## 🚀 Getting Started

### 1. Frontend Setup (Vite/Vanilla or React)

```bash
cd frontend
npm install
npm run dev
```

Visit: [http://localhost:5173/](http://localhost:5173/)

---

### 2. (Optional) Backend Setup (Flask + API)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Visit: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

You can expose endpoints like `/api/risk` to receive and process telemetry.

---

## 🧠 Crash Risk Model Inputs (Sample)

This project uses simulated or real-time telemetry such as:

```json
{
  "engine_rpm": 6995.58,
  "brake_pedal_pressure": 3.9,
  "brake_disc_temp_FL": 380.6,
  "tire_pressure_FR": 30.03,
  "tire_wear_rate": 0.0000052,
  "oil_temperature": 100.0,
  "oil_pressure": 60.0,
  "heart_rate": 131,
  "gsr": 4.06,
  "pupil_dilation": 3.0,
  "blink_rate": 18.0,
  "track_temperature": 35.01,
  "rainfall_intensity": 0.065,
  "ambient_light": 783.8
}
```

🧪 These metrics feed into a crash/failure probability engine (in progress) which can color-code cars or trigger alerts.

---

## 🛠 Customization & Extension

| Goal                          | How to do it                                |
| ----------------------------- | ------------------------------------------- |
| Add more cars                 | Update the `cars` array in `map.js`         |
| Change track or scale         | Replace background in `public/`             |
| Connect to live data          | Use `fetch()` to pull from `/api/telemetry` |
| Show car IDs or flags         | Add labels in the canvas draw logic         |
| Highlight crash-prone drivers | Color-code by risk level                    |

---

## 🧩 Coming Soon

* 🧠 Machine Learning model for crash prediction
* 🖼️ UI dashboard with car telemetry in real time
* 📍 Sector timing, laps completed, weather overlay
* 🛠️ Admin mode to simulate scenarios manually

---

## 📄 License

MIT — or use a license appropriate for your hackathon or internal project.
