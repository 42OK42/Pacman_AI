# opponent.py
from game_functions import is_walkable, calculate_direction, coin_positions, calculate_new_position_opponent
import globals
from bullet import Bullet, bullets
from settings import bullet_speed
import random
import pygame

clock = pygame.time.Clock()

def opposite_direction(direction):
	if direction == 'up':
		return 'down'
	elif direction == 'down':
		return 'up'
	elif direction == 'left':
		return 'right'
	elif direction == 'right':
		return 'left'

def is_at_crossroads(position, level_map):
	directions = ['up', 'down', 'left', 'right']
	print("Hallo")
	if globals.current_direction_opponent:
		directions.remove(globals.current_direction_opponent)
		directions.remove(opposite_direction(globals.current_direction_opponent))
	walkable_directions = 0
	for direction in directions:
		new_position = calculate_new_position_opponent(position, direction)
		if is_walkable(new_position, level_map, len(coin_positions)):
			walkable_directions += 1
	return walkable_directions > 0

# def line_of_sight(start, end, level_map):
# 	""" Prüft, ob eine klare Sichtlinie zwischen zwei Punkten besteht, unter Verwendung des Bresenham-Algorithmus. """
# 	x0, y0 = start
# 	x1, y1 = end
# 	dx = abs(x1 - x0)
# 	dy = -abs(y1 - y0)
# 	sx = 1 if x0 < x1 else -1
# 	sy = 1 if y0 < y1 else -1
# 	err = dx + dy
# 	while True:
# 		if not is_walkable((x0, y0), level_map, len(coin_positions)):
# 			return False
# 		if (x0 == x1) and (y0 == y1):
# 			return True
# 		e2 = 2 * err
# 		if e2 >= dy:
# 			err += dy
# 			x0 += sx
# 		if e2 <= dx:
# 			err += dx
# 			y0 += sy

def line_of_sight(start, end, level_map):
	x0, y0 = start
	x1, y1 = end

	# Bestimmt die Richtung der Überprüfung
	if x0 == x1:  # Vertikale Linie
		step = 1 if y1 > y0 else -1
		for y in range(y0 + step, y1, step):
			if not is_walkable((x0, y), level_map, len(coin_positions)):
				return False
	elif y0 == y1:  # Horizontale Linie
		step = 1 if x1 > x0 else -1
		for x in range(x0 + step, x1, step):
			if not is_walkable((x, y0), level_map, len(coin_positions)):
				return False
	else:
		return False  # Keine direkte horizontale oder vertikale Linie

	return True

def is_at_dead_end(position, level_map):
	"""Prüft, ob der Gegner in einer Sackgasse steckt, indem er alle möglichen Richtungen überprüft."""
	possible_directions = ['up', 'down', 'left', 'right']
	possible_moves = 0

	for direction in possible_directions:
		new_position = calculate_new_position_opponent(position, direction)
		if is_walkable(new_position, level_map, len(coin_positions)):
			possible_moves += 1

	return possible_moves == 1  # Nur eine mögliche Bewegungsrichtung

def move_opponent_smartly(opponent_position, player_position, level_map, bullets):
	global last_seen_player_position

	direction_to_move = None

	if line_of_sight(opponent_position, player_position, level_map):
		print("Sichtkontakt")
		globals.last_seen_player_position = player_position
		direction_to_move = calculate_direction(opponent_position, player_position)
		bullets.append(Bullet(opponent_position, direction_to_move, bullet_speed//100))
		print ("Bullet fired")
	elif globals.last_seen_player_position:
		direction_to_move = calculate_direction(opponent_position, globals.last_seen_player_position)
		if opponent_position == globals.last_seen_player_position:
			globals.last_seen_player_position = None

	if direction_to_move and is_walkable(calculate_new_position_opponent(opponent_position, direction_to_move), level_map, len(coin_positions)):
		return calculate_new_position_opponent(opponent_position, direction_to_move)
	else:
		return move_opponent_randomly(opponent_position, level_map)

def move_opponent_randomly(position, level_map):
	directions = ['up', 'down', 'left', 'right']
	new_position = position  # Startposition als Fallback

	if globals.current_direction_opponent:
		# Berechne die potenzielle neue Position in der aktuellen Richtung
		potential_new_pos = calculate_new_position_opponent(position, globals.current_direction_opponent)
		if is_walkable(potential_new_pos, level_map, len(coin_positions)):
			# Wenn die aktuelle Richtung begehbar ist und keine Kreuzung vorliegt, weiter in dieser Richtung
			if not is_at_crossroads(position, level_map):
				new_position = potential_new_pos
			else:
				# An einer Kreuzung: Wähle eine neue begehbare Richtung
				random.shuffle(directions)
				for direction in directions:
					potential_new_pos = calculate_new_position_opponent(position, direction)
					if is_walkable(potential_new_pos, level_map, len(coin_positions)):
						globals.current_direction_opponent = direction
						new_position = potential_new_pos
						break
		else:
			# Aktuelle Richtung nicht begehbar: Wähle eine neue Richtung
			random.shuffle(directions)
			for direction in directions:
				potential_new_pos = calculate_new_position_opponent(position, direction)
				if is_walkable(potential_new_pos, level_map, len(coin_positions)):
					globals.current_direction_opponent = direction
					new_position = potential_new_pos
					break

	return new_position

def check_collision(player_position, opponent_position):
	# Prüfen, ob die Positionen identisch sind
	if player_position == opponent_position:
		return True
	return False

def check_bullet_collision(player_position, bullet_position):
	if bullet_position == player_position:
		return True
	return False


