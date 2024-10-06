from flask import Flask, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import requests
from datetime import datetime, timedelta
import os

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

socketio = SocketIO(app, cors_allowed_origins="*")

NASA_API_KEY = os.environ.get("NASA_API_KEY")


def get_neo_data():
    # Obtener fecha actual y de mañana
    today = datetime.now().strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    print(today, tomorrow)
    # Hacer petición a la API de NASA
    url = f"https://api.nasa.gov/neo/rest/v1/feed"
    params = {"start_date": today, "end_date": tomorrow, "api_key": NASA_API_KEY}
    print(url, params)
    response = requests.get(url, params=params)

    # print(response.json())
    if response.status_code == 200:
        return response.json()
    return None


@socketio.on("connect")
def handle_connect():
    print("Cliente conectado")


@socketio.on("disconnect")
def handle_disconnect():
    print("Cliente desconectado")


@socketio.on("select_asteroid")
def handle_asteroid_selection(data):
    # Emitir los datos del asteroide seleccionado a todos los clientes
    emit("asteroid_updated", data, broadcast=True)


## new code
@socketio.on("celestial_body_selected")
def handle_celestial_body(data):
    # Emit the selected celestial body to all connected clients
    emit("update_celestial_body", {"body": data["body"]}, broadcast=True)


@app.route("/api/asteroids")
def get_asteroids():
    neo_data = get_neo_data()
    if neo_data:
        # Procesar y devolver solo los datos necesarios
        today = datetime.now().strftime("%Y-%m-%d")
        asteroids = neo_data["near_earth_objects"][today]
        processed_asteroids = []

        for asteroid in asteroids:
            processed_asteroids.append(
                {
                    "id": asteroid["id"],
                    "name": asteroid["name"],
                    "diameter": asteroid["estimated_diameter"]["kilometers"][
                        "estimated_diameter_max"
                    ],
                    "is_potentially_hazardous": asteroid[
                        "is_potentially_hazardous_asteroid"
                    ],
                    "close_approach_date": asteroid["close_approach_data"][0][
                        "close_approach_date_full"
                    ],
                    "velocity": asteroid["close_approach_data"][0]["relative_velocity"][
                        "kilometers_per_hour"
                    ],
                    "miss_distance": asteroid["close_approach_data"][0][
                        "miss_distance"
                    ]["kilometers"],
                }
            )
        # print(processed_asteroids)
        return {"asteroids": processed_asteroids}

    return {"error": "No se pudieron obtener los datos"}, 500


if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0')
