import pygame
from settings import tile_size, info_panel_width, opponent_step_size, debug_game_functions, BLACK
from assets import coin_image, end_image, player_image, opponent_image
from level import level_map, draw_level

# Skalierte Breite des Info-Panels
map_height = len(level_map)
map_width = max(len(row) for row in level_map)
screen_width = map_width * tile_size + info_panel_width
screen_height = map_height * tile_size

# game_functions.py
player_position = None  # oder einen anderen Anfangswert
coin_positions = []  # oder einen anderen Anfangswert
opponent_positions = []  # oder einen anderen Anfangswert
end_position = None  # oder einen anderen Anfangswert
total_coins = 0  # oder einen anderen Anfangswert
# Rest des Codes

# Spielobjekte initialisieren
def setup_game(level_map):
	global player_position, coin_positions, opponent_positions, end_position, total_coins
	for y, row in enumerate(level_map):
		for x, tile in enumerate(row):
			position = (x * tile_size, y * tile_size)
			if tile == 'P':
				player_position = position
			elif tile == 'C':
				coin_positions.append(position)
			elif tile == 'O':
				opponent_positions.append(position)
			elif tile == 'E':
				end_position = position
	total_coins = len(coin_positions)

setup_game(level_map)

def initialize_game_screen(screen, exit_position, coin_positions, player_position, opponents):
	screen.fill(BLACK)
	draw_level(screen, level_map)
	screen.blit(player_image, player_position)
	for coin_pos in coin_positions:
		screen.blit(coin_image, coin_pos)
	if exit_position:
		screen.blit(end_image, exit_position)
	for opponent in opponents:
		screen.blit(opponent_image, opponent.position)
	pygame.display.update()
coins_collected = 0

def check_if_player_is_at_coin(player_pos, coins):
	player_rect = pygame.Rect(player_pos, (tile_size, tile_size))
	for coin_pos in coins:
		coin_rect = pygame.Rect(coin_pos, (tile_size, tile_size))
		if player_rect.colliderect(coin_rect):
			return True
	return False

def collect_coin(player_pos, coins):
	global coins_collected
	player_rect = pygame.Rect(player_pos, (tile_size, tile_size))
	new_coins = []
	for coin_pos in coins:
		coin_rect = pygame.Rect(coin_pos, (tile_size, tile_size))
		if player_rect.colliderect(coin_rect):
			coins_collected += 1  # Erhöhen Sie die Anzahl der gesammelten Münzen
		else:
			new_coins.append(coin_pos)  # Die Münze wird nicht entfernt
	return new_coins

def move_player(position, direction):
	x, y = position
	if direction == 'up':
		y -= tile_size
	elif direction == 'down':
		y += tile_size
	elif direction == 'left':
		x -= tile_size
	elif direction == 'right':
		x += tile_size
	return x, y

def calculate_new_position_opponent(position, direction):
	x, y = position
	if direction == 'up':
		y = y - opponent_step_size
	elif direction == 'down':
		y = y + opponent_step_size
	elif direction == 'left':
		x = x - opponent_step_size
	elif direction == 'right':
		x = x + opponent_step_size
	return x, y


def calculate_direction(from_pos, to_pos):
	deltaX = to_pos[0] - from_pos[0]
	deltaY = to_pos[1] - from_pos[1]

	if abs(deltaX) > abs(deltaY):
		if (debug_game_functions):
			print("right" if deltaX > 0 else "left")
		return 'right' if deltaX > 0 else 'left'
	else:
		if (debug_game_functions):
			print("down" if deltaY > 0 else "up")
		return 'down' if deltaY > 0 else 'up'


def is_walkable_player(target_pos, level_map, coins_remaining):
	map_x, map_y = target_pos[0] // tile_size, target_pos[1] // tile_size
	if 0 <= map_x < map_width and 0 <= map_y < map_height:
		tile = level_map[map_y][map_x]
		# Das Ziel ist begehbar, wenn keine Münzen übrig sind
		if tile == 'E' and coins_remaining == 0:
			return True
		# Andere begehbare Felder
		return tile in ['B', 'C', 'P', 'E']
	return False
