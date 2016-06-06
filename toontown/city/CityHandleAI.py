from direct.directnotify.DirectNotifyGlobal import directNotify
from toontown.toonbase import ToontownGlobals
import ToontropolisCityAI

Zone2City = {
    ToontownGlobals.TOONTROPOLIS_ZONE: ToontropolisCityAI.ToontropolisCityAI
}

class CityHandleAI:
    notify = directNotify.newCategory('DistributedDistrict')
    
    def __init__(self, air, cityZone):
        self.air = air
        self.cityZone = cityZone
        self.city = None
        
    def processCity(self):
        if Zone2City.has_key(self.cityZone):
            self.city = Zone2City[self.cityZone](self.air, self.cityZone)
            self.city.start()
        else:
            self.notify.warning('Unmaped city zone: %s' %self.cityZone)
            