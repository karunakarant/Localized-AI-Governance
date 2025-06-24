import numpy as np

class S3Governance:
    def __init__(self, veto_threshold=0.15):
        self.threshold = veto_threshold
        self.veto_count = 0
        self.total_actions = 0
    
    def check_action(self, action, obs):
        action_norm = np.linalg.norm(action)
        confidence = 1 / (1 + np.exp(-action_norm))  # Sigmoid
        self.total_actions += 1
        if confidence < self.threshold:
            self.veto_count += 1
            return False
        return True
    
    @property
    def cci(self):
        return 1 - (self.veto_count / max(self.total_actions, 1))
