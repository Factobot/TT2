from direct.showbase.ShowBase import ShowBase
from toontown.toonbase.ToontownLoader import ToontownLoader
from toontown.toongui.LoadingScreen import LoadingScreen
from direct.showbase.Transitions import Transitions
from toontown.toonbase.AudioManager import AudioManager
from toontown.toonbase import ToontownGlobals
from toontown.interaction.InteractiveObjectManager import InteractiveObjectManager
import time, sys

MaxPhaseRegular = 13
HalfPhases = ["phase_3.5", "phase_5.5"]
MaxStage = 4
class ToonBase(ShowBase, AudioManager):
    
    def __init__(self, *args, **kwArgs):
        ShowBase.__init__(self, args, kwArgs)
        self.audioManager = AudioManager()
        self.interactiveObjectMgr = InteractiveObjectManager()
        self.transitions.IrisModelName = 'phase_3/models/misc/iris'
        self.transitions.FadeModelName = 'phase_3/models/misc/fade'
        self.__mountMultifiles()
        self.loader = ToontownLoader(self)
        self.accept('f1', self.takeScreenShot)
        
    def __mountMultifiles(self):
        MountList = []
        path = config.GetString("mount-path", "")
        if path != "":
            for i in range(3, MaxPhaseRegular+1):
                MountList.append(path + "/phase_%d.mf" %i)
            for x in HalfPhases:
                MountList.append(path + "/%s.mf" %x)
            for i in range(3, MaxStage+1):
                MountList.append(path + "/stage_%d.mf" %i)
            vfs = VirtualFileSystem.getGlobalPtr()
            for m in MountList:
                vfs.mount(Filename(m), ".", VirtualFileSystem.MFReadOnly)
    
    def openMainWindow(self, *args, **kwArgs):
        ShowBase.openMainWindow(self, *args, **kwArgs)
        
        if not self.win:
            raise Exception('Toonbase: Failed to openMainWindow!')
        
        if config.GetBool('want-disable-mouse', False):
            self.disableMouse()

        self.accept('f2', self.getDoIdList)

    def getDoIdList(self):
        print (base.cr.doId2do)
    
    def createToonBase(self):
        self.camLens.setFilmSize(*ToontownGlobals.FilmSize)
        self.camLens.setFov(52.0)
        self.camLens.setFar(400.0)
        self.camLens.setNear(1.0)
        self.loadingScreen = LoadingScreen()
        self.loadingScreen.enter()

        self.playMusic('stage_3/audio/bgm/TT_Theme.mp3', True, volume=0.6)

    def playMusic(self, musicFile, wantLoop, volume=0):
        self.audioManager.playMusic(musicFile, wantLoop, volume)
    
    def takeScreenShot(self):
        self.prefix = config.GetString('screenshot-prefix', 'toontown')
        self.screenshot(namePrefix='%s-%d' % (self.prefix, int(time.time())))