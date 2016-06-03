from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from panda3d.core import *
from pandac.PandaModules import *
from toontown.toongui.Intro import *
from toontown.toonbase import TTLocalizer, ToontownGlobals

class LoadingScreen(Intro):

    def __init__(self):
        self.canClick = False
        self.background = OnscreenImage( 
            image = loader.loadTexture("stage_3/maps/t2_gui_loadingBg.jpg"),
            scale = Vec3(1,1,1)
        )
        self.background.reparentTo(render2dp)
        self.background.hide()
        self.logo = DirectButton(
            relief=None,
            image = loader.loadTexture("stage_3/maps/t2_logo.png"),
            scale = Vec3(1.3,1,0.5)
        )
        self.loadingAsset = OnscreenImage(
            image = loader.loadTexture("stage_3/maps/t2_gui_loadingAsset.png"),
            scale = Vec3(1,1,1),
            #pos = (-0.1,0,0.1)
        )
        self.loadingAsset.reparentTo(aspect2dp)
        self.loadingAsset.hide()
        self.loadingAsset.setTransparency(TransparencyAttrib.MAlpha)
        self.logo.reparentTo(aspect2dp)
        self.logo.setTransparency(TransparencyAttrib.MAlpha)
        self.logo.hide()
        self.assetSpinIval = Sequence(
            self.loadingAsset.hprInterval(10, Vec3(0,0,360), blendType='easeOut'),
            self.loadingAsset.hprInterval(10, Vec3(0,0,0), blendType='easeInOut')
        )
        self.clickToPlay = OnscreenText(text=TTLocalizer.ClickToPlay,
            font=ToontownGlobals.getMickeyFont(),
            fg=(1,1,0,1),
            parent=aspect2dp,
            pos=(0,-0.95)
        )
        self.clickToPlay.hide()
        self.logoIv1 = Sequence(
            self.logo.scaleInterval(0.7, Vec3(1.34,1.04,0.54)),
            self.logo.scaleInterval(0.7, Vec3(1.3,1,0.5))
        )

        Intro.__init__(self)
        
    def enablePlay(self, avList):
        self.clickToPlay.show()
        self.logoIv1.loop()
        self.logo.bind(DGG.B1CLICK, self.__handleLogoClick, [avList])
        
    def __handleLogoClick(self, avList, e):
        if self.canClick == False:
            return

        base.cr.removeLoadingScreen()
        base.cr._handleLoginDone(avList)
        
    def enter(self):
        Intro.enter(self)
        self.background.show()
        self.logo.show()
        self.loadingAsset.show()
        self.assetSpinIval.loop()
    
    def exit(self):
        Intro.exit(self)
        self.background.hide()
        self.logo.hide()
        self.loadingAsset.hide()
        self.assetSpinIval.finish()
        self.clickToPlay.hide()
        self.logoIv1.finish()
        
        