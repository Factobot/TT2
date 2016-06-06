from panda3d.core import *
from toontown.toon.ToonDNA import *

class MakeAToon:

    def __init__(self, slot, doneEvent):
        self.slot = slot
        self.doneEvent = doneEvent
        
    def skipMakeAToon(self):
        name = 'Skid'
        dna = ToonDNA()
        messenger.send(self.doneEvent, [self.slot, name, dna])

    def enter(self):
        self.skipMakeAToon()
        return
        base.audioManager.stopMusic()
        base.playMusic('stage_3/audio/bgm/MAT_Theme.mp3', True, volume=0.6)

    def exit(self):
        base.audioManager.stopMusic()