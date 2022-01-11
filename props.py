from direct.actor.Actor import Actor
from panda3d.core import CollisionSphere
from panda3d.core import NodePath
class propos:
    position = []
    model = None
    base = None
    collider = None
    def __init__(self, base, model, rad):
        self.base = base
        self.model = model
        self.collider = CollisionSphere(0,0,0, rad)
        self.model.addSolid(self.collider)
        