# visualizer.py
import pygame

# Farben
transparent_color = (255, 255, 255)  
circle_color = (255, 0, 0)        # Roter Kreis

class Visualizer:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Roboter-Visualisierung")
        self.clock = pygame.time.Clock()
        self.running = True

    def draw_circle(self, x, y):
        self.screen.fill(transparent_color)  
        pygame.draw.circle(self.screen, circle_color, (x, y), 20)  # Roter Kreis
        pygame.display.flip()

    def run(self, get_coordinates):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Koordinaten abrufen und Kreis zeichnen
            x, y = get_coordinates()
            self.draw_circle(x, y)
            self.clock.tick(60)  # 60 FPS

        pygame.quit()
