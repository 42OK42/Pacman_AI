from stable_baselines3 import PPO

def train_agent():
	env = CustomGameEnv()
	model = PPO("CnnPolicy", env, verbose=1)
	model.learn(total_timesteps=10000)
	model.save("ppo_pacman")

	del model  # Lösche das Modell, um es später wieder zu laden

if __name__ == "__main__":
	train_agent()