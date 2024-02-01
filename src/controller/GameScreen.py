import pygame as pg
import src.view.UI.UIObject as UIObject

class GameScreen:
    screenSurf:pg.Surface
    
    uiGroup:pg.sprite.Group=pg.sprite.Group()
    
    def __init__(self,screenSurf:pg.Surface) -> None:
        self.screenSurf=screenSurf
        pass
    
    def update(self)->None:
        for sprite in self.uiGroup.sprites():
            sprite.update(self.screenSurf)
            pass
            
        pass