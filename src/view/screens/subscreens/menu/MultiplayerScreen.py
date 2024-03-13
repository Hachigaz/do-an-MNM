import pygame as pg

import components.game_components.Textures as Textures;
import components.UI.UIObject as UIObject
import components.UI.UIText as UIText
import components.UI.UIButton as UIButton

import view.screens.GameScreen as GameScreen



class MultiplayerScreen(GameScreen.GameScreen):
    def __init__(self) -> None:
        super().__init__()
        
        buttonSurf = next(item for item in Textures.loadedSurfaces if item["name"]=="blue_button00")["surface"]
        
        screenCenterPos:pg.Vector2=  pg.Vector2(self.screenSurf.get_rect().center)
        
        titleSurf =pg.font.Font("resources/ui/Font/kenvector_future.ttf",40).render("Multiplayer",True,pg.Color(255,255,255))
        title = UIText.UIText(titleSurf,pg.Rect(pg.Vector2(screenCenterPos.x,150),pg.Vector2(titleSurf.get_size())))
        self.uiGroup.add(title)
        
        menuBtnsOffsetY=200
        self.hostBtn = UIButton.UIButton(buttonSurf,pg.Rect(pg.Vector2(pg.Vector2(screenCenterPos.x,menuBtnsOffsetY+100)),pg.Vector2(350,80)),"Host",25)
        self.uiGroup.add(self.hostBtn)
        self.browseBtn = UIButton.UIButton(buttonSurf,pg.Rect(pg.Vector2(pg.Vector2(screenCenterPos.x,menuBtnsOffsetY+200)),pg.Vector2(350,80)),"Browse Server",25)
        self.uiGroup.add(self.browseBtn)
        self.joinByIPBtn = UIButton.UIButton(buttonSurf,pg.Rect(pg.Vector2(pg.Vector2(screenCenterPos.x,menuBtnsOffsetY+300)),pg.Vector2(350,80)),"Join By IP",25)
        self.uiGroup.add(self.joinByIPBtn)
        self.backToMenuBtn = UIButton.UIButton(buttonSurf,pg.Rect(pg.Vector2(pg.Vector2(screenCenterPos.x,menuBtnsOffsetY+400)),pg.Vector2(350,80)),"Back To Menu",25)
        self.uiGroup.add(self.backToMenuBtn)