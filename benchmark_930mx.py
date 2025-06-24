import gym
import pybullet_envs
import numpy as np
from power_monitor import LegacyGPUMonitor
from policy_930mx import LowVRAMPolicy
from s3_governance import S3Governance

def run_benchmark():
    env = gym.make('ReacherBulletEnv-v0')
    policy = LowVRAMPolicy('ReacherBulletEnv-v0')
    energy_mon = LegacyGPUMonitor()
    s3 = S3Governance(veto_threshold=0.15)
    total_episodes = 50
    success_count = 0
    adaptation = []

    energy_mon.start()
    for ep in range(total_episodes):
        obs = env.reset()
        done = False
        episode_success = False
        while not done:
            action = policy.predict(obs)
            if s3.check_action(action, obs):
                obs, reward, done, _ = env.step(action)
                if reward >= 0.8:
                    episode_success = True
            else:
                action = env.action_space.sample()
            energy_mon.update()
        if episode_success:
            success_count += 1
        if ep % 5 == 0:
            adaptation.append(success_count / (ep + 1))

    total_energy = energy_mon.get_energy()
    eta = success_count / total_energy if total_energy > 0 else 0

    print(f"\nBenchmark Results (930MX):")
    print(f"Success Rate: {success_count/total_episodes:.2f}")
    print(f"Estimated Energy Efficiency: {eta:.4f} successes/J")
    print(f"CCI: {s3.cci:.2f}")
    print(f"Adaptation Trend: {adaptation[-5:]}")
    env.close()

if __name__ == "__main__":
    run_benchmark()
