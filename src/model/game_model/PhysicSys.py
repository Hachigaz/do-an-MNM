from __future__ import annotations

import pygame as pg
import pymunk as pm
from pymunk.pygame_util import DrawOptions

class PhysicManager:
    physicManager:PhysicManager
    
    def __init__(self) -> None:
        space = pm.Space()
        space.gravity = 0,0
        
        self.projToWallImp:pm.CollisionHandler = space.add_collision_handler(4,1)
        self.projToRockImp:pm.CollisionHandler = space.add_collision_handler(4,2)
        self.projToPlayerImp:pm.CollisionHandler = space.add_collision_handler(4,3)
        self.projToProjImp:pm.CollisionHandler = space.add_collision_handler(4,4)
        
        self.space:pm.Space = space        
        pass
            
    def addObject(self,body:pm.Body,shape:pm.Shape):
        self.space.add(body,shape)
        pass

    def removeObject(self,body:pm.Body,shape:pm.Shape):
        self.space.remove(body,shape)
    
    def update(self):
        self.space.step(0.1)
        
    def debugUpdate(self,screenSurf:pg.surface.Surface):
        self.space.step(0.1)
        self.space.debug_draw(DrawOptions(screenSurf))