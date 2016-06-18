from toontown.city.City import *

class TTPCity(City):
    def __init__(self, zoneId):
        City.__init__(self, zoneId)
        
    def load(self):
        # Here goes everything
        # For now a ttc landwalker.
        ground = loader.loadModel('phase_4/models/neighborhoods/toontown_central')
        ground.reparentTo(render)
        
        City.load(self)