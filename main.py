import pygame
import sys
from settings import info_panel_width, BLACK, WHITE, win_message_background_color, font, opponent_time_to_move, lose_message_background_color
from rendering import render_text, render_text_center
from assets import coin_image, end_image, player_image, opponent_image
from level import load_level, draw_level
from game_functions import screen_width, screen_height, level_map, move_player, collect_coins, is_walkable, opponent_positions, player_position, coin_positions, end_position, total_coins, coins_collected
from opponent import move_opponent_randomly, opponent_move_time, check_collision

# Globale Variablen

# Initialisierung von Pygame
pygame.init()


level_map = load_level('level.txt', )

# Fenstergröße und Titel einstellen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Labyrinth-Spiel")

opponent_move_time = pygame.time.get_ticks()

# Spiel-Hauptschleife
running = True
while running:
	# Ereignisse durchlaufen
	current_time = pygame.time.get_ticks()
	if current_time - opponent_move_time > opponent_time_to_move:  # 1000 Millisekunden (1 Sekunde)	
		for i, pos in enumerate(opponent_positions):
			new_position = move_opponent_randomly(pos, level_map)
			if new_position:
				opponent_positions[i] = new_position
				screen.blit(opponent_image, opponent_positions[i])
				if check_collision(player_position, opponent_positions[i]):
					message_background = pygame.Rect(0, screen_height // 2 - 30, screen_width, 60)
					pygame.draw.rect(screen, lose_message_background_color, message_background)
					# Nachricht rendern und auf den Bildschirm zeichnen
					render_text_center("Spieler gestorben", font, (255, 255, 255), screen, screen_height // 2)
					pygame.display.update()  # Aktualisieren des Displays nach dem Rendern des Textes
					pygame.time.delay(5000)  # Warten für 5 Sekunden
					running = False
				opponent_move_time = current_time
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
	screen.blit(player_image, player_position)


	# Überprüfen, ob das Level abgeschlossen ist
	if len(coin_positions) == 0 and player_position == end_position:
		level_complete = True
		# Warten Sie einen Moment und zeigen Sie die Nachricht an
		pygame.time.delay(500)  # Warten für 0,5 Sekunden
		# Hintergrund für die Nachricht zeichnen
		message_background = pygame.Rect(0, screen_height // 2 - 30, screen_width, 60)
		pygame.draw.rect(screen, win_message_background_color, message_background)
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