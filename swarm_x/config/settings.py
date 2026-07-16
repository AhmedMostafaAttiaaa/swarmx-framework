from dataclasses import dataclass, field
@dataclass
class Settings:
    providers: dict = field(default_factory=dict); agents: dict = field(default_factory=dict)

