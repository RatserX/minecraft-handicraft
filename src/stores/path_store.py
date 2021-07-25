import dataclasses
import os
import sys

@dataclasses.dataclass
class PathStore:
    base_directory: str = sys.path[0]
    home_directory: str = os.path.abspath(os.sep)

    def get_public_configuration_directory() -> str:
        return os.path.join(PathStore.base_directory, "../public/configuration")

    def get_public_data_directory() -> str:
        return os.path.join(PathStore.base_directory, "../public/data")

    def get_public_log_directory() -> str:
        return os.path.join(PathStore.base_directory, "../public/log")

    def get_public_profile_directory() -> str:
        return os.path.join(PathStore.base_directory, "../public/profile")
