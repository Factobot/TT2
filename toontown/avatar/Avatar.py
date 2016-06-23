from toontown.interaction import Nametag

class Avatar:
    
    def __init__(self):
        self.style = None
        self.avatarScale = 0
        self.height = 0
        self.name = ''
        
    def generateNametag(self):
        nametagJoint = self.find("**/head*")
        self.nametagJoint = self.attachNewNode("nametagJoint")
        self.nametagJoint.setZ(nametagJoint.getZ(self) + 1.15)
        self.nametag = Nametag.Nametag(self.nametagJoint)
        self.nametag.load()
        
    def updateNametag(self):
        self.nametag.setName(self.name)
        
    def setName(self, name):
        self.name = name
        self.updateNametag()
        
    def setAvatarScale(self, scale):
        self.avatarScale = scale
        
    def setHeight(self, height):
        self.height = height
        
    def setStyle(self, style):
        self.style = style