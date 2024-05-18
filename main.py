import pygame
from settings import BLACK, WHITE, font, tile_size, debug_opponent, win_message_background_color, info_panel_width, bullet_move_interval, background_color, LOAD_MODEL, num_parallel_models
from rendering import render_text_center, render_text
from assets import coin_image, end_image, player_image, opponent_image, bullet_image
from level import load_level, draw_level_partially
from opponent import Opponent
from settings import RENDER, AI_MODE
from game_functions import screen_width, screen_height
from custom_game_env import CustomGameEnv
from player_controlled import run_player_controlled_game
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.vec_env import SubprocVecEnv

def main():
	if AI_MODE:
		if not LOAD_MODEL:
			# Trainiere ein neues Modell
			num_envs = num_parallel_models
			vec_env = make_vec_env(lambda: CustomGameEnv(), n_envs=num_envs)
			model = PPO("MlpPolicy", vec_env, verbose=1)
			model.learn(total_timesteps=200000)
			model.save("ppo_customgame")
			vec_env.close()
		else:
			# Lade und rendere das trainierte Modell
			render_trained_model()

	else:
		run_player_controlled_game()

	env.close()  # Schließe die Umgebung, wenn das Spiel beendet wird

def render_trained_model():
	env = CustomGameEnv()
	model = PPO.load("ppo_customgame", env=env)

	obs = env.reset()
	while True:
		action, _states = model.predict(obs, deterministic=True)
		obs, rewards, done, info = env.step(action)
		env.render()
		if done:
			obs = env.reset()

if __name__ == "__main__":
	main()