import __builtin__, os

from panda3d.core import loadPrcFile
loadPrcFile("config/dev.prc")

from toontown.toonbase.ToonBase import ToonBase
from toontown.toonbase.ToonSettings import ToonSettings
from direct.gui import DirectGuiGlobals

settings = ToonSettings()
settings.read()

__builtin__.settings = settings
__builtin__.base = ToonBase()
__builtin__.loader = base.loader

try:
    base.createToonBase()
except:
    raise #Exception('Could not init createToonBase!')

base.disableMouse()
    
DirectGuiGlobals.setDefaultRolloverSound(base.loadSfx('phase_3/audio/sfx/GUI_rollover.mp3'))
DirectGuiGlobals.setDefaultClickSound(base.loadSfx('stage_3/audio/sfx/GUI_click.ogg'))

from toontown.distributed.ToontownClientRepository import ToontownClientRepository
serverVersion = config.GetString('server-version')

if os.environ.has_key("GAMESERVER"):
    gameserver = os.environ['GAMESERVER']
else:
    gameserver = config.GetString('game-server', '127.0.0.1')
print gameserver
__builtin__.base.cr = ToontownClientRepository(
    dcFileNames=['config/toon.dc'], 
    serverVersion=serverVersion, 
    serverList=[gameserver, 7198], # Port stays default.
    accountDetails=[os.environ['ACCOUNT_PLAYTOKEN'], os.environ['ACCOUNT_PASSWORD']]
)

base.cr._connect()

try:
    base.run()
except:
    # Uh, this can't really ever happen...
    run()