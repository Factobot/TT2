from panda3d.core import *

# Zones
TOON_CONTINENT_ZONE = 10000 # That's just a base, only used for calcs
TOONTROPOLIS_ZONE = TOON_CONTINENT_ZONE + 100
ToontownZones = {
    TOONTROPOLIS_ZONE: [
        TOONTROPOLIS_ZONE + 1
    ]
}

zone2Details = {
    TOONTROPOLIS_ZONE: ['phase_4/models/neighborhoods/toontown_central', [0,0,0,0,0,0]]
}

# Toon control options
ToonSpeedFactor = 1.25
ToonForwardSpeed = 16.0 * ToonSpeedFactor
ToonJumpForce = 24.0
ToonReverseSpeed = 8.0 * ToonSpeedFactor
ToonRotateSpeed = 80.0 * ToonSpeedFactor
ToonForwardSlowSpeed = 6.0
ToonJumpSlowForce = 4.0
ToonReverseSlowSpeed = 2.5
ToonRotateSlowSpeed = 33.0

FloorOffset = 0.025
WallBitmask = BitMask32(1)
FloorBitmask = BitMask32(2)
CameraBitmask = BitMask32(4)
CameraTransparentBitmask = BitMask32(8)
SafetyNetBitmask = BitMask32(512)
SafetyGateBitmask = BitMask32(1024)
GhostBitmask = BitMask32(2048)
PathFindingBitmask = BitMask32.bit(29)
OriginalCameraFov = 52.0
DefaultCameraFov = 52.0
DefaultCameraFar = 400.0
DefaultCameraNear = 1.0

toonBodyScales = {'mouse': 0.6,
 'cat': 0.73,
 'duck': 0.66,
 'rabbit': 0.74,
 'horse': 0.85,
 'dog': 0.85,
 'monkey': 0.68,
 'bear': 0.85,
 'pig': 0.77}
toonHeadScales = {'mouse': Point3(1.1),
 'cat': Point3(1.2),
 'duck': Point3(1.2),
 'rabbit': Point3(1.2),
 'horse': Point3(1.2),
 'dog': Point3(1.2),
 'monkey': Point3(1.2),
 'bear': Point3(1.2),
 'pig': Point3(1.2)}
legHeightDict = {'s': 1.5,
 'm': 2.0,
 'l': 2.75}
torsoHeightDict = {'s': 1.5,
 'm': 1.75,
 'l': 2.25,
 'ss': 1.5,
 'ms': 1.75,
 'ls': 2.25,
 'sd': 1.5,
 'md': 1.75,
 'ld': 2.25}

headHeightDict = {'dls': 0.75,
 'dss': 0.5,
 'dsl': 0.5,
 'dll': 0.75,
 'cls': 0.75,
 'css': 0.5,
 'csl': 0.5,
 'cll': 0.75,
 'hls': 0.75,
 'hss': 0.5,
 'hsl': 0.5,
 'hll': 0.75,
 'mls': 0.75,
 'mss': 0.5,
 'rls': 0.75,
 'rss': 0.5,
 'rsl': 0.5,
 'rll': 0.75,
 'fls': 0.75,
 'fss': 0.5,
 'fsl': 0.5,
 'fll': 0.75,
 'pls': 0.75,
 'pss': 0.5,
 'psl': 0.5,
 'pll': 0.75,
 'bls': 0.75,
 'bss': 0.5,
 'bsl': 0.5,
 'bll': 0.75,
 'sls': 0.75,
 'sss': 0.5,
 'ssl': 0.5,
 'sll': 0.75}

ToonHidden = 0
ToonRender = 1
DefaultFilmSize = (1.0, 0.75)
TTOFilmSize = (1.0, 0.85)
FilmSize = TTOFilmSize # That size was defined by vote, so please don't change it.
ChatHotkey = "c"

def getMickeyFont():
    return loader.loadFont("phase_3/models/fonts/MickeyFont.bam")
    
def getToonFont():
    return loader.loadFont("phase_3/models/fonts/ImpressBT.ttf")
    