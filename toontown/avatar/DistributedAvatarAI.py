from direct.distributed.DistributedSmoothNodeAI import DistributedSmoothNodeAI

class DistributedAvatarAI(DistributedSmoothNodeAI):

    def __init__(self, air):
        DistributedSmoothNodeAI.__init__(self, air)