import pynvml
import time

class LegacyGPUMonitor:
    def __init__(self):
        try:
            pynvml.nvmlInit()
            self.handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            self.has_gpu = True
        except:
            self.has_gpu = False
        self.energy = 0
        self.start_time = time.time()
        
    def start(self):
        self.energy = 0
        self.start_time = time.time()
        
    def update(self):
        try:
            if self.has_gpu:
                power_w = pynvml.nvmlDeviceGetPowerUsage(self.handle) / 1000  # W
            else:
                power_w = 30  # Worst case fallback for 930MX
        except:
            power_w = 30
        elapsed = time.time() - self.start_time
        self.energy += power_w * elapsed
        self.start_time = time.time()
        
    def get_energy(self):
        return self.energy
