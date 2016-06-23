from direct.showbase.DirectObject import *

INTERACTIVE_NAMETAG = 0

class InteractiveObject(DirectObject):
    def __init__(self, objType):
        self.objType = objType
        
    def enable(self):
        pass#base.interactiveObjectMgr.add(self)