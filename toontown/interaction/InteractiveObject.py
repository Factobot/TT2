from direct.showbase.DirectObject import *

INTERACTIVE_NAMETAG = 0

class InteractiveObject(DirectObject):
    def __init__(self, objType):
        self.objType = objType
        self.enabled = 0
        
    def enable(self):
        self.enabled = 1
        base.interactiveObjectMgr.add(self)
        
    def disable(self):
        self.enabled = 0
        base.interactiveObjectMgr.remove(self)
        
    def update(self):
        if self.objType == INTERACTIVE_NAMETAG:
            self.updateScreenNametag()
            
    def getScreenCell(self):
        return base.interactiveObjectMgr.getAvailableCell()
        
    def availableScreenCell(self, cellParent, cellPos):
        base.interactiveObjectMgr.setAvailableCell(cellParent, cellPos)