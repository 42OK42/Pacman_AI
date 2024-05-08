from assets import wall_image
from settings import BLACK, original_tile_size, scale_factor


# Funktion zum Laden des Levels aus einer Datei
def load_level(filename):
	with open(filename, 'r') as file:
		level_map = file.read().splitlines()
	return level_map

tile_size = int(original_tile_size * scale_factor)

level_map = load_level('level.txt')

# Zeichnen des Levels (angepasst, um Bilder zu verwenden)
def draw_level(screen, level_map):
	for y, row in enumerate(level_map):
		for x, tile in enumerate(row):
			position = (x * tile_size, y * tile_size)
			if tile == 'W':
				screen.blit(wall_image, position)
			else:
				screen.fill(BLACK, (position, (tile_size, tile_size)))