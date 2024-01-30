import pygame as pg


class UIObject(pg.sprite.Sprite):
    rect: pg.Rect
    surface: pg.Surface
    
    def __init__(self,rect:pg.Rect,surface:pg.Surface) -> None:
        self.rect: pg.Rect = rect
        self.surface: pg.Surface = surface
        pass
    
    def draw(self,screenSurface:pg.Surface)->None:
        screenSurface.blit(self.rect,self.surface)