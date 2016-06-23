
class City:
    def __init__(self, zoneId):
        self.zoneId = zoneId
        
    def load(self):
        base.localAvatar.playAssistant.request("Play")
        base.transitions.fadeIn(1)
        base.localAvatar.setPosHprScale(0,0,0,0,0,0,1,1,1)
        base.localAvatar.reparentTo(render)
        base.localAvatar.playAssistant.controlManager.get("walk").placeOnFloor()