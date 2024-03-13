import view.screens.GameScreen as GameScreen
import components.game_components.Textures as Textures

import pygame as pg


import components.UI.UIText as UIText
import components.UI.UIButton as UIButton

class MenuScreen(GameScreen.GameScreen):        
    def __init__(self):
        super().__init__()
        
        
        #get loaded surfaces
        buttonSurf = Textures.getLoadedSurfaces("blue_button00")
        
        screenCenterPos:pg.Vector2=  pg.Vector2(self.screenSurf.get_rect().center)
        
        titleSurf =pg.font.Font("resources/ui/Font/kenvector_future.ttf",40).render("Bom man",True,pg.Color(255,255,255))
        gameTitle = UIText.UIText(titleSurf,pg.Rect(pg.Vector2(screenCenterPos.x,150),pg.Vector2(titleSurf.get_size())))
        self.uiGroup.add(gameTitle)
        
        menuBtnsOffsetY=200
        self.singlePlayerBtn = UIButton.UIButton(buttonSurf,pg.Rect(pg.Vector2(pg.Vector2(screenCenterPos.x,menuBtnsOffsetY+100)),pg.Vector2(350,80)),"Singleplayer",25)
        self.uiGroup.add(self.singlePlayerBtn)
        
        
        self.multiplayerBtn = UIButton.UIButton(buttonSurf,pg.Rect(pg.Vector2(pg.Vector2(screenCenterPos.x,menuBtnsOffsetY+200)),pg.Vector2(350,80)),"Multiplayer",25)
        self.uiGroup.add(self.multiplayerBtn)
        
        self.optionBtn= UIButton.UIButton(buttonSurf,pg.Rect(pg.Vector2(pg.Vector2(screenCenterPos.x,menuBtnsOffsetY+300)),pg.Vector2(350,80)),"Options",25)
        self.optionBtn.is_disabled = True
        self.uiGroup.add(self.optionBtn)
        
        self.quitBtn = UIButton.UIButton(buttonSurf,pg.Rect(pg.Vector2(screenCenterPos.x,menuBtnsOffsetY+400),pg.Vector2(350,80)),"Quit",25)
        self.uiGroup.add(self.quitBtn)