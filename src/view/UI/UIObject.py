import pygame as pg


class UIObject(pg.sprite.Sprite):
    surface: pg.Surface
    position:pg.Vector2
    def __init__(self,surface:pg.Surface,position:pg.Vector2) -> None:
        self.surface: pg.Vector2 = surface
        self.position=position-pg.Vector2(surface.get_size())/2

        pass
    
    def draw(self,drawSurface:pg.Surface)->None:
        drawSurface.blit(self.surface,self.position)