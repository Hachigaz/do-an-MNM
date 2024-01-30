import pygame as pg
import src.view.UI.UIObject as UIObject

class GameScreen:
    rectScreen:pg.Surface
    
    screenBtns:[{"name":str,"button":UIObject.UIObject}]=[]
    
    def __init__(self) -> None:
        pass
    
    def update(self)->None:
        for item in self.screenBtns:
            button = item["button"]
            self.rectScreen.blit(button.surface,button.rect)
            pass
            
        pass