import pygame as pg
import components.UI.UIObject as UIObject

class UIText(UIObject.UIObject):
        def __init__(self,font:pg.font.Font,text:str,position:pg.Vector2,is_using_topleft = False) -> None:
                super().__init__()

                self.textColor = pg.Color(255,255,255,255)
                self.font:pg.font.Font = font      
                self.position = position
                self.is_using_topleft = is_using_topleft
                
                self.uiSurfaces.insert(0,None)
                self.updateText(text)
                
        def updateText(self,text:str):
                textSurf = self.font.render(text,True,self.textColor)
                if(not self.is_using_topleft):
                        rect=pg.Rect((self.position-pg.Vector2(textSurf.get_size())/2),pg.Vector2(textSurf.get_size()))
                else:
                        rect=pg.Rect(self.position,pg.Vector2(textSurf.get_size()))
                self.uiSurfaces[0]=UIObject.uiSpriteElement(textSurf,rect)