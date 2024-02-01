import src.controller.GameScreen as GameScreen
import src.model.GameObject.Textures as Textures

import pygame as pg


import src.view.UI.UIObject as UIObject
import src.view.UI.Components.UIButton as UIButton

class MenuScreen(GameScreen.GameScreen):
    def __init__(self,screenSurf:pg.Surface):
        super().__init__(screenSurf)
        buttonSurf = next(item for item in Textures.loadedSurfaces if item["name"]=="blue_button00")["surface"]
        
        screenCenterPos:pg.Vector2=  pg.Vector2(self.screenSurf.get_rect().center)
        
        titleSurf =pg.font.Font("resources/ui/Font/kenvector_future.ttf",40).render("Bom man",True,pg.Color(255,255,255))
        gameTitle = UIObject.UIObject(titleSurf,pg.Rect(pg.Vector2(screenCenterPos.x,150),pg.Vector2(titleSurf.get_size())))
        self.uiGroup.add(gameTitle)
        
        menuBtnsOffsetY=200
        menuBtn = UIButton.UIButton(buttonSurf,pg.Rect(pg.Vector2(pg.Vector2(screenCenterPos.x,menuBtnsOffsetY+100)),pg.Vector2(350,80)),"Singleplayer",25)
        self.uiGroup.add(menuBtn)
        menuBtn = UIButton.UIButton(buttonSurf,pg.Rect(pg.Vector2(pg.Vector2(screenCenterPos.x,menuBtnsOffsetY+200)),pg.Vector2(350,80)),"Multiplayer",25)
        self.uiGroup.add(menuBtn)
        menuBtn = UIButton.UIButton(buttonSurf,pg.Rect(pg.Vector2(pg.Vector2(screenCenterPos.x,menuBtnsOffsetY+300)),pg.Vector2(350,80)),"Options",25)
        self.uiGroup.add(menuBtn)
        menuBtn = UIButton.UIButton(buttonSurf,pg.Rect(pg.Vector2(pg.Vector2(screenCenterPos.x,menuBtnsOffsetY+400)),pg.Vector2(350,80)),"Quit",25)
        self.uiGroup.add(menuBtn)
        
    def update(self):
        super().update()