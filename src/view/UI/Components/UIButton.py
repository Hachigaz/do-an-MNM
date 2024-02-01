import src.view.UI.UIObject as UIObject

import pygame as pg

class UIButton(UIObject.UIObject):
    text_font:pg.font.Font
    text_surface:pg.Surface
    text_rect:pg.Vector2
    
    hover_surface_effect:pg.Surface
    
    def __init__(self,surface:pg.Surface,rect:pg.Rect,text:str)->None:
        super().__init__(surface,rect)
        self.setFontSize(25)
        self.setText(text)
        
        self.hover_surface_effect=pg.Surface(self.surface.get_size(),pg.SRCALPHA).convert_alpha()
        self.hover_surface_effect.fill((255,255,255,100))
        pass
    

    def update(self,drawSurface:pg.Surface)->None:
        super().update(drawSurface)
        drawSurface.blit(self.text_surface,self.text_rect.topleft)
        if(self.rect.collidepoint(pg.Vector2(pg.mouse.get_pos()))):
            drawSurface.blit(self.hover_surface_effect,self.rect)
        
            
        pass
    
    def setFontSize(self,size:int):
        self.text_font = pg.font.Font("resources/ui/Font/kenvector_future_thin.ttf",size)
    
    def setText(self,text:str)->None:
        self.text_surface = self.text_font.render(text,True,pg.Color(255,255,255))
        self.text_rect=pg.Rect(pg.Vector2(self.surface.get_rect().center)-(pg.Vector2(self.text_surface.get_size())/2)+self.rect.topleft,pg.Vector2(self.text_surface.get_size()))