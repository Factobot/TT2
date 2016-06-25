from toontown.interaction import Nametag, ChatBalloon

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
        self.nametag = Nametag.Nametag(self, self.nametagJoint)
        self.nametag.load()
        self.chat = ChatBalloon.ChatBalloon(self, self.nametag)
        self.chat.load()
        self.chat2d = ChatBalloon.ChatBalloon(self, self.nametag)
        self.chat2d.load(is2d=1)
        self.chatThought = ChatBalloon.ChatBalloon(self, self.nametag)
        self.chatThought.load(isThought=1)
        
    def setChat(self, chat, isThought = 0):
        if isThought:
            self.chatThought.setChat(chat)
        else:
            self.chat.setChat(chat)
        self.chat2d.setChat(chat)
        
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