﻿import pygame
import requests

# Farben
transparent_color = (255, 255, 255)
circle_color = (255, 0, 0)  # Roter Kreis

class Visualizer:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Roboter-Visualisierung")
        self.clock = pygame.time.Clock()
        self.running = True

    def draw(self, objects):
        """Zeichnet alle sichtbaren Objekte."""
        self.screen.fill((255, 255, 255))  # Hintergrund schwarz

        for obj in objects:
            if obj["type"] == "circle":
                pygame.draw.circle(self.screen, obj["color"], (obj["x"], obj["y"]), obj["scale_x"], obj["border_width"])
            elif obj["type"] == "rectangle":
                pygame.draw.rect(self.screen, obj["color"], (obj["x"], obj["y"], obj["scale_x"], obj["scale_y"]), obj["border_width"])
    
        pygame.display.flip()
    
    def run(self, connection):
        """Startet die Visualisierungsschleife."""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Koordinaten abrufen und Kreis zeichnen
            objects = connection.fetch_objects(self)
            self.draw(objects)
            self.clock.tick(60)  # 60 FPS

        pygame.quit()
