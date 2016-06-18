
class City:
    def __init__(self, zoneId):
        self.zoneId = zoneId
        
    def load(self):
        base.localAvatar.playAssistant.request("Play")
        base.transitions.fadeOut(1)