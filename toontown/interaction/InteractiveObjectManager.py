from direct.showbase.DirectObject import *

class InteractiveObjectManager(DirectObject):
    def __init__(self):
        self.objectMap = {}
        
    def add(self, obj):
        self.objectMap[obj.objType] = obj