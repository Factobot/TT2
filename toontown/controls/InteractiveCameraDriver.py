from panda3d.core import *
from direct.showbase.DirectObject import *
from direct.task.Task import Task

class InteractiveCameraDriver(DirectObject):
    PITCH_LIMIT_TOP = -50
    PITCH_LIMIT_BOT = 10
    MAX_CAM_DISTANCE = 8.5
    MIN_CAM_DISTANCE = 0
    CameraFactor = 0.3

    def __init__(self, camera, cameraColl = True):
        self.camera = camera
        self.cameraCollisions = cameraColl
        self.safePointerData = (0, 0, 250)
        self.mouseCoords = [0,0]
        self.target = None
        self.wantControl = False
        self.canControlCam = False
        self.canZoom = False
        
    def setTarget(self, target):
        self.target = target
        if self.target:
            self.cameraParent = self.target.attachNewNode('cameraParent')
            self.camera.reparentTo(self.cameraParent)
            self.camera.lookAt(self.cameraParent)
        
    def start(self):
        self.accept('m', self.__handlePressMouse)
        self.accept('=' or '+', self.__handleCameraIn)
        self.accept('-', self.__handleCameraOut)
        self.accept('r', self.__resetCameraPos)
        taskMgr.add(self.__cameraControlTask, 'InteractiveCameraControlTask')
        taskMgr.add(self.__updateCanControl, 'UpdateCan_InteractiveCameraControlTask')
        
    def __handlePressMouse(self):
        if self.canControlCam:
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

    def __resetCameraPos(self):
        self.cameraParent.setPosHpr(0,0,0,0,0,0)

    def __updateCanControl(self, task):
        if self.target.getY(self.cameraParent) == InteractiveCameraDriver.MIN_CAM_DISTANCE:

            if self.cameraParent.getHpr() == Vec3(0,0,0) and self.cameraParent.getPos() == Vec3(0,0,0):
                self.canControlCam = True
                self.canZoom = True
            else:
                self.canZoom = False
        else:
            self.canControlCam = False

        return Task.cont

    def __handleCameraIn(self):
        if self.cameraParent != None:

            if self.canZoom:
                if self.target.getY(self.cameraParent) > InteractiveCameraDriver.MIN_CAM_DISTANCE < InteractiveCameraDriver.MAX_CAM_DISTANCE:
                    self.cameraParent.setY(self.cameraParent.getY() + 1.0)

    def __handleCameraOut(self):
        if self.cameraParent != None:

            if self.canZoom:
                if self.target.getY(self.cameraParent) < InteractiveCameraDriver.MAX_CAM_DISTANCE > InteractiveCameraDriver.MIN_CAM_DISTANCE:
                    self.cameraParent.setY(self.cameraParent.getY() - 1.0)
        
    def stop(self):
        self.ignore('m')
        self.ignore('=' and '+')
        self.ignore('-')
        self.ignore('r')
        self.wantControl = False
        self.canControlCam = False
        self.canZoom = False
        taskMgr.remove('InteractiveCameraControlTask')
        taskMgr.remove('UpdateCan_InteractiveCameraControlTask')
        
    # todo: rotate avatar with camera change
    def __cameraControlTask(self, task):
        if self.canControlCam:
            if self.wantControl:
                mouseD = base.win.getPointer(0)
                x = mouseD.getX()
                y = mouseD.getY()
                
                heading = self.cameraParent.getH()
                pitch = self.cameraParent.getP()
                if base.win.movePointer(0, self.mouseCoords[0], self.mouseCoords[1]):
                    heading -= (x - self.mouseCoords[0]) * InteractiveCameraDriver.CameraFactor
                    pitch -= (y - self.mouseCoords[1]) * InteractiveCameraDriver.CameraFactor

                    if pitch > InteractiveCameraDriver.PITCH_LIMIT_BOT:
                        pitch = InteractiveCameraDriver.PITCH_LIMIT_BOT
                    elif pitch < InteractiveCameraDriver.PITCH_LIMIT_TOP:
                        pitch = InteractiveCameraDriver.PITCH_LIMIT_TOP
                        
                self.cameraParent.setHpr(heading, pitch, 0)
        
        return Task.cont