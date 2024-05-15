import pygame
import sys
from settings import BLACK, WHITE, font, tile_size, debug_opponent, win_message_background_color, info_panel_width, bullet_move_interval, background_color
from rendering import render_text_center, render_text
from assets import coin_image, end_image, player_image, opponent_image, bullet_image
from level import load_level, draw_level_partially
from game_functions import screen_width, screen_height, move_player, collect_coin, is_walkable_player, check_if_player_is_at_coin, initialize_game_screen
from opponent import Opponent

# Initialisierung von Pygame
def run_player_controlled_game():
	pygame.init()
	screen = pygame.display.set_mode((screen_width, screen_height))
	pygame.display.set_caption("Pacman-Spiel")

	# Lade die Level-Karte
	level_map = load_level('level.txt')

	# Startpositionen für Spieler, Gegner, Münzen und Exit finden
	player_position = None
	coin_positions = []
	opponent_positions = []
	exit_position = None
	coins_collected = 0

	for y, line in enumerate(level_map):
		for x, char in enumerate(line):
			world_x, world_y = x * tile_size, y * tile_size
			if char == 'P':
				player_position = (world_x, world_y)
			elif char == 'C':
				coin_positions.append((world_x, world_y))
			elif char == 'O':
				opponent_positions.append((world_x, world_y))
			elif char == 'E':
				exit_position = (world_x, world_y)

	total_coins = len(coin_positions)
	opponents = [Opponent(pos, level_map, opponent_positions) for pos in opponent_positions]

	initialize_game_screen(screen, exit_position, coin_positions, player_position, opponents)

	# Hauptspiel-Schleife
	running = True
	while running:
		updated_rects = []
		# player_movement
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key in [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]:
					direction = {pygame.K_w: 'up', pygame.K_s: 'down', pygame.K_a: 'left', pygame.K_d: 'right'}[event.key]
					new_position = move_player(player_position, direction)
					if is_walkable_player(new_position, level_map, len(coin_positions)):
						old_rect = pygame.Rect(player_position[0], player_position[1], tile_size, tile_size)
						player_position = new_position
						new_rect = pygame.Rect(player_position[0], player_position[1], tile_size, tile_size)
						updated_rects.extend([old_rect, new_rect])  # Füge sowohl die alte als auch die neue Position zu den zu aktualisierenden Bereichen hinzu
						if check_if_player_is_at_coin(player_position, coin_positions):
							coin_positions = collect_coin(player_position, coin_positions)
							coins_collected += 1

		screen.fill(background_color)
		draw_level_partially(screen, level_map, updated_rects)  # Zeichnet nur die geänderten Teile des Levels
		screen.blit(player_image, player_position)
		for coin_pos in coin_positions:
			screen.blit(coin_image, coin_pos)
		if exit_position:
			screen.blit(end_image, exit_position)

		for opponent in opponents:
			#Move opponent
			result_move = opponent.move_smartly(player_position)
			if result_move:
				old_pos, new_pos = result_move
				old_rect = pygame.Rect(old_pos[0], old_pos[1], tile_size, tile_size)
				new_rect = pygame.Rect(new_pos[0], new_pos[1], tile_size, tile_size)
				updated_rects.extend([old_rect, new_rect])
			screen.blit(opponent_image, opponent.position)  # Füge das Rechteck zur Liste der zu aktualisierenden Bereiche hinzu
			# Shoot bullet
			opponent.try_shoot(player_position, pygame.time.get_ticks(), updated_rects)
			# Move bullets
			for bullet in opponent.bullets:
				current_time = pygame.time.get_ticks()
				if current_time - bullet.move_time > bullet_move_interval:
					previous_bullet_position = bullet.position
					if bullet.move(level_map):
						old_bullet_rect = pygame.Rect(previous_bullet_position[0], previous_bullet_position[1], tile_size, tile_size)
						updated_rects.append(old_bullet_rect)
					
						# Zeichne das Geschoss an der neuen Position
						new_bullet_rect = pygame.Rect(bullet.position[0], bullet.position[1], tile_size, tile_size)
						updated_rects.append(new_bullet_rect)
						
						screen.blit(bullet_image, bullet.position)
						bullet.move_time = current_time
					else:
						bullet_rect = pygame.Rect(bullet.position[0], bullet.position[1], tile_size, tile_size)
						updated_rects.append(bullet_rect)  # Füge das Rechteck zur Liste der zu aktualisierenden Bereiche hinzu
						opponent.bullets.remove(bullet)  # Entferne das Bullet sicher

				if bullet.check_bullet_collision(player_position):
					message_rect = pygame.Rect(0, screen_height // 2 - 30, screen_width, 60)  # Anpassen nach Bedarf
					pygame.draw.rect(screen, BLACK, message_rect)  # Übermalt den alten Inhalt
					render_text_center("Spieler gestorben", font, WHITE, screen, screen_height // 2)
					updated_rects.append(message_rect)
					pygame.display.update(updated_rects)  # Aktualisiere nur den Nachrichtenbereich
					pygame.time.delay(1000)
					running = False

		if len(coin_positions) == 0 and player_position == exit_position:
			message_background = pygame.Rect(0, screen_height // 2 - 30, screen_width, 60)
			pygame.draw.rect(screen, win_message_background_color, message_background)
			render_text_center("Herzlichen Glückwunsch, Level geschafft!", font, WHITE, screen, screen_height // 2)
			updated_rects.append(message_background)
			pygame.display.update(updated_rects)  # Aktualisiere nur den Nachrichtenbereich
			pygame.time.delay(1000)
			running = False

		coins_text = f"Coins: {coins_collected}/{total_coins}"
		render_text(coins_text, font, WHITE, screen, screen_width - info_panel_width // 2, 10)

		pygame.display.update(updated_rects)  # Aktualisiere nur die geänderten Bereiche

	# Spiel beenden
	pygame.quit()
	sys.exit()