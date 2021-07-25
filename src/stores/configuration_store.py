import dataclasses

@dataclasses.dataclass
class ConfigurationStore:
    autorun: dict
    launcher: dict
    profile: dict
