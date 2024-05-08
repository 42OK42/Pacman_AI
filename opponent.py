# opponent.py
from game_functions import is_walkable, coin_positions, move_opponent
import random
import pygame

clock = pygame.time.Clock()
opponent_move_time = 0

def move_opponent_randomly(position, level_map):
	directions = ['up', 'down', 'left', 'right']
	random.shuffle(directions)  # Zufällige Reihenfolge der Richtungen
	for direction in directions:
		new_position = move_opponent(position, direction)
		if is_walkable(new_position, level_map, len(coin_positions)):
			return new_position
	return None

def check_collision(player_position, opponent_position):
	# Prüfen, ob die Positionen identisch sind
	return player_position == opponent_position


