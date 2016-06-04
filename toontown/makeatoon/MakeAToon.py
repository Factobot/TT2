from panda3d.core import *

class MakeAToon:

    def __init__(self, doneEvent):
        self.doneEvent = doneEvent

    def enter(self):
        base.audioManager.stopMusic()
        base.playMusic('stage_3/audio/bgm/MAT_Theme.mp3', True, volume=0.6)

    def exit(self):
        base.audioManager.stopMusic()