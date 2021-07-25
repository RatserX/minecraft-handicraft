import dataclasses

@dataclasses.dataclass
class OptionStore:
    launcher_key: str
    platform_name: str
    profile_key: str
