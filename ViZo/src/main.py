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
    """Koordinaten vom Server abrufen."""
    try:
        response = requests.get("http://127.0.0.1:8000/status")
        response.raise_for_status()
        data = response.json()
        return data.get("x", 0), data.get("y", 0)
    except requests.RequestException as e:
        print(f"Fehler beim Abrufen der Koordinaten: {e}")
        return 0, 0

if __name__ == "__main__":
    visualizer = Visualizer()
    visualizer.run(fetch_coordinates)
