import time
import json
import hashlib
import threading
import requests
from visualizer import Visualizer

class Connector:
    def __init__(self):
        self.objects = []  
        self.sounds = []   
        self.running = True 

        # Starte separate Threads für Objekte & Sounds
        threading.Thread(target=self.update_objects, daemon=True).start()
        threading.Thread(target=self.update_sounds, daemon=True).start()

    def fetch_objects(self):
        """API-Request senden und Objekte abrufen"""
        try:
            response = requests.get("http://127.0.0.1:8000/objects", timeout=1)
            response.raise_for_status()
            self.objects = [obj for obj in response.json() if obj["visible"]]
        except requests.RequestException as e:
            print(f"Fehler beim Abrufen der Koordinaten: {e}")

    def fetch_audio(self):
        try:
            response = requests.get("http://127.0.0.1:8000/sounds", timeout=1)
            response.raise_for_status()
            self.sounds = response.json()
        except requests.RequestException as e:
            print(f"Fehler beim Abrufen der Soundnamen: {e}")

    def update_objects(self):
        """Hintergrund-Thread: Lädt kontinuierlich neue Objektdaten."""
        while self.running:
            self.fetch_objects()
            time.sleep(0.1)  # API-Abfrage alle 100ms (verhindert Überlastung)

    def update_sounds(self):
        """Hintergrund-Thread: Lädt kontinuierlich neue Sounddaten."""
        while self.running:
            self.fetch_audio()
            time.sleep(0.1)  # API-Abfrage alle 100ms

    def delete_sounds(self):
        """Sendet einen DELETE-Request, um abgespielte Sounds zu entfernen."""
        try:
            response = requests.delete("http://127.0.0.1:8000/sounds")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Fehler beim Löschen der Sounds: {e}")
            return None

if __name__ == "__main__":
    visualizer = Visualizer(fullScreen=False)
    visualizer.run(Connector())
