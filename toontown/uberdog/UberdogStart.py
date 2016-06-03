from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
import __builtin__

loadPrcFileData('', 'window-type none')

__builtin__.base = ShowBase()

from toontown.uberdog.UberdogRepository import UberdogRepository
__builtin__.base.air = UberdogRepository(
    dcFileNames=['config/toon.dc'],
    baseChannel=100000000, 
    serverId=10000
)
base.air.notify.setInfo(True)

(host, port) = '127.0.0.1:7199'.split(':')
base.air.connect(host, port)

if base != None:
    base.run()
else:
    run()