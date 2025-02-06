import time

import requests
from visualizer import Visualizer

class Connector:
    def fetch_objects(self):
        """Koordinaten vom Server abrufen."""
        try:
            response = requests.get("http://127.0.0.1:8000/objects")
            response.raise_for_status()
            objects = response.json()
            return [obj for obj in objects if obj["visible"]]  # Nur sichtbare Objekte zurückgeben
        except requests.RequestException as e:
            print(f"Fehler beim Abrufen der Koordinaten: {e}")
            return 0, 0

    # Dummy-Datenquelle (Bewegung in X-Richtung)
    def dummy_coordinates(self):
        import time
        t = time.time()  # Aktuelle Zeit
        x = int(400 + 100 * (t % 10))  # X-Koordinate bewegt sich sinusförmig
        y = 300  # Y-Koordinate bleibt konstant
        return x, y


if __name__ == "__main__":
    visualizer = Visualizer(fullScreen=False)
    visualizer.run(Connector)
    
