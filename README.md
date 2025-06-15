# Le Mans Car Track Visualizer

This project visualizes the Circuit de la Sarthe (Le Mans) track and animates race cars (as dots) moving around the track using a Flask backend and JavaScript frontend.

## Features
- Visual representation of the Le Mans track
- Animated race cars (dots) moving along the track
- Easily extendable for real or simulated driver data

## Project Structure
- `app.py` — Flask backend serving the main page and static files
- `templates/iframe.html` — Main HTML template with canvas and JS
- `static/map.js` — JavaScript for drawing the track and animating cars
- `static/Circuit_de_la_Sarthe_map.webp` — Track map image
- `requirements.txt` — Python dependencies

## Getting Started

### 1. Backend Setup (Flask)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Visit [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser.

## How It Works
- The Flask app serves a page with a canvas and loads the track image.
- `map.js` animates colored dots (cars) moving along the track.
- You can update `map.js` to fetch real-time data from the backend or an API.

## Customization & Extension
- **Add more cars:** Edit the `cars` array in `static/map.js`.
- **Use real data:** Add a Flask API endpoint and fetch data in `map.js`.
- **Change visuals:** Adjust colors, dot size, or add labels in `map.js`.

## License
MIT (or specify your hackathon's license requirements) 