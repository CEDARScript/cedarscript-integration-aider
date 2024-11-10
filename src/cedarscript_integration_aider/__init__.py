from ._version import __version__
from importlib.resources import files
from pathlib import Path


__all__ = [
    "__version__",
    "prompt_folder_path",
]

def prompt_folder_path(name: str) -> Path:
    result = files('cedarscript_integration_aider').joinpath(name)
    assert result.exists(), f"[prompt_folder_path '{name}']: Path not found: {result}"
    return result
