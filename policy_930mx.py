import torch
from stable_baselines3 import PPO

class LowVRAMPolicy:
    def __init__(self, env_name):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = PPO("MlpPolicy", env_name, device=self.device,
                         policy_kwargs={"net_arch": [64, 64]})
    def predict(self, obs):
        with torch.no_grad():
            action, _ = self.model.predict(obs, deterministic=True)
        return action
