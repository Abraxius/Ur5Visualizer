// api.ts
import axios from "axios";

// Basis-URL der FastAPI
const API_URL = "http://127.0.0.1:8000"; // Passe die URL an, wenn der Server auf einem anderen Port oder Host läuft

export const getObjects = async () => {
  try {
    const response = await axios.get(`${API_URL}/objects`);
    return response.data;
  } catch (error) {
    console.error("Fehler beim Abrufen der Objekte:", error);
    return [];
  }
};

export async function getObjectsTest() {
    const res = await fetch("http://127.0.0.1:8000/objects"); // FastAPI-Endpunkt
    if (!res.ok) {
      throw new Error("Fehler beim Abrufen der Objekte");
    }
    return res.json(); // Gibt die Objekte als JSON zurück
  }

export const updateObject = async (objectId: number, updatedObject: any) => {
  try {
    const response = await axios.post(`${API_URL}/update/${objectId}`, updatedObject);
    return response.data;
  } catch (error) {
    console.error("Fehler beim Aktualisieren des Objekts:", error);
    return null;
  }
};

export const createObject = async (newObject: any) => {
  try {
    const response = await axios.post(`${API_URL}/objects`, newObject);
    return response.data;
  } catch (error) {
    console.error("Fehler beim Erstellen des Objekts:", error);
    return null;
  }
};