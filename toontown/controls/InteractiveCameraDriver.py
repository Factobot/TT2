from panda3d.core import *
from direct.showbase.DirectObject import *

CameraFactor = 0.3
PITCH_LIMIT = 10

class InteractiveCameraDriver(DirectObject):
    
    def __init__(self, camera, cameraColl = True):
        self.camera = camera
        self.cameraCollisions = cameraColl
        self.safePointerData = (0, 0, 250)
        self.heading = 0
        self.pitch = 0
        self.target = None
        
    def setup(self):
        self.cameraParent = render.attachNewNode("cameraParent")
        self.cameraParent.setEffect(CompassEffect.make(render))
        self.camera.reparentTo(self.cameraParent)
        self.camera.lookAt(self.cameraParent)
        
    def setTarget(self, target):
        if not hasattr(self, "cameraParent"):
            print "Must setup camera before setting a target!"
            return

        self.target = target
        self.cameraParent.reparentTo(self.target)
        
    def start(self):
        taskMgr.add(self.__cameraControlTask, "InteractiveCameraControlTask")
        base.win.movePointer(*self.safePointerData)
        
    def stop(self):
        taskMgr.remove("InteractiveCameraControlTask")
        
    def __cameraControlTask(self, task):
        mouseD = base.win.getPointer(0)
        x = mouseD.getX()
        y = mouseD.getY()
        
        if base.win.movePointer(0, 200, 200):
            self.heading -= (x - 200) * CameraFactor
            self.pitch -= (y - 200) * CameraFactor

            if self.pitch > self.PITCH_LIMIT:
                self.pitch = self.PITCH_LIMIT
                
        self.cameraParent.setHpr(self.heading, self.pitch, 0)
        
        return task.cont