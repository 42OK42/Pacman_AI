from assets import wall_image
from settings import BLACK, original_tile_size, scale_factor, background_color

# Funktion zum Laden des Levels aus einer Datei
def load_level(filename):
	with open(filename, 'r') as file:
		level_map = file.read().splitlines()
	return level_map

tile_size = int(original_tile_size * scale_factor)

level_map = load_level('level.txt')

def find_opponent_start_positions(level_map):
	start_positions = []
	for y, row in enumerate(level_map):
		for x, char in enumerate(row):
			if char == 'O':
				start_positions.append((x, y))
	return start_positions

def draw_level_partially(screen, level_map, update_rects):
	for rect in update_rects:
		x_start = rect.x // tile_size
		x_end = (rect.x + rect.width) // tile_size + 1
		y_start = rect.y // tile_size
		y_end = (rect.y + rect.height) // tile_size + 1

		for y in range(y_start, min(y_end, len(level_map))):
			for x in range(x_start, min(x_end, len(level_map[0]))):
				position = (x * tile_size, y * tile_size)
				tile = level_map[y][x]
				if tile == 'W':
					screen.blit(wall_image, position)
				else:
					screen.fill(background_color, (position, (tile_size, tile_size)))

# Zeichnen des Levels (angepasst, um Bilder zu verwenden)
def draw_level(screen, level_map):
	for y, row in enumerate(level_map):
		for x, tile in enumerate(row):
			position = (x * tile_size, y * tile_size)
			if tile == 'W':
				screen.blit(wall_image, position)
			else:
				screen.fill(background_color, (position, (tile_size, tile_size)))