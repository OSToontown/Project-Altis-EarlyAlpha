from direct.fsm import ClassicFSM, State
from toontown.toonbase.ToontownGlobals import OptionsPageHotkey
from toontown.toontowngui import TTDialog

class FeatureComingSoonDialog:

    def __init__(self):
        self.dialog = TTDialog.TTGlobalDialog(
            dialogName='ControlRemap', doneEvent='exitDialog', style=TTDialog.Acknowledge,
            text="Woah! That feature will enabled in \n\1textShadow\1beta\2! Sorry about that!", text_wordwrap=24,
            text_pos=(0, 0, -0.8), suppressKeys = True, suppressMouse = True
        )
        self.dialog.accept('exitDialog', self.exitDialog)
        
    def exitDialog(self):
        self.dialog.cleanup()
        del self.dialog