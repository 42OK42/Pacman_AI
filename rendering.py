import pygame
from settings import WHITE

def load_and_scale_image(image_path, scale_factor):
	image = pygame.image.load(image_path)
	image_size = (int(image.get_width() * scale_factor), int(image.get_height() * scale_factor))
	return pygame.transform.scale(image, image_size)

# Funktion zum Rendern von Text an einer bestimmten Position
def render_text(message, font, color, surface, x, y):
	text_obj = font.render(message, True, color)
	text_rect = text_obj.get_rect(topright=(x, y))
	surface.blit(text_obj, text_rect)

# Funktion zum Rendern von Text in der Mitte des Bildschirms
def render_text_center(message, font, color, surface, y_pos):
	text_obj = font.render(message, True, color)
	text_rect = text_obj.get_rect(center=(surface.get_width() // 2, y_pos))
	surface.blit(text_obj, text_rect)
