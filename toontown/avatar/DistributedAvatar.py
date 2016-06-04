from direct.distributed.DistributedObject import DistributedObject

class DistributedAvatar(DistributedObject):

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)