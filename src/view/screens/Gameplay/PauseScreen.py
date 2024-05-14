import pygame as pg

import view.screens.GameScreen as GameScreen

import components.game_components.Textures as Textures
import components.UI.UIText as UIText
import components.UI.UIButton as UIButton


class PauseScreen(GameScreen.GameScreen):
    def __init__(self) -> None:
        super().__init__()
        
        buttonSurf = Textures.getLoadedSurfaces("blue_button00")
        
        screenCenterPos:pg.Vector2=  pg.Vector2(self.screenSurf.get_rect().center)
        
        title = UIText.UIText(pg.font.Font("resources/ui/Font/kenvector_future.ttf",40),"Bom man",pg.Vector2(screenCenterPos.x,150))
        self.uiGroup.add(title)
        
        menuBtnsOffsetY=200
        
        self.resumeBtn = UIButton.UIButton(buttonSurf,pg.Rect(pg.Vector2(pg.Vector2(screenCenterPos.x,menuBtnsOffsetY+100)),pg.Vector2(350,80)),"Resume",25)
        self.uiGroup.add(self.resumeBtn)
        
        self.quitBtn = UIButton.UIButton(buttonSurf,pg.Rect(pg.Vector2(screenCenterPos.x,menuBtnsOffsetY+200),pg.Vector2(350,80)),"Quit",25)
        self.uiGroup.add(self.quitBtn)
        
    pass