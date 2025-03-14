import pygame
import requests
import os

# Farben
transparent_color = (255, 255, 255)
circle_color = (255, 0, 0)  # Roter Kreis

class Visualizer:
    def __init__(self, width=1000, height=600, fullScreen=False):
        pygame.init()
        pygame.mixer.init()
        
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

    def draw_crosshair(self, screen, color, center_x, center_y, size=20, border_with=2):
        horizontal_line = [(center_x - size/2, center_y), (center_x + size/2, center_y)]
        vertical_line = [(center_x, center_y - size/2), (center_x, center_y + size/2)]
        
        pygame.draw.lines(screen, color, False, horizontal_line, border_with)
        pygame.draw.lines(screen, color, False, vertical_line, border_with)

    def play_sound(self, sound_list, connector):
        """Spielt eine Sound-Datei ab."""
        if sound_list:
            for snd in sound_list:
                try:
                    sound_path = os.path.join("sounds", snd["name"])

                    if not os.path.exists(sound_path):
                        print(f"Fehler: Audiodatei '{sound_path}' nicht gefunden.")
                        continue  # Nächste Datei prüfen

                    sound = pygame.mixer.Sound(sound_path)
                    sound.play()
                except Exception as e:
                    print(f"Fehler beim Laden der Audiodatei: {e}")
            connector.delete_sounds()

    def draw_rotated_rectangle(self, obj):
        """Zeichnet ein Rechteck mit Rotation."""
        rotation_angle = obj.get("rotation", 0)  # Standardwert: 0° Rotation
    
        rect_surface = pygame.Surface((obj["scale_x"], obj["scale_y"]), pygame.SRCALPHA)
        pygame.draw.rect(rect_surface, obj["color"], (0, 0, obj["scale_x"], obj["scale_y"]), obj["border_width"])
        
        rotated_surface = pygame.transform.rotate(rect_surface, rotation_angle)   
        rotated_rect = rotated_surface.get_rect(center=(obj["x"], obj["y"]))
    
        self.screen.blit(rotated_surface, rotated_rect)



    def draw_image(self, obj):
        """Lädt ein Bild aus dem /images Ordner und zeigt es an der angegebenen Position."""
        try:
            image_path = os.path.join("images", obj["name"])

            # Überprüfen, ob die Datei existiert
            if not os.path.exists(image_path):
                print(f"Fehler: Bilddatei '{image_path}' nicht gefunden. Bild wird nicht geladen.")
                return  # Beende die Funktion
            
            # Bild nur einmal laden und zwischenspeichern
            if "image_surface" not in obj:
                obj["image_surface"] = pygame.image.load(image_path).convert_alpha()
    
            image_surface = obj["image_surface"]
            image_surface = pygame.transform.scale(image_surface, (obj["scale_x"], obj["scale_y"]))
            image_surface = pygame.transform.rotate(image_surface, obj["rotation"])
    
            image_rect = image_surface.get_rect(center=(obj["x"], obj["y"]))
            self.screen.blit(image_surface, image_rect)
    
        except Exception as e:
            print(f"Fehler beim Laden des Bildes {obj['image_name']}: {e}")
            return


    def draw(self, objects):
        """Zeichnet alle sichtbaren Objekte."""
        self.screen.fill((255, 255, 255))  

        for obj in objects:
            if obj["type"] == "circle":
                pygame.draw.circle(self.screen, obj["color"], ((obj["x"]), (obj["y"])), obj["scale_x"]/2, obj["border_width"])
            elif obj["type"] == "rectangle":
                self.draw_rotated_rectangle(obj)
            elif obj["type"] == "lines":
                pygame.draw.lines(self.screen, obj["color"], False, obj["lines_points"], obj["border_width"])
            elif obj["type"] == "text":
                text_surface = self.font.render(obj["text"], True, obj["color"])
                text_rect = text_surface.get_rect(center=(obj["x"], obj["y"]))
                self.screen.blit(text_surface, text_rect)
            elif obj["type"] == "crosshair":
                self.draw_crosshair(self.screen, obj["color"], obj["x"], obj["y"], obj["scale_x"], obj["border_width"])
            elif obj["type"] == "image":
                self.draw_image(obj)
            else:
                print("type is not known")
                
        pygame.display.flip()
    
    def credits(self):
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)

        # Aktuelle Fenstergröße abrufen
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        # Text rendern
        title_text = self.font.render("ViZo", True, WHITE)
        version_text = self.font.render("Version 1.0", True, WHITE)
        author_text = self.font.render("by Alexander Jost", True, WHITE)
        
        # Positionen berechnen
        title_rect = title_text.get_rect(center=(screen_width / 2, screen_height / 3))
        version_rect = version_text.get_rect(center=(screen_width / 2, screen_height / 2))
        author_rect = author_text.get_rect(center=(screen_width / 2, screen_height * 2 / 3))
        
        # Startscreen anzeigen
        self.screen.fill(BLACK)
        self.screen.blit(title_text, title_rect)
        self.screen.blit(version_text, version_rect)
        self.screen.blit(author_text, author_rect)
        pygame.display.flip()
        
        # Kurze Wartezeit für den Startscreen
        pygame.time.delay(3000)  
        return 0
    
    def run(self, connection):
        """Startet die Visualisierungsschleife."""
        
        self.credits()
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
    
            # Koordinaten abrufen und Kreis zeichnen
            objects = connection.objects
            self.draw(objects)
            self.clock.tick(60)  # 60 FPS
            
            sounds = connection.sounds
            self.play_sound(sounds, connection)

        pygame.quit()
