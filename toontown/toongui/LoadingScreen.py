from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from panda3d.core import *

from toontown.toongui.Intro import *

class LoadingScreen(Intro):

    def __init__(self):
        self.background = OnscreenImage( 
            image = loader.loadTexture("stage_3/maps/t2_gui_loadingBg.jpg"),
            parent = render2dp,
            scale = Vec3(1,1,1)
        )
        self.background.hide()
        self.logo = OnscreenImage(
            image = loader.loadTexture("stage_3/maps/t2_logo.png"),
            scale = Vec3(1.3,1,0.5)
        )
        self.logo.reparentTo(aspect2dp)
        self.logo.setTransparency(TransparencyAttrib.MAlpha)
        self.logo.hide()
        self.loadingAsset = OnscreenImage(
            image = loader.loadTexture("stage_3/maps/t2_gui_loadingAsset.png"),
            scale = Vec3(1,1,1),
            #pos = (-0.1,0,0.1)
        )
        self.loadingAsset.reparentTo(self.background)
        self.loadingAsset.hide()
        self.loadingAsset.setTransparency(TransparencyAttrib.MAlpha)
        self.assetSpinIval = Sequence(
            self.loadingAsset.hprInterval(10, Vec3(0,0,360), blendType='easeOut'),
            self.loadingAsset.hprInterval(10, Vec3(0,0,0), blendType='easeInOut')
        )
        Intro.__init__(self)
        
    def enter(self):
        Intro.enter(self)
        self.background.show()
        self.logo.show()
        self.loadingAsset.show()
        self.assetSpinIval.loop()
    
    def exit(self):
        self.background.hide()
        self.logo.hide()
        self.loadingAsset.hide()
        self.assetSpinIval.finish()
        
        