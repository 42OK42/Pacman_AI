import pygame
import gym
from gym import spaces
import numpy as np
from settings import RENDER, AI_MODE, background_color, tile_size, bullet_move_interval, win_message_background_color, font, BLACK, WHITE
from rendering import render_text_center, render_text
from assets import coin_image, end_image, player_image, opponent_image, bullet_image
from game_functions import move_player, is_walkable_player, check_if_player_is_at_coin, collect_coin, screen_width, screen_height
from level import load_level, draw_level_partially, draw_level
from opponent import Opponent

class CustomGameEnv(gym.Env):
	metadata = {'render.modes': ['human']}

	def __init__(self):
		super(CustomGameEnv, self).__init__()
		self.action_space = spaces.Discrete(4)  # 4 mögliche Aktionen: oben, unten, links, rechts
		self.observation_space = spaces.Box(low=0, high=255, shape=(screen_height, screen_width, 3), dtype=np.uint8)

		if RENDER:
			pygame.init()
			self.screen = pygame.display.set_mode((screen_width, screen_height))
			pygame.display.set_caption("Pacman-Spiel")

		self.clock = pygame.time.Clock()
		self.updated_rects = []
		self.initialize_game()

	def initialize_game(self):
		self.level_map = load_level('level.txt')
		self.player_position = None
		self.coin_positions = []
		self.opponent_positions = []
		self.exit_position = None
		self.coins_collected = 0
		self.opponents = []

		for y, line in enumerate(self.level_map):
			for x, char in enumerate(line):
				world_x, world_y = x * tile_size, y * tile_size
				if char == 'P':
					self.player_position = (world_x, world_y)
				elif char == 'C':
					self.coin_positions.append((world_x, world_y))
				elif char == 'O':
					new_opponent = Opponent((world_x, world_y), self.level_map, self.opponent_positions)
					self.opponents.append(new_opponent)
					self.opponent_positions.append((world_x, world_y))
				elif char == 'E':
					self.exit_position = (world_x, world_y)
		print("Player position1", self.player_position)
		print("opponent position1", self.opponent_positions)

		if RENDER:
			self.screen.fill(background_color)
			draw_level(self.screen, self.level_map)
			self.draw_game_elements()  # Diese Methode sollte alle dynamischen Elemente zeichnen.
			pygame.display.update()

	def step(self, action):
		# Führe die Aktion aus und aktualisiere den Zustand des Spiels
		self.update_game(action)

		# Berechne die Belohnung
		reward = self.calculate_reward()

		# Überprüfe, ob das Spiel beendet ist
		done = self.check_if_done()

		# Optional: zusätzliche Informationen, die nützlich sein könnten
		info = {}

		# Aktualisiere das Rendering, wenn nötig
		if RENDER:
			self.redraw_updated_areas()

		# Erstelle eine Beobachtung des neuen Zustands (optional, abhängig von deinen Anforderungen)
		obs = self.create_observation()

		return obs, reward, done, info

	def create_observation(self):
		# Diese Methode sollte den aktuellen Zustand der Umgebung in einer Form zurückgeben,
		# die von deinem Agenten interpretiert werden kann.
		# Beispiel:
		return pygame.surfarray.array3d(self.screen)

	def update_game(self, action):
		if action != -1:
			direction = ['up', 'down', 'left', 'right'][action]
			new_position = move_player(self.player_position, direction)
			
			if is_walkable_player(new_position, self.level_map, len(self.coin_positions)):
				# Erfasse die alte Position für das Update-Rect
				old_rect = pygame.Rect(self.player_position[0], self.player_position[1], tile_size, tile_size)

				# Aktualisiere die Spielerposition
				self.player_position = new_position

				# Erfasse die neue Position für das Update-Rect
				new_rect = pygame.Rect(self.player_position[0], self.player_position[1], tile_size, tile_size)

				# Füge beide Rechtecke zu den updated_rects hinzu
				self.updated_rects.append(old_rect)
				self.updated_rects.append(new_rect)

				if check_if_player_is_at_coin(self.player_position, self.coin_positions):
					self.coin_positions = collect_coin(self.player_position, self.coin_positions)
					self.coins_collected += 1

		for opponent in self.opponents:
			result = opponent.move_smartly(self.player_position)
			print("result", result)
			if result:
				old_pos, new_pos = result
				old_rect = pygame.Rect(old_pos[0], old_pos[1], tile_size, tile_size)
				new_rect = pygame.Rect(new_pos[0], new_pos[1], tile_size, tile_size)
				self.updated_rects.append(old_rect)
				self.updated_rects.append(new_rect)
				print("self.updated_rects", self.updated_rects)

			opponent.try_shoot(self.player_position, pygame.time.get_ticks(), self.updated_rects)

		self.handle_bullets()

		if RENDER:
			draw_level_partially(self.screen, self.level_map, self.updated_rects)
			self.draw_game_elements()
			self.redraw_updated_areas()

	def draw_game_elements(self):
		# Zeichne den Spieler
		self.screen.blit(player_image, self.player_position)

		# Zeichne die Münzen
		for pos in self.coin_positions:
			self.screen.blit(coin_image, pos)

		# Zeichne die Gegner
		for opponent in self.opponents:
			self.screen.blit(opponent_image, opponent.position)

		# Zeichne die Geschosse
		for opponent in self.opponents:
			for bullet in opponent.bullets:
				self.screen.blit(bullet_image, bullet.position)
	
	def handle_bullets(self):
		for opponent in self.opponents:
			for bullet in list(opponent.bullets):
				# Bestimme die alte Position des Geschosses für das Update-Rect
				old_rect = pygame.Rect(bullet.position[0], bullet.position[1], bullet.width, bullet.height)

				if pygame.time.get_ticks() - bullet.move_time > bullet_move_interval:
					if bullet.move(self.level_map):
						# Bestimme die neue Position des Geschosses für das Update-Rect
						new_rect = pygame.Rect(bullet.position[0], bullet.position[1], bullet.width, bullet.height)

						# Füge sowohl das alte als auch das neue Rect zu updated_rects hinzu
						self.updated_rects.append(old_rect)
						self.updated_rects.append(new_rect)

						if RENDER:
							self.screen.blit(bullet_image, bullet.position)
						bullet.move_time = pygame.time.get_ticks()
					else:
						# Das Geschoss muss entfernt werden, füge das alte Rect hinzu
						self.updated_rects.append(old_rect)
						opponent.bullets.remove(bullet)

				# Überprüfung auf Kollision mit dem Spieler
				if bullet.check_bullet_collision(self.player_position):
					# Füge das Rect des Geschosses bei Kollision hinzu
					self.updated_rects.append(pygame.Rect(bullet.position[0], bullet.position[1], bullet.width, bullet.height))

					if RENDER:
						message_rect = pygame.Rect(0, screen_height // 2 - 30, screen_width, 60)
						pygame.draw.rect(self.screen, BLACK, message_rect)
						render_text_center("Spieler gestorben", font, WHITE, self.screen, screen_height // 2)
						pygame.display.update([message_rect])
					pygame.time.delay(1000)
					return True  # Ends the game

	# def redraw_updated_areas(self):
	# 	# Zeichnet nur die geänderten Teile des Levels
	# 	draw_level_partially(self.screen, self.level_map, [])
	# 	self.screen.blit(player_image, self.player_position)
	# 	for coin_pos in self.coin_positions:
	# 		self.screen.blit(coin_image, coin_pos)
	# 	if self.exit_position:
	# 		self.screen.blit(end_image, self.exit_position)
	# 	for opponent in self.opponents:
	# 		self.screen.blit(opponent_image, opponent.position)
	# 	for bullet in self.opponent_bullets:
	# 		self.screen.blit(bullet_image, bullet.position)
	# 	pygame.display.update()

	def redraw_updated_areas(self):
		print("Updating rects:", self.updated_rects)
		for rect in self.updated_rects:
			print("Updating rect:", rect)
			pygame.display.update(rect)
		self.updated_rects.clear()

	def reset(self):
		self.initialize_game()
		initial_observation = pygame.surfarray.array3d(pygame.display.get_surface())
		return initial_observation

	def render(self, mode='human'):
		if not RENDER:
			return
		if mode == 'human':
			pygame.display.flip()
			self.clock.tick(60)

	def close(self):
		if RENDER:
			pygame.quit()

	def calculate_reward(self):
		reward = 0
		if self.coins_collected > 0:
			reward += self.coins_collected * 5  # Belohnung für das Sammeln von Münzen

		# Belohnung für das Erreichen des Endes, wenn alle Münzen gesammelt wurden
		if self.player_position == self.exit_position and not self.coin_positions:
			reward += 10  # Spieler hat das Ziel erreicht und alle Münzen gesammelt

		# Überprüfe Kollisionen mit Gegnern und Geschossen
		for opponent in self.opponents:
			if self.player_position == opponent.position:
				reward -= 5  # Strafe für das Laufen in einen Gegner
				break  # Verlasse die Schleife, da die Kollision bereits erkannt wurde

		for bullet in opponent.bullets:
			if bullet.check_bullet_collision(self.player_position):
				reward -= 3  # Strafe für das Getroffenwerden von einem Geschoss
				opponent.bullets.remove(bullet)  # Entferne das Geschoss, nachdem es den Spieler getroffen hat
				break  # Verlasse die Schleife, da die Kollision bereits erkannt wurde

		return reward

	def check_if_done(self):
		# Das Spiel endet, wenn der Spieler die Endposition erreicht und alle Münzen gesammelt hat
		if self.player_position == self.exit_position and not self.coin_positions:
			return True

		# Das Spiel endet auch, wenn der Spieler von einem Gegner oder einem Geschoss getroffen wird
		for opponent in self.opponents:
			if self.player_position == opponent.position:
				return True  # Der Spieler läuft in einen Gegner
			for bullet in opponent.bullets:
				if bullet.check_bullet_collision(self.player_position):
					return True  # Der Spieler wird von einem Geschoss getroffen

		return False  # Das Spiel ist noch nicht beendet