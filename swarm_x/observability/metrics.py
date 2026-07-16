from collections import Counter
class Metrics:
    def __init__(self): self.counts=Counter(); self.latencies=[]
    def increment(self, name, value=1): self.counts[name] += value
    def snapshot(self): return {"counts": dict(self.counts), "latencies": list(self.latencies)}

