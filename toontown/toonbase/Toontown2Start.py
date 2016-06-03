import __builtin__

from panda3d.core import loadPrcFile
loadPrcFile("config/dev.prc")

from toontown.toonbase.ToonBase import ToonBase
from toontown.toonbase.ToonSettings import ToonSettings

settings = ToonSettings()
settings.read()

__builtin__.settings = settings
__builtin__.base = ToonBase()
__builtin__.loader = base.loader

try:
    base.createToonBase()
except:
    raise Exception('Could not init createToonBase!')

from toontown.distributed.ToontownClientRepository import ToontownClientRepository
serverVersion = config.GetString('server-version')

__builtin__.base.cr = ToontownClientRepository(
    dcFileNames=['config/toon.dc'], 
    serverVersion=serverVersion, 
    serverList=[config.GetString('game-server', '127.0.0.1'), 7198], # Port stays default.
    playToken=config.GetString('play-token')
)

base.cr._connect()

try:
    base.run()
except:
    # Uh, this can't really ever happen...
    run()