from direct.gui.DirectGui import *
from panda3d.core import *
from direct.interval.IntervalGlobal import *
from direct.actor.Actor import *
from toontown.toon import Toon, ToonHead

import random

class ProgressLoadingScreen:
    def __init__(self, toon, doneEvent):
        self.toon = toon
        self.intervals = []
        
    def load(self):
        self.lsNodeWide = render2dp.attachNewNode("LS_WIDE_NODE")
        self.lsNodeRegular = aspect2dp.attachNewNode("LS_REGULAR_NODE")
        self.background = OnscreenImage(
            image = "stage_3/maps/t2_gui_ls_space.png",
            parent = self.lsNodeWide
        )
        self.stars = OnscreenImage(
            image = "stage_3/maps/t2_gui_ls_stars.png",
            parent = self.background
        )
        self.stars.setTransparency(TransparencyAttrib.MAlpha)
        self.starsBlinkIv = Sequence(
            self.stars.colorInterval(3, (1,1,1,0.2)),
            self.stars.colorInterval(3, (1,1,1,1))
        )
        self.loadingBar = DirectWaitBar(
            parent = self.lsNodeWide,
            scale = (0.8,0,0.3),
            pos = (0,0,-0.9),
            barTexture = loader.loadTexture("stage_3/maps/t2_gui_ls_btex.jpg"),
            barColor = Vec4(1,1,1,1),
            value = 50
        )
        self.firstPlanet = self.createPlanet(1, scale=0.05, pos=(base.a2dTopRight.getX()-0.2,0,base.a2dTopRight.getZ()-0.2))
        self.secondPlanet = self.createPlanet(3, scale=0.15, pos=(base.a2dTopLeft.getX()+0.2,0,0.3))
        self.thirdPlanet = self.createPlanet(2, scale=0.25, pos=(0,0,-0.1))
        self.lsNodeWide.hide()
        self.lsNodeRegular.hide()
        
    def do360(self, p, extra):
        p.hprInterval(30 + extra, (0, 0, p.getR() + 360)).start()
        
    def createPlanet(self, planetId, **kw):
        p = OnscreenImage(
            image = "stage_3/maps/t2_gui_ls_p%s.png" %planetId,
            parent = self.lsNodeRegular,
            **kw
        )
        p.setTransparency(TransparencyAttrib.MAlpha)
        extra = random.random() * 20
        print extra
        self.intervals.append(Sequence(
            Func(self.do360, p, extra),
            Wait(30 + extra)
        ))
        return p
        
    def enter(self):
        self.lsNodeWide.show()
        self.lsNodeRegular.show()
        self.starsBlinkIv.loop()
        for interval in self.intervals:
            interval.loop()
        