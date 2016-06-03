from direct.gui.DirectGui import *
from panda3d.core import *
from direct.interval.IntervalGlobal import *

class Intro:
    def __init__(self):
        self.curtain = OnscreenImage(
            image = "stage_3/maps/t2_gui_curtain.jpg",
        )
        self.curtain.reparentTo(render2dp)
        self.curtain.setBin('gui-popup', 2)
        self.curtain.hide()
        
        self.introIval = Sequence(
            Wait(2.5),
            self.curtain.posInterval(1, (0,0,2))
        )
        
    def enter(self):
        self.curtain.show()
        self.introIval.start()
        
    def exit(self):
        self.curtain.remove()
        self.introIval.finish()