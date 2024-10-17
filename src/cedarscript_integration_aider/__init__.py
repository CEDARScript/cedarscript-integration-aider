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
    def __init__(self, cedarscript_prompts):
        self.cedarscript_prompts: CEDARScriptPromptsBase = cedarscript_prompts

    def __getattr__(self, name):
        result = getattr(self.cedarscript_prompts, name)
        # if name != 'edit_format_training':
        #     print(f"[__getattr__] {name} = {result}")
        # if name == 'edit_format_name':
        #     print(f'edit_format_name: {result()}')
        return result
