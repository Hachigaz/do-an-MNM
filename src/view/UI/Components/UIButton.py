import src.view.UI.UIObject as UIObject

import pygame as pg

class UIButton(UIObject.UIObject):
    text_font:pg.font.Font
    text_surface:pg.Surface
    text_rect:pg.Rect
    def __init__(self,rect:pg.Rect,surface:pg.Surface,text:str)->None:
        super().__init__(rect,surface)
        self.setFontSize(20)
        self.setText(text)
        pass

    def draw(self)->None:
        super().draw()
        self.surface.blit(self.text.surface,self.text.rect)
        pass
    
    def setFontSize(self,size:int):
        self.text_font = pg.font.Font("resources/ui/Font/kenvector_future_thin.ttf",size)
    
    def setText(self,text:str)->None:
        self.text_surface = self.text_font.render(text,True,pg.Color(255,255,255))
        self.text_rect = pg.Rect(self.surface.get_rect().center[0],self.surface.get_rect().center[1],self.text_surface.get_rect().width,self.text_surface.get_rect().height)
        