from direct.gui.DirectGui import *
from panda3d.core import *

class Intro:
    def __init__(self):
        self.curtain = OnscreenImage(
            image = "stage_3/maps/t2_gui_curtain.jpg",
        )
        self.curtain.reparentTo(render2dp)
        self.curtain.stash(50)
        
    def enter(self):
        pass#self.curtain.unstash(50)