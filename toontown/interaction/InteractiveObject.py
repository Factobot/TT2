from direct.showbase.DirectObject import *

INTERACTIVE_NAMETAG = 0

class InteractiveObject(DirectObject):
    def __init__(self, objType):
        self.objType = objType
        
    def enable(self):
        base.interactiveObjectMgr.add(self)
        
    def update(self):
        if self.objType == INTERACTIVE_NAMETAG:
            self.updateScreenNametag()
            
    def getScreenCell(self):
        return base.interactiveObjectMgr.getAvailableCell()
        
    def availableScreenCell(self, cellParent, cellPos):
        base.interactiveObjectMgr.setAvailableCell(cellParent, cellPos)