import src.view.UI.UIObject as UIObject

import pygame as pg

class UIButton(UIObject.UIObject):
    text_font:pg.font.Font
    text_surface:pg.Surface
    text_pos:pg.Vector2
    def __init__(self,surface:pg.Surface,position:pg.Vector2,text:str)->None:
        super().__init__(surface,position)
        self.setFontSize(20)
        self.setText(text)
        pass
    

    def draw(self,drawSurface:pg.Surface)->None:
        self.surface.blit(self.text_surface,self.text_pos)
        super().draw(drawSurface)
        pass
    
    def setFontSize(self,size:int):
        self.text_font = pg.font.Font("resources/ui/Font/kenvector_future_thin.ttf",size)
    
    def setText(self,text:str)->None:
        self.text_surface = self.text_font.render(text,True,pg.Color(255,255,255))
        self.text_pos=pg.Vector2(self.surface.get_rect().center)-(pg.Vector2(self.text_surface.get_size())/2)
        