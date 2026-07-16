from .base import Skill
class SkillRegistry:
    def __init__(self, skills=None): self._skills = {s.name: s for s in skills or []}
    def register(self, skill: Skill): self._skills[skill.name] = skill
    def get(self, name): return self._skills[name]
    def all(self): return list(self._skills.values())
