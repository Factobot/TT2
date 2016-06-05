from direct.controls.ControlManager import *
from direct.showbase.InputStateGlobal import inputState

class ToontownControlManager(ControlManager):
    
    def __init__(self, *args):
        ControlManager.__init__(self, args)
        
    def enable(self):
        if self.isEnabled:
            assert self.notify.debug('already isEnabled')
            return
        
        self.isEnabled = 1
        ist = self.inputStateTokens
        inputState.watch("forward", "w", "w-up", inputSource=inputState.WASD)
        inputState.watch("reverse", "s", "s-up", inputSource=inputState.WASD)
        inputState.watch("turnLeft", "a", "a-up", inputSource=inputState.WASD)
        inputState.watch("turnRight", "d", "d-up", inputSource=inputState.WASD)
        inputState.watch("jump", "space", "space-up", inputSource=inputState.WASD)
        
        if self.currentControls:
            self.currentControls.enableAvatarControls()