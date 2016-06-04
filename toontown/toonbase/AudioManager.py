from panda3d.core import *

class AudioManager:

    def __init__(self):
        self.currentPlaying = None
        self.isPlaying = False

    def playMusic(self, musicName, wantLoop, volume):
        self.currentPlaying = loader.loadSfx(musicName)
        self.currentPlaying.setLoop(wantLoop)

        if volume > 0:
            self.currentPlaying.setVolume(volume)

        if self.isPlaying == False:
            self.isPlaying = True
            self.currentPlaying.play()

    def stopMusic(self):
        if self.currentPlaying != None and self.isPlaying == True:
            self.currentPlaying.stop()

        self.currentPlaying = None
        self.isPlaying = False