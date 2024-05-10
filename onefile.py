import pygame
import sys

# Globale Variablen
global current_direction_opponent
scale_factor = 2.0
player_position = None
coin_positions = []
opponent_positions = []
end_position = None
coins_collected = 0

# Initialisierung von Pygame
pygame.init()

# Karte aus Datei laden
def load_level(filename):
	with open(filename, 'r') as file:
		level_map = file.read().splitlines()
	return level_map

level_map = load_level('level.txt')

# Originalgrößen
original_tile_size = 50  # Die ursprüngliche Größe der Kachel
original_info_panel_width = 200  # Die ursprüngliche Breite des Info-Panels

# Skalierte Größen
tile_size = int(original_tile_size * scale_factor)  # Skalierte Kachelgröße
info_panel_width = int(original_info_panel_width * scale_factor)  # Skalierte Breite des Info-Panels
map_height = len(level_map)
map_width = max(len(row) for row in level_map)
screen_width = map_width * tile_size + info_panel_width
screen_height = map_height * tile_size

# Fenstergröße und Titel einstellen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Labyrinth-Spiel")

# Farben
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

def load_and_scale_image(image_path, scale_factor):
	image = pygame.image.load(image_path)
	image_size = (int(image.get_width() * scale_factor), int(image.get_height() * scale_factor))
	return pygame.transform.scale(image, image_size)

# Bilder laden und Größe anpassen
pacman_image = load_and_scale_image('pacman.png', scale_factor/10)
opponent_image = load_and_scale_image('opponent.png', scale_factor/10)
coin_image = load_and_scale_image('coin.png', scale_factor/10)
end_image = load_and_scale_image('end.png', scale_factor/10)
wall_image = load_and_scale_image('wall.png', scale_factor/10)

# Schriften
pygame.font.init()
font = pygame.font.SysFont("Arial", 36)

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

# Zeichnen des Levels (angepasst, um Bilder zu verwenden)
def draw_level(screen, level_map):
	for y, row in enumerate(level_map):
		for x, tile in enumerate(row):
			position = (x * tile_size, y * tile_size)
			if tile == 'W':
				screen.blit(wall_image, position)
			else:
				screen.fill(BLACK, (position, (tile_size, tile_size)))

def collect_coins(player_pos, coins):
	global coins_collected
	player_rect = pygame.Rect(player_pos, (tile_size, tile_size))
	new_coins = []
	for coin_pos in coins:
		coin_rect = pygame.Rect(coin_pos, (tile_size, tile_size))
		if player_rect.colliderect(coin_rect):
			coins_collected += 1
		else:
			new_coins.append(coin_pos)
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

def is_walkable(target_pos, level_map, coins_remaining):
	map_x, map_y = target_pos[0] // tile_size, target_pos[1] // tile_size
	if 0 <= map_x < map_width and 0 <= map_y < map_height:
		tile = level_map[map_y][map_x]
		# Das Ziel ist begehbar, wenn keine Münzen übrig sind
		if tile == 'E' and coins_remaining == 0:
			return True
		# Andere begehbare Felder
		return tile in ['B', 'C']
	return False

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

# Zeichnen des Levels (angepasst, um Bilder zu verwenden)
def draw_level(screen, level_map):
	for y, row in enumerate(level_map):
		for x, tile in enumerate(row):
			position = (x * tile_size, y * tile_size)
			if tile == 'W':
				screen.blit(wall_image, position)
			else:
				screen.fill(BLACK, (position, (tile_size, tile_size)))

# Spiel-Hauptschleife
running = True
while running:
	# Ereignisse durchlaufen
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:
			new_position = player_position 
			if event.key == pygame.K_w:
				new_position = move_player(player_position, 'up')
			elif event.key == pygame.K_s:
				new_position = move_player(player_position, 'down')
			elif event.key == pygame.K_a:
				new_position = move_player(player_position, 'left')
			elif event.key == pygame.K_d:
				new_position = move_player(player_position, 'right')

			# Validieren Sie die neue Position, bevor Sie den Spieler bewegen
			if is_walkable(new_position, level_map, len(coin_positions)):
				player_position = new_position
				# Münzen sammeln, wenn auf Münzenposition bewegt
				coin_positions = collect_coins(player_position, coin_positions)
				
	# Bildschirm aktualisieren
	screen.fill(BLACK)
	draw_level(screen, level_map)

	# Münzen zeichnen (mit Bild)
	for coin_pos in coin_positions:
		screen.blit(coin_image, coin_pos)
	# Zeichnen Sie die Tür, falls keine Münzen mehr vorhanden sind
	if len(coin_positions) == 0:
		screen.blit(end_image, end_position)
	# Zeichnen Sie alle Gegner
	for opponent_pos in opponent_positions:
		screen.blit(opponent_image, opponent_pos)
	# Zeichnen Sie den Spieler (Pacman)
	screen.blit(pacman_image, player_position)

	
	# Überprüfen, ob das Level abgeschlossen ist
	if len(coin_positions) == 0 and player_position == end_position:
		level_complete = True
		# Warten Sie einen Moment und zeigen Sie die Nachricht an
		pygame.time.delay(500)  # Warten für 0,5 Sekunden
		# Hintergrund für die Nachricht zeichnen
		message_background = pygame.Rect(0, screen_height // 2 - 30, screen_width, 60)
		pygame.draw.rect(screen, message_background_color, message_background)
		# Nachricht rendern und auf den Bildschirm zeichnen
		render_text_center("Herzlichen Glückwunsch, Level geschafft!", font, (255, 255, 255), screen, screen_height // 2)
		pygame.display.update()  # Aktualisieren des Displays nach dem Rendern des Textes
		pygame.time.delay(5000)  # Warten für 5 Sekunden
		running = False

	coins_text = f"Coins: {coins_collected}/{total_coins}"
	render_text(coins_text, font, WHITE, screen, screen_width - info_panel_width // 2, 10)

	pygame.display.update()

# Pygame beenden
pygame.quit()
sys.exit()