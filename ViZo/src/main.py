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

    def fetch_audio(self):
        try:
            response = requests.get("http://127.0.0.1:8000/sounds")
            response.raise_for_status()
            sounds = response.json()
            return sounds
        except requests.RequestException as e:
            print(f"Fehler beim Abrufen der Soundnamen: {e}")
            return 0

    #ToDo: Diese Klasse funktioniert noch nicht richtig, aktuell allerdings auch unnötig und deshalb auf später verschoben
    #def delete_sound(self, sound_name: str):
    #    """Sendet einen DELETE-Request, um den Sound zu entfernen."""
    #    try:
    #        response = requests.delete(f"http://127.0.0.1:8000/sounds/{sound_name}")
    #        if response.status_code == 200:
    #            print(f"Sound {sound_name} wurde gelöscht.")
    #        return response.json()
    #   except requests.RequestException as e:
    #        print(f"Fehler beim Löschen des Sounds: {e}")
    #        return None

    def delete_sounds(self):
        """Sendet einen DELETE-Request, um den Sound zu entfernen."""
        try:
            response = requests.delete(f"http://127.0.0.1:8000/sounds")
            return response.json()
        except requests.RequestException as e:
            print(f"Fehler beim Löschen des Sounds: {e}")
            return None


if __name__ == "__main__":
    visualizer = Visualizer(fullScreen=False)
    visualizer.run(Connector)
    
