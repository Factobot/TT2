from panda3d.core import *
import os

language = config.GetString('game-language', "english")
path = "toontown.toonbase.TTLocalizer_%s" %language
m = __import__(path, {}, {}, ['toontown.toonbase'])
globals().update(m.__dict__)