import json, logging
class JsonLogger:
    def __init__(self, name="swarm_x"): self.logger=logging.getLogger(name)
    def info(self, message, **fields): self.logger.info(json.dumps({"message":message, **fields}, default=str))

