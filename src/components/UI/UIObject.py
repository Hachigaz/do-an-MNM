import pygame as pg

class uiSprite:
    def __init__(self,surface,rect) -> None:
        self.surface=surface
        self.rect=rect
    
    def draw(self, drawSurface:pg.Surface):
        drawSurface.blit(self.surface,self.rect)
        
class UIObject(pg.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.uiSurfaces=[]
        self.hoverEffects=[]
        self.disabledEffects=[]
        self.is_disabled = False
        self.draw_disabled = False
        pass
    
    def update(self,drawSurface:pg.Surface)->None:
        if(not self.draw_disabled):
            for surface in self.uiSurfaces:
                surface.draw(drawSurface)