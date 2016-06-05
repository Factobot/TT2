from panda3d.core import *
from direct.showbase.DirectObject import *

CameraFactor = 0.3

class InteractiveCameraDriver(DirectObject):
    PITCH_LIMIT = 10
    def __init__(self, camera, cameraColl = True):
        self.camera = camera
        self.cameraCollisions = cameraColl
        self.safePointerData = (0, 0, 250)
        self.mouseCoords = [0,0]
        self.target = None
        self.wantControl = False
        
    def setTarget(self, target):
        self.target = target
        if self.target:
            self.cameraParent = self.target.attachNewNode("cameraParent")
            self.camera.reparentTo(self.cameraParent)
            self.camera.lookAt(self.cameraParent)
        
    def start(self):
        self.accept("m", self.__handlePressMouse)
        taskMgr.add(self.__cameraControlTask, "InteractiveCameraControlTask")
        
    def __handlePressMouse(self):
        self.wantControl = not self.wantControl
        if self.wantControl:
            self.mouseCoords = [base.win.getPointer(0).getX(), base.win.getPointer(0).getY()]
            props = WindowProperties()
            props.setCursorHidden(True)
            base.win.requestProperties(props)
        else:
            props = WindowProperties()
            props.setCursorHidden(False)
            base.win.requestProperties(props)
        
    def stop(self):
        self.ignore("m")
        self.wantControl = False
        taskMgr.remove("InteractiveCameraControlTask")
        
    # todo: rotate avatar with camera change
    def __cameraControlTask(self, task):
        if self.wantControl:
            mouseD = base.win.getPointer(0)
            x = mouseD.getX()
            y = mouseD.getY()
            
            heading = self.cameraParent.getH()
            pitch = self.cameraParent.getP()
            if base.win.movePointer(0, self.mouseCoords[0], self.mouseCoords[1]):
                heading -= (x - self.mouseCoords[0]) * CameraFactor
                pitch -= (y - self.mouseCoords[1]) * CameraFactor

                if pitch > self.PITCH_LIMIT:
                    pitch = self.PITCH_LIMIT
                    
            self.cameraParent.setHpr(heading, pitch, 0)
        
        return task.cont