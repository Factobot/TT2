from panda3d.core import *
from direct.showbase.DirectObject import *
from direct.task.Task import Task
from toontown.toonbase import ToontownGlobals

import math, random

class InteractiveCameraDriver(DirectObject):
    PITCH_LIMIT_TOP = -50
    PITCH_LIMIT_BOT = 10
    MAX_CAM_DISTANCE = 8.5
    MIN_CAM_DISTANCE = 0
    CameraFactor = 0.3
    CameraBitmask = BitMask32(4)

    def __init__(self, camera, cameraColl = True):
        self.camera = camera
        self.cameraCollisions = cameraColl
        self.safePointerData = (0, 0, 250)
        self.mouseCoords = [0,0]
        self.target = None
        self.wantControl = False
        self.canControlCam = False
        self.canZoom = False
        self._smartCamEnabled = 0
        self.cTrav = base.cTrav
        self.uniqueICId = random.random()
        
    def __setupSmartCamera(self):
        self.__idealCameraObstructed = 0
        self.closestObstructionDistance = 0.0
        self.cameraZOffset = 0.0
        self.__onLevelGround = 0
        self.__camCollCanMove = 0
        self.__geom = render
        self.__disableSmartCam = 0
        self.ccTrav = CollisionTraverser('LocalAvatar.ccTrav')
        self.ccLine = CollisionSegment(0.0, 0.0, 0.0, 1.0, 0.0, 0.0)
        self.ccLineNode = CollisionNode('ccLineNode')
        self.ccLineNode.addSolid(self.ccLine)
        self.ccLineNodePath = self.target.attachNewNode(self.ccLineNode)
        self.ccLineBitMask = self.CameraBitmask
        self.ccLineNode.setFromCollideMask(self.ccLineBitMask)
        self.ccLineNode.setIntoCollideMask(BitMask32.allOff())
        self.camCollisionQueue = CollisionHandlerQueue()
        self.ccTrav.addCollider(self.ccLineNodePath, self.camCollisionQueue)
        self.ccSphere = CollisionSphere(0, 0, 0, 1)
        self.ccSphereNode = CollisionNode('ccSphereNode')
        self.ccSphereNode.addSolid(self.ccSphere)
        self.ccSphereNodePath = base.camera.attachNewNode(self.ccSphereNode)
        self.ccSphereNode.setFromCollideMask(self.CameraBitmask)
        self.ccSphereNode.setIntoCollideMask(BitMask32.allOff())
        self.camPusher = CollisionHandlerPusher()
        self.camPusher.addCollider(self.ccSphereNodePath, base.camera)
        self.camPusher.setCenter(self.target)
        self.ccPusherTrav = CollisionTraverser('LocalAvatar.ccPusherTrav')
        self.ccSphere2 = self.ccSphere
        self.ccSphereNode2 = CollisionNode('ccSphereNode2')
        self.ccSphereNode2.addSolid(self.ccSphere2)
        self.ccSphereNodePath2 = base.camera.attachNewNode(self.ccSphereNode2)
        self.ccSphereNode2.setFromCollideMask(self.CameraBitmask)
        self.ccSphereNode2.setIntoCollideMask(BitMask32.allOff())
        self.camPusher2 = CollisionHandlerPusher()
        self.ccPusherTrav.addCollider(self.ccSphereNodePath2, self.camPusher2)
        self.camPusher2.addCollider(self.ccSphereNodePath2, base.camera)
        self.camPusher2.setCenter(self.target)
        self.camFloorRayNode = self.target.attachNewNode('camFloorRayNode')
        self.ccRay = CollisionRay(0.0, 0.0, 0.0, 0.0, 0.0, -1.0)
        self.ccRayNode = CollisionNode('ccRayNode')
        self.ccRayNode.addSolid(self.ccRay)
        self.ccRayNodePath = self.camFloorRayNode.attachNewNode(self.ccRayNode)
        self.ccRayBitMask = ToontownGlobals.FloorBitmask
        self.ccRayNode.setFromCollideMask(self.ccRayBitMask)
        self.ccRayNode.setIntoCollideMask(BitMask32.allOff())
        self.ccTravFloor = CollisionTraverser('LocalAvatar.ccTravFloor')
        self.camFloorCollisionQueue = CollisionHandlerQueue()
        self.ccTravFloor.addCollider(self.ccRayNodePath, self.camFloorCollisionQueue)
        self.ccTravOnFloor = CollisionTraverser('LocalAvatar.ccTravOnFloor')
        self.ccRay2 = CollisionRay(0.0, 0.0, 0.0, 0.0, 0.0, -1.0)
        self.ccRay2Node = CollisionNode('ccRay2Node')
        self.ccRay2Node.addSolid(self.ccRay2)
        self.ccRay2NodePath = self.camFloorRayNode.attachNewNode(self.ccRay2Node)
        self.ccRay2BitMask = ToontownGlobals.FloorBitmask
        self.ccRay2Node.setFromCollideMask(self.ccRay2BitMask)
        self.ccRay2Node.setIntoCollideMask(BitMask32.allOff())
        self.ccRay2MoveNodePath = hidden.attachNewNode('ccRay2MoveNode')
        self.camFloorCollisionBroadcaster = CollisionHandlerFloor()
        self.camFloorCollisionBroadcaster.setInPattern('on-floor')
        self.camFloorCollisionBroadcaster.setOutPattern('off-floor')
        self.camFloorCollisionBroadcaster.addCollider(self.ccRay2NodePath, self.ccRay2MoveNodePath)
        
    def recalcCameraSphere(self):
        nearPlaneDist = base.camLens.getNear()
        hFov = base.camLens.getHfov()
        vFov = base.camLens.getVfov()
        hOff = nearPlaneDist * math.tan(deg2Rad(hFov / 2.0))
        vOff = nearPlaneDist * math.tan(deg2Rad(vFov / 2.0))
        camPnts = [Point3(hOff, nearPlaneDist, vOff),
         Point3(-hOff, nearPlaneDist, vOff),
         Point3(hOff, nearPlaneDist, -vOff),
         Point3(-hOff, nearPlaneDist, -vOff),
         Point3(0.0, 0.0, 0.0)]
        avgPnt = Point3(0.0, 0.0, 0.0)
        for camPnt in camPnts:
            avgPnt = avgPnt + camPnt

        avgPnt = avgPnt / len(camPnts)
        sphereRadius = 0.0
        for camPnt in camPnts:
            dist = Vec3(camPnt - avgPnt).length()
            if dist > sphereRadius:
                sphereRadius = dist

        avgPnt = Point3(avgPnt)
        self.ccSphereNodePath.setPos(avgPnt)
        self.ccSphereNodePath2.setPos(avgPnt)
        self.ccSphere.setRadius(sphereRadius)
        
    def startUpdateSmartCamera(self, push = 1):
        if self._smartCamEnabled:
            return
        self._smartCamEnabled = True
        self.__floorDetected = 0
        self.__cameraHasBeenMoved = 0
        self.recalcCameraSphere()
        self.__instantaneousCamPos = camera.getPos()
        if push:
            self.cTrav.addCollider(self.ccSphereNodePath, self.camPusher)
            self.ccTravOnFloor.addCollider(self.ccRay2NodePath, self.camFloorCollisionBroadcaster)
            self.__disableSmartCam = 0
        else:
            self.__disableSmartCam = 1
        self.__lastPosWrtRender = camera.getPos(render)
        self.__lastHprWrtRender = camera.getHpr(render)
        taskName = 'updateSmartCamera' + str(self.uniqueICId)
        taskMgr.remove(taskName)
        taskMgr.add(self.updateSmartCamera, taskName, priority=47)
        
    def updateSmartCamera(self, task):
        if not self.__camCollCanMove and not self.__cameraHasBeenMoved:
            if self.__lastPosWrtRender == camera.getPos(render):
                if self.__lastHprWrtRender == camera.getHpr(render):
                    return task.cont
        self.__cameraHasBeenMoved = 0
        self.__lastPosWrtRender = camera.getPos(render)
        self.__lastHprWrtRender = camera.getHpr(render)
        self.__idealCameraObstructed = 0
        if not self.__disableSmartCam:
            self.ccTrav.traverse(self.__geom)
            if self.camCollisionQueue.getNumEntries() > 0:
                self.camCollisionQueue.sortEntries()
                self.handleCameraObstruction(self.camCollisionQueue.getEntry(0))
            if not self.__onLevelGround:
                self.handleCameraFloorInteraction()
        if not self.__idealCameraObstructed:
            self.nudgeCamera()
        if not self.__disableSmartCam:
            self.ccPusherTrav.traverse(self.__geom)
            self.putCameraFloorRayOnCamera()
        self.ccTravOnFloor.traverse(self.__geom)
        return task.cont
        
    def nudgeCamera(self):
        CLOSE_ENOUGH = 0.1
        curCamPos = self.__instantaneousCamPos
        curCamHpr = camera.getHpr()
        targetCamPos = self.getCompromiseCameraPos()
        targetCamLookAt = self.getLookAtPoint()
        posDone = 0
        if Vec3(curCamPos - targetCamPos).length() <= CLOSE_ENOUGH:
            camera.setPos(targetCamPos)
            posDone = 1
        camera.setPos(targetCamPos)
        camera.lookAt(targetCamLookAt)
        targetCamHpr = camera.getHpr()
        hprDone = 0
        if Vec3(curCamHpr - targetCamHpr).length() <= CLOSE_ENOUGH:
            hprDone = 1
        if posDone and hprDone:
            return
        lerpRatio = 0.15
        lerpRatio = 1 - pow(1 - lerpRatio, globalClock.getDt() * 30.0)
        self.__instantaneousCamPos = targetCamPos * lerpRatio + curCamPos * (1 - lerpRatio)
        if self.__disableSmartCam or not self.__idealCameraObstructed:
            newHpr = targetCamHpr * lerpRatio + curCamHpr * (1 - lerpRatio)
        else:
            newHpr = targetCamHpr
        print 1
        camera.setPos(self.__instantaneousCamPos)
        camera.setHpr(newHpr)
        
    def handleCameraFloorInteraction(self):
        self.putCameraFloorRayOnCamera()
        self.ccTravFloor.traverse(self.__geom)
        if self.__onLevelGround:
            return
        if self.camFloorCollisionQueue.getNumEntries() == 0:
            return
        self.camFloorCollisionQueue.sortEntries()
        camObstrCollisionEntry = self.camFloorCollisionQueue.getEntry(0)
        camHeightFromFloor = camObstrCollisionEntry.getSurfacePoint(self.ccRayNodePath)[2]
        self.cameraZOffset = camera.getPos()[2] + camHeightFromFloor
        if self.cameraZOffset < 0:
            self.cameraZOffset = 0
        if self.__floorDetected == 0:
            self.__floorDetected = 1
            self.popCameraToDest()
            
    def putCameraFloorRayOnCamera(self):
        self.camFloorRayNode.setPos(self.ccSphereNodePath, 0, 0, 0)
        
    def handleCameraObstruction(self, camObstrCollisionEntry):
        collisionPoint = camObstrCollisionEntry.getSurfacePoint(self.ccLineNodePath)
        collisionVec = Vec3(collisionPoint - self.ccLine.getPointA())
        distance = collisionVec.length()
        self.__idealCameraObstructed = 1
        self.closestObstructionDistance = distance
        self.popCameraToDest()
        
    def popCameraToDest(self):
        newCamPos = self.getCompromiseCameraPos()
        newCamLookAt = self.getLookAtPoint()
        self.positionCameraWithPusher(newCamPos, newCamLookAt)
        self.__instantaneousCamPos = camera.getPos()
        
    def getLookAtPoint(self):
        return self.__idealCameraPos
        
    def positionCameraWithPusher(self, pos, lookAt):
        camera.setPos(pos)
        self.ccPusherTrav.traverse(self.__geom)
        camera.lookAt(lookAt)
        
    def getCompromiseCameraPos(self):
        if self.__idealCameraObstructed == 0:
            compromisePos = self.getIdealCameraPos()
        else:
            visPnt = self.getVisibilityPoint()
            idealPos = self.getIdealCameraPos()
            distance = Vec3(idealPos - visPnt).length()
            ratio = self.closestObstructionDistance / distance
            compromisePos = idealPos * ratio + visPnt * (1 - ratio)
            liftMult = 1.0 - ratio * ratio
            compromisePos = Point3(compromisePos[0], compromisePos[1], compromisePos[2] + self.getHeight() * 0.4 * liftMult)
        compromisePos.setZ(compromisePos[2] + self.cameraZOffset)
        return compromisePos
        
    def getVisibilityPoint(self):
        return Vec3(0,0,self.getHeight())
        
    def getHeight(self):
        return base.playAssistant.getAvatarHeight()
        
    def getIdealCameraPos(self):
        return self.__idealCameraPos
        
    def setTarget(self, target):
        if target and not self.target:
            self.target = target
            self.__idealCameraPos = base.playAssistant.cameraDefaultPos
            self.cameraParent = self.target.attachNewNode('cameraParent')
            self.camera.reparentTo(self.cameraParent)
            self.camera.lookAt(self.cameraParent)
            self.__setupSmartCamera()
        
    def start(self):
        self.accept('m', self.__handlePressMouse)
        self.accept('=' or '+', self.__handleCameraIn)
        self.accept('-', self.__handleCameraOut)
        self.accept('r', self.__resetCameraPos)
        taskMgr.add(self.__cameraControlTask, 'InteractiveCameraControlTask')
        #taskMgr.add(self.__updateCanControl, 'UpdateCan_InteractiveCameraControlTask')
        self.canControlCam = 1
        #self.startUpdateSmartCamera()
        
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
        if self.wantControl:
            self.__handlePressMouse()
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
                if base.win.movePointer(0, int(self.mouseCoords[0]), int(self.mouseCoords[1])):
                    heading -= (x - self.mouseCoords[0]) * InteractiveCameraDriver.CameraFactor
                    pitch -= (y - self.mouseCoords[1]) * InteractiveCameraDriver.CameraFactor

                    if pitch > InteractiveCameraDriver.PITCH_LIMIT_BOT:
                        pitch = InteractiveCameraDriver.PITCH_LIMIT_BOT
                    elif pitch < InteractiveCameraDriver.PITCH_LIMIT_TOP:
                        pitch = InteractiveCameraDriver.PITCH_LIMIT_TOP
                        
                self.cameraParent.setHpr(heading, pitch, 0)
        
        return Task.cont