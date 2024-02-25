import pygame as pg
import src.view.UI.UIObject as UIObject

#game screen la screen chinh
#game screen chua cac thanh phan ui
class GameScreen:
    def __init__(self,screenSurf:pg.Surface) -> None:
        self.screenSurf=screenSurf
        self.uiGroup = pg.sprite.Group()
        self.currentScreen = self
        pass
    
    def update(self) -> None:
        if(self.currentScreen!=self):
            self.currentScreen.update()
        else:
            for sprite in self.uiGroup.sprites():
                sprite.update(self.screenSurf)
                pass
            
    def disableUI(self):
        for sprite in self.uiGroup.sprites():
            sprite.is_disabled = True
            
    def enableUI(self):
        for sprite in self.uiGroup.sprites():
            sprite.is_disabled = False
            
    

#subscreen la gamescreen con nam trong gamescreen
#subscreen co the quay ve gamescreen cha
class SubScreen(GameScreen):
    def __init__(self, screenSurf: pg.Surface,parentScreen:GameScreen) -> None:
        super().__init__(screenSurf)
        self.parentScreen = parentScreen
        
    def toParentScreen(self) -> None:
        self.parentScreen.currentScreen = self.parentScreen