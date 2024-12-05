# main.py
import requests

from visualizer import Visualizer

# Dummy-Datenquelle (Bewegung in X-Richtung)
def dummy_coordinates():
    import time
    t = time.time()  # Aktuelle Zeit
    x = int(400 + 100 * (t % 10))  # X-Koordinate bewegt sich sinusförmig
    y = 300  # Y-Koordinate bleibt konstant
    return x, y

def fetch_coordinates():
    response = requests.get("http://127.0.0.1:5000/coordinates")
    data = response.json()
    return data["x"], data["y"]

if __name__ == "__main__":
    visualizer = Visualizer()
    visualizer.run(fetch_coordinates)
