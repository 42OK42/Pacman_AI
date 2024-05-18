import pygame
import random
from game_functions import calculate_direction, calculate_new_position_opponent, map_width, map_height
from bullet import Bullet
from globals import coin_positions
from level import load_level
from settings import bullet_step_size, opponent_time_to_move, tile_size, debug_opponent, debug_bullet, bullet_move_interval, shoot_interval_opponet

class OpponentManager:
	def __init__(self, level_map):
		self.level_map = level_map
		self.opponents = []

	def add_opponent(self, position, direction=None):
		new_opponent = Opponent(position, self.level_map, direction)
		self.opponents.append(new_opponent)
		return new_opponent

	def update_opponent_positions(self):
		positions = [opponent.position for opponent in self.opponents]
		for opponent in self.opponents:
			opponent.update_positions(positions)

	def move_opponents(self):
		for opponent in self.opponents:
			opponent.move_smartly(self.opponents)
			self.update_opponent_positions()

class Opponent:

	def	__init__(self, position, level_map, opponents_positions, direction=None):
		self.position = position
		self.level_map = level_map
		self.opponents_positions = opponents_positions
		self.direction = direction if direction else self.choose_random_direction()
		self.last_seen_player_position = None
		self.bullets = []
		self.Bullet = Bullet
		self.shoot_interval_opponet = shoot_interval_opponet
		self.move_time = pygame.time.get_ticks()
		self.last_shot_time = 0 # Zeitpunkt des letzten Schusses

	def update_positions(self, positions):
		self.opponents_positions = positions

	def is_walkable_opponents(self, target_pos, coins_remaining, opponents_positions):
		if (debug_opponent):
			print("check walkable", target_pos, coins_remaining, opponents_positions)
		map_x, map_y = target_pos[0] // tile_size, target_pos[1] // tile_size
		if 0 <= map_x < map_width and 0 <= map_y < map_height:
			tile = self.level_map[map_y][map_x]
			if tile == 'E' and coins_remaining == 0:
				if (debug_opponent):
					print("walkable")
				return True
			if tile in ['B', 'C', 'P', 'E'] and target_pos not in opponents_positions:
				if (debug_opponent):
					print("walkable")
				return True
		if (debug_opponent):
			print("not walkable")
		return False
	
	def choose_random_direction(self):
		directions = ['up', 'down', 'left', 'right']
		random.shuffle(directions)
		for direction in directions:
			new_position = calculate_new_position_opponent(self.position, direction)
			if self.is_walkable_opponents(new_position, len(coin_positions), [pos for pos in self.opponents_positions if pos != self.position]):
				return direction
		return None

	def is_at_dead_end(self, level_map):
		possible_directions = ['up', 'down', 'left', 'right']
		walkable_directions = 0
		for direction in possible_directions:
			new_position = calculate_new_position_opponent(self.position, direction)
			if self.is_walkable_opponents(new_position, level_map, self.position ,len(coin_positions)):
				walkable_directions += 1
		return walkable_directions == 1  # Nur eine mögliche Bewegungsrichtung

	def opposite_direction(self):
		if self.direction == 'up':
			return 'down'
		elif self.direction == 'down':
			return 'up'
		elif self.direction == 'left':
			return 'right'
		elif self.direction == 'right':
			return 'left'

	def is_at_crossroads(self, level_map):
		directions = ['up', 'down', 'left', 'right']
		if self.direction:
			directions.remove(self.direction)
			directions.remove(self.opposite_direction())
		walkable_directions = 0
		for direction in directions:
			new_position = calculate_new_position_opponent(self.position, direction)
			if self.is_walkable_opponents(new_position, len(coin_positions), self.position):
				walkable_directions += 1
		return walkable_directions > 0

	def can_move_current_direction(self):
		new_position = calculate_new_position_opponent(self.position, self.direction)
		return self.is_walkable_opponents(new_position, len(coin_positions), self.opponents_positions)

	def move_randomly(self, level_map):
		directions = ['up', 'down', 'left', 'right']
		random.shuffle(directions)
		for direction in directions:
			new_position = calculate_new_position_opponent(self.position, direction)
			if self.is_walkable_opponents(new_position, level_map, self.position ,len(coin_positions)):
				self.direction = direction
				return new_position
		return self.position

	def check_collision(self, player_position):
		if self.position == player_position:
			return True
		return False
	
	def move_smartly(self, player_position):
		#print("self.position_movesmartly", self.position)
		#print("player_position_movesmartly", player_position)
		current_time = pygame.time.get_ticks()
		moved = False
		old_position = self.position  # Speichere die alte Position für das Neuzeichnen

		if self.line_of_sight(player_position):
			self.last_seen_player_position = player_position

		if current_time - self.move_time > opponent_time_to_move:
			self.move_time = current_time
			new_position = None
			if self.last_seen_player_position:
				self.direction = calculate_direction(self.position, self.last_seen_player_position)
				new_position = calculate_new_position_opponent(self.position, self.direction)
				if self.position == self.last_seen_player_position:
					self.last_seen_player_position = None
			else:
				self.direction = self.choose_random_direction()
				new_position = calculate_new_position_opponent(self.position, self.direction)

			if new_position and self.is_walkable_opponents(new_position, len(coin_positions), self.opponents_positions):
				self.position = new_position
				moved = True
		if moved:
			return old_position, self.position
		else:
			return None

	def try_shoot(self, player_position, current_time, updated_rects):
		#current_time = pygame.time.get_ticks()
		if self.line_of_sight(player_position) and (current_time - self.last_shot_time > self.shoot_interval_opponet):
			self.last_shot_time = current_time
			self.last_seen_player_position = player_position
			bullet = self.fire_bullet(updated_rects)
			return True
		return False

	def line_of_sight(self, player_position):
		x0, y0 = self.position
		x1, y1 = player_position

		if x0 == x1:  # Vertikale Linie
			step = 1 if y1 > y0 else -1
			for y in range(y0 + step, y1, step):
				if not self.is_walkable_opponents((x0, y), len(coin_positions), self.opponents_positions):
					return False
		elif y0 == y1:  # Horizontale Linie
			step = 1 if x1 > x0 else -1
			for x in range(x0 + step, x1, step):
				if not self.is_walkable_opponents((x, y0), len(coin_positions), self.opponents_positions):
					return False
		else:
			return False  # Keine direkte Linie, daher keine Sichtlinie

		return True  # Keine Hindernisse gefunden, Sichtlinie ist klar

	def fire_bullet(self, updated_rects):
		print("self.position", self.position)
		print("self.last_seen_player_position", self.last_seen_player_position)
		direction = calculate_direction(self.position, self.last_seen_player_position)
		print("self.position", self.position)
		print("direction", direction)
		bullet_start_position = Bullet.calculate_bullet_start_position(self.position, direction)
		print("bullet_start_position", bullet_start_position)
		new_bullet = Bullet(bullet_start_position, direction, bullet_step_size // 100)
		bullet_rect = pygame.Rect(new_bullet.position[0], new_bullet.position[1], tile_size, tile_size)
		updated_rects.append(bullet_rect)
		print("bullet_start_position", bullet_start_position)
		self.bullets.append(new_bullet)