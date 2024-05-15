import pygame
from game_functions import calculate_new_position_opponent, is_walkable_player
from settings import bullet_step_size, bullet_move_interval
from globals import coin_positions

bullets = [] # Liste, um alle Kugeln zu speichern

class Bullet:
	def __init__(self, position, direction, bullet_step_size):
		self.position = position
		self.direction = direction
		self.step_size = bullet_step_size
		current_time = pygame.time.get_ticks()
		self.move_time = current_time

	def calculate_bullet_start_position(opponent_position, direction):
		x, y = opponent_position
		if direction == 'up':
			return (x, y - 0 * bullet_step_size)
		elif direction == 'down':
			return (x, y + 0 * bullet_step_size)
		elif direction == 'left':
			return (x - 0 * bullet_step_size, y)
		elif direction == 'right':
			return (x + 0 * bullet_step_size, y)
		return opponent_position  # Falls keine gültige Richtung vorliegt, geben Sie die ursprüngliche Position zurück

	def move(self, level_map):
		"""Bewegt die Kugel basierend auf ihrer Richtung und Geschwindigkeit."""
		current_time = pygame.time.get_ticks()
		if current_time - self.move_time > bullet_move_interval:
			for _ in range(self.step_size):
				#print("bullet position", self.position)
				new_position = calculate_new_position_opponent(self.position, self.direction)
				#print("new position", new_position)
				if is_walkable_player(new_position, level_map, len(coin_positions)):
					self.position = new_position
					self.move_time = current_time
				else:
					return False  # Kugel trifft auf ein Hindernis
			return True
	
	def check_bullet_collision(self, player_position):
		#print("bullet position", self.position)
		if self.position == player_position:
			return True
		return False