import pygame
import requests

# Farben
transparent_color = (255, 255, 255)
circle_color = (255, 0, 0)  # Roter Kreis



class Visualizer:
    def __init__(self, width=1000, height=600, fullScreen=False):
        pygame.init()

        #Standard-Schriftart mit Größe 36
        self.font = pygame.font.Font(None, 36)
        
        # Bildschirmgröße automatisch abrufen
        screen_info = pygame.display.Info()
        screen_width, screen_height = screen_info.current_w, screen_info.current_h

        if fullScreen:
            flags = pygame.NOFRAME  # Borderless-Fenster (rahmenlos, füllt ganzen Bildschirm)
            self.screen = pygame.display.set_mode((screen_width, screen_height), flags)
        else:
            self.screen = pygame.display.set_mode((width, height))
            
        #self.screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
        pygame.display.set_caption("Roboter-Visualisierung")
        self.clock = pygame.time.Clock()
        self.running = True

    def draw(self, objects):
        """Zeichnet alle sichtbaren Objekte."""
        self.screen.fill((255, 255, 255))  # Hintergrund schwarz

        for obj in objects:
            if obj["type"] == "circle":
                pygame.draw.circle(self.screen, obj["color"], ((obj["x"]-obj["scale_x"]), (obj["y"]-obj["scale_x"])), obj["scale_x"], obj["border_width"])
            elif obj["type"] == "rectangle":
                pygame.draw.rect(self.screen, obj["color"], ((obj["x"] - obj["scale_x"]/2), (obj["y"] - obj["scale_y"]/2), obj["scale_x"], obj["scale_y"]), obj["border_width"])
            elif obj["type"] == "lines":
                pygame.draw.lines(self.screen, obj["color"], False, obj["lines_points"], obj["border_width"])
            elif obj["type"] == "text":
                text_surface = self.font.render(obj["text"], True, obj["color"])
                text_rect = text_surface.get_rect(center=(obj["x"], obj["y"]))
                self.screen.blit(text_surface, text_rect)
    
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
