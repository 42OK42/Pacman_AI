import pygame
import sys
from settings import info_panel_width, BLACK, WHITE, message_background_color, font
from rendering import render_text, render_text_center
from assets import coin_image, end_image, pacman_image, opponent_image
from level import load_level, draw_level
from game_functions import screen_width, screen_height, level_map, move_player, collect_coins, is_walkable, opponent_positions, player_position, coin_positions, end_position, total_coins, coins_collected

# Globale Variablen

# Initialisierung von Pygame
pygame.init()


level_map = load_level('level.txt', )

# Fenstergröße und Titel einstellen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Labyrinth-Spiel")

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