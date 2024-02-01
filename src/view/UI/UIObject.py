import pygame as pg


class UIObject(pg.sprite.Sprite):
    surface: pg.Surface
    rect:pg.Rect
    def __init__(self,surface:pg.Surface,rect:pg.Rect) -> None:
        super().__init__()
        self.surface = pg.transform.scale(surface,rect.size)
        self.rect=pg.Rect((pg.Vector2(rect.topleft)-pg.Vector2(self.surface.get_size())/2),pg.Vector2(self.surface.get_size()))
        pass
    
    def update(self,drawSurface:pg.Surface)->None:
        drawSurface.blit(self.surface,self.rect)