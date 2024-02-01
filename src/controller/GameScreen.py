import pygame as pg
import src.view.UI.UIObject as UIObject

class GameScreen:
    screenSurf:pg.Surface
    
    screenBtns:[{"name":str,"button":UIObject.UIObject}]=[]
    
    def __init__(self,screenSurf:pg.Surface) -> None:
        self.screenSurf=screenSurf
        pass
    
    def update(self)->None:
        for item in self.screenBtns:
            button = item["button"]
            button.update(self.screenSurf)
            pass
            
        pass