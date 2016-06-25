from direct.showbase.DirectObject import *

#todo: calculate available space on screen and make cells based on that.
LeftScreenCells = [
    (0,0,2.5),
    (0,0,4.3),
    (0,0,6.1)
]
RightScreenCells = LeftScreenCells
BottomScreenCells = [
    (-3.2,0,0),
    (0,0,0),
    (3.2,0,0)
]

class InteractiveObjectManager(DirectObject):
    def __init__(self):
        self.objectMap = []
        self.leftCellsMap = list(LeftScreenCells)
        self.leftCellsNode = base.a2dBottomLeft.attachNewNode("IOMLeftCells")
        self.leftCellsNode.setScale(0.2)
        self.leftCellsNode.setX(0.27)
        self.rightCellsMap = list(RightScreenCells)
        self.rightCellsNode = base.a2dBottomRight.attachNewNode("IOMRightCells")
        self.rightCellsNode.setScale(0.2)
        self.rightCellsNode.setX(-0.27)
        self.bottomCellsMap = list(BottomScreenCells)
        self.bottomCellsNode = base.a2dBottomCenter.attachNewNode("IOMBottomCells")
        self.bottomCellsNode.setScale(0.2)
        self.bottomCellsNode.setZ(0.27)
        self.cellParent2Map = {
            self.leftCellsNode: self.leftCellsMap,
            self.rightCellsNode: self.rightCellsMap,
            self.bottomCellsNode: self.bottomCellsMap
        }
        taskMgr.add(self.__updateObjectsTask, "update-int-objects-task")
        
    def add(self, obj):
        self.objectMap.append(obj)
        
    def __updateObjectsTask(self, task):
        for obj in self.objectMap:
            obj.update()
        return task.again
        
    def setAvailableCell(self, cellParent, cellPos):
        if not cellPos in self.cellParent2Map[cellParent]:
            self.cellParent2Map[cellParent].append(cellPos)
        
    def getAvailableCell(self):
        if len(self.leftCellsMap) > 0:
            return (self.leftCellsNode, self.leftCellsMap.pop())
        if len(self.rightCellsMap) > 0:
            return (self.rightCellsNode, self.rightCellsMap.pop())
        if len(self.bottomCellsMap) > 0:
            return (self.bottomCellsNode, self.bottomCellsMap.pop())