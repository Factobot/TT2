from direct.showbase.ShowBase import ShowBase
from toontown.toonbase.ToontownLoader import ToontownLoader
from toontown.toongui.LoadingScreen import LoadingScreen
from direct.showbase.Transitions import Transitions
from toontown.toonbase.AudioManager import AudioManager
import time, sys

class ToonBase(ShowBase, AudioManager):
    
    def __init__(self, *args, **kwArgs):
        ShowBase.__init__(self, args, kwArgs)
        AudioManager.__init__(self)

        self.loader = ToontownLoader(self)
        self.accept('f1', self.takeScreenShot)
    
    def openMainWindow(self, *args, **kwArgs):
        ShowBase.openMainWindow(self, *args, **kwArgs)
        
        if not self.win:
            raise Exception('Toonbase: Failed to openMainWindow!')
        
        if config.GetBool('want-disable-mouse', False):
            self.disableMouse()
    
    def createToonBase(self):
        self.loadingScreen = LoadingScreen()
        self.loadingScreen.enter()

        self.loadMusic('stage_3/audio/bgm/TT_Theme.mp3', True, volume=0.6)

    def loadMusic(self, musicFile, wantLoop, volume=0):
        AudioManager.playMusic(self, musicFile, wantLoop, volume)
    
    def takeScreenShot(self):
        self.prefix = config.GetString('screenshot-prefix', 'toontown')
        self.screenshot(namePrefix='%s-%d' % (self.prefix, int(time.time())))