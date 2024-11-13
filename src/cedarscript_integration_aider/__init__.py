from ._version import __version__
from importlib.resources import files
from pathlib import Path


__all__ = [
    "__version__",
    "prompt_folder_path",
]

prompt_folder_path = files('cedarscript_integration_aider')
