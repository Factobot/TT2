from toontown.interaction import Nametag, ChatBalloon
from panda3d.core import *

TypeToDiff = {
    "ss": 0.3,
    "sl": 0.3,
    "ls": 0.1
}

class Avatar:
    
    def __init__(self):
        self.style = None
        self.avatarScale = 0
        self.height = 0
        self.name = ''
        
    def generateNametag(self):
        nametagJoint = self.find("**/head*")
        self.nametagJoint = self.attachNewNode("nametagJoint")
        self.nametagJoint.setZ(nametagJoint.getZ(self) + (nametagJoint.getSy(self) + (nametagJoint.getSy(self) * 0.6)))
        if TypeToDiff.has_key(self.style.head[1:]):
            self.nametagJoint.setZ(self.nametagJoint.getZ() - TypeToDiff[self.style.head[1:]])
        self.nametag = Nametag.Nametag(self, self.nametagJoint)
        self.nametag.load()
        #self.chat = ChatBalloon.ChatBalloon(self, self.nametag)
        #self.chat.load()
        
    def setChat(self, chat, isThought = 0):
        return
        if isThought:
            self.chat.setChat(chat, 1)
        else:
            self.chat.setChat(chat)
        self.chat.setChat(chat, 0, 1)
        
    def updateNametag(self):
        self.nametag.setName(self.name)
        
    def setName(self, name):
        self.name = name
        self.updateNametag()
        
    def setAvatarScale(self, scale):
        self.avatarScale = scale
        
    def setHeight(self, height):
        self.height = height
        
    def delete(self):
        self.nametag.unload()
        self.chat.unload()
        
    def setStyle(self, style):
        self.style = style
