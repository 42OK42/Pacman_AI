from game_functions import calculate_new_position_opponent, is_walkable
from settings import bullet_speed
from globals import coin_positions

bullets = [] # Liste, um alle Kugeln zu speichern

class Bullet:
	def __init__(self, position, direction, speed):
		self.position = position
		self.direction = direction
		self.speed = speed

	def move(self, level_map):
		"""Bewegt die Kugel basierend auf ihrer Richtung und Geschwindigkeit."""
		for _ in range(self.speed):
			new_position = calculate_new_position_opponent(self.position, self.direction)
			if is_walkable(new_position, level_map, len(coin_positions)):
				self.position = new_position
			else:
				return False  # Kugel trifft auf ein Hindernis
		return True