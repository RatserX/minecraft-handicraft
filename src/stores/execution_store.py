import dataclasses
import subprocess

@dataclasses.dataclass
class ExecutionStore:
    directory: str
    subprocesses: dict[str, subprocess.Popen]
