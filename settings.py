import pygame

# Skalierungsfaktor für die Größe des Spiels
scale_factor = 2.0

# Originalgrößen
original_tile_size = 50  # Die ursprüngliche Größe der Kachel
original_info_panel_width = 200  # Die ursprüngliche Breite des Info-Panels

# Farbdefinitionen
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
LIME = (50, 205, 50)
PINK = (255, 192, 203)
TEAL = (0, 128, 128)
NAVY = (0, 0, 128)
MAROON = (128, 0, 0)
OLIVE = (128, 128, 0)
BROWN = (165, 42, 42)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
BEIGE = (245, 245, 220)
MINT = (189, 252, 201)
LAVENDER = (230, 230, 250)

# Nachricht Hintergrundfarbe
message_background_color = (GOLD)

# Schriften
pygame.font.init()
font = pygame.font.SysFont("Arial", 36)

tile_size = int(original_tile_size * scale_factor)  # Skalierte Kachelgröße
info_panel_width = int(original_info_panel_width * scale_factor) 