import pygame
from settings import BLACK, WHITE, font, tile_size, debug_opponent, win_message_background_color, info_panel_width, bullet_move_interval, background_color
from rendering import render_text_center, render_text
from assets import coin_image, end_image, player_image, opponent_image, bullet_image
from level import load_level, draw_level_partially
from opponent import Opponent
from settings import RENDER, AI_MODE
from game_functions import screen_width, screen_height
from custom_game_env import CustomGameEnv
from player_controlled import run_player_controlled_game

def main():
	# Initialisiere die Spielumgebung
	env = CustomGameEnv()
	#obs = env.reset()

	if AI_MODE:
		print("AI-Modus aktiviert")
		running = True
		while running:
			# Verarbeite Spielerinputs
			action = None
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						running = False

					# Mappe Tastatureingaben auf Aktionen
					action_map = {
						pygame.K_w: 0,  # Oben
						pygame.K_s: 1,  # Unten
						pygame.K_a: 2,  # Links
						pygame.K_d: 3   # Rechts
					}
					if event.key in action_map:
						action = action_map[event.key]

			# Führe einen Schritt aus basierend auf der Aktion oder führe eine Standardaktion aus
			if action is not None:
				print("Aktion:", action)
				obs, reward, done, info = env.step(action)
			else:
				# Führe eine "Neutrale" Aktion aus, um das Spiel zu aktualisieren, auch wenn keine Eingabe erfolgt
				obs, reward, done, info = env.step(-1)  # annehmen, dass Aktion 0 eine neutrale Aktion ist

			if done:
				print("Spiel beendet, Neustart...")
				#obs = env.reset()  # Reset, wenn das Spiel beendet ist
				running = False

			if RENDER:
				env.render()  # Aktualisiere die grafische Darstellung des Spiels

		env.close()  # Schließe die Umgebung, wenn das Spiel beendet wird
	else:
		run_player_controlled_game()

if __name__ == "__main__":
	main()