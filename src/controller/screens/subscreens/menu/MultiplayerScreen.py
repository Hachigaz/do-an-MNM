import src.controller.GameScreen as GameScreen
import pygame as pg
import src.model.GameObject.Textures as Textures;

import src.view.UI.UIObject as UIObject
import src.view.UI.Components.UIText as UIText
import src.view.UI.Components.UIButton as UIButton


class MultiplayerScreen(GameScreen.SubScreen):
    def __init__(self, screenSurf: pg.Surface, parentScreen: GameScreen) -> None:
        super().__init__(screenSurf, parentScreen)
        
        buttonSurf = next(item for item in Textures.loadedSurfaces if item["name"]=="blue_button00")["surface"]
        
        screenCenterPos:pg.Vector2=  pg.Vector2(self.screenSurf.get_rect().center)
        
        titleSurf =pg.font.Font("resources/ui/Font/kenvector_future.ttf",40).render("Multiplayer",True,pg.Color(255,255,255))
        title = UIText.UIText(titleSurf,pg.Rect(pg.Vector2(screenCenterPos.x,150),pg.Vector2(titleSurf.get_size())))
        self.uiGroup.add(title)
        
        menuBtnsOffsetY=200
        menuBtn = UIButton.UIButton(buttonSurf,pg.Rect(pg.Vector2(pg.Vector2(screenCenterPos.x,menuBtnsOffsetY+100)),pg.Vector2(350,80)),"Host",25)
        self.uiGroup.add(menuBtn)
        menuBtn = UIButton.UIButton(buttonSurf,pg.Rect(pg.Vector2(pg.Vector2(screenCenterPos.x,menuBtnsOffsetY+200)),pg.Vector2(350,80)),"Browse Server",25)
        self.uiGroup.add(menuBtn)
        menuBtn = UIButton.UIButton(buttonSurf,pg.Rect(pg.Vector2(pg.Vector2(screenCenterPos.x,menuBtnsOffsetY+300)),pg.Vector2(350,80)),"Join By IP",25)
        self.uiGroup.add(menuBtn)
        menuBtn = UIButton.UIButton(buttonSurf,pg.Rect(pg.Vector2(pg.Vector2(screenCenterPos.x,menuBtnsOffsetY+400)),pg.Vector2(350,80)),"Back To Menu",25)
        self.uiGroup.add(menuBtn)
        menuBtn.setTriggerFunction(self.toParentScreen)