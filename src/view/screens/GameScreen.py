import pygame as pg
import components.UI.UIObject as UIObject
 
class GameScreen:
    screenSurf:pg.Surface
    
    def __setup__(screenSurf:pg.Surface):
        GameScreen.screenSurf = screenSurf
        
    def __init__(self) -> None:
        self.uiGroup = pg.sprite.Group()
        pass
    
    def update(self) -> None:
        for sprite in self.uiGroup.sprites():
            sprite.update(self.screenSurf)
            pass
            
    def disableUI(self):
        for sprite in self.uiGroup.sprites():
            sprite.is_disabled = True
            
    def enableUI(self):
        for sprite in self.uiGroup.sprites():
            sprite.is_disabled = False