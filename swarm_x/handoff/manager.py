from .schemas import Handoff
class HandoffManager:
    def resolve(self, source, output):
        return Handoff(source, output.next_agent, output.handoff_message, output.handoff_reason) if output.next_agent else None

