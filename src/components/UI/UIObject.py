import pygame as pg

class uiSpriteElement:
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
                
class UISprite(UIObject):
    def __init__(self,surf:pg.surface.Surface, rect:pg.rect.Rect,is_using_topleft = False) -> None:
        super().__init__()
        surf = pg.transform.scale(surf,pg.Vector2(rect.width,rect.height))
        if(not is_using_topleft):
            surfaceRect=pg.Rect((pg.Vector2(rect.topleft)-pg.Vector2(surf.get_size())/2),pg.Vector2(surf.get_size()))
        else:
            surfaceRect = rect
        self.uiSurfaces.insert(0,uiSpriteElement(surface=surf,rect=surfaceRect))