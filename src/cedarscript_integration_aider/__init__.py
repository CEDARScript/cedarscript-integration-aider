from .cedarscript_prompts_g import CEDARScriptPromptsGrammar
from .cedarscript_prompts_rw import CEDARScriptPromptsRW
from .cedarscript_prompts_w import CEDARScriptPromptsW
from ._version import __version__

__all__ = [
    "__version__",
    "CEDARScriptPromptsAdapter",
    "CEDARScriptPromptsGrammar",
    "CEDARScriptPromptsRW",
    "CEDARScriptPromptsW"
]

class CEDARScriptPromptsAdapter:
    def __init__(self, cedarscript_prompts, base_prompts):
        self.cedarscript_prompts: CEDARScriptPromptsBase = cedarscript_prompts
        self.base_prompts = base_prompts

    def __getattribute__(self, name):
        cedarscript_prompts = super().__getattribute__('cedarscript_prompts')
        if hasattr(cedarscript_prompts, name):
            return getattr(cedarscript_prompts, name)

        base_prompts = super().__getattribute__('base_prompts')
        return getattr(base_prompts, name)
