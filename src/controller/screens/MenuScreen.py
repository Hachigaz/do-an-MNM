import src.controller.GameScreen as GameScreen
import src.model.GameObject.Textures as Textures

import pygame as pg


import src.view.UI.UIObject as UIObject
import src.view.UI.Components.UIButton as UIButton

class MenuScreen(GameScreen.GameScreen):
    def __init__(self,screenSurf:pg.Surface):
        super().__init__(screenSurf)
        buttonSurf = next(item for item in Textures.loadedSurfaces if item["name"]=="blue_button00")["surface"]
        
        menuBtnsOffsetY=200
        menuBtn = UIButton.UIButton(buttonSurf,pg.Rect(pg.Vector2(pg.Vector2(self.screenSurf.get_rect().center[0],menuBtnsOffsetY+100)),pg.Vector2(350,80)),"Singleplayer")
        self.screenBtns.append({"name":"singleplayerBtn","button":menuBtn})
        menuBtn = UIButton.UIButton(buttonSurf,pg.Rect(pg.Vector2(pg.Vector2(self.screenSurf.get_rect().center[0],menuBtnsOffsetY+200)),pg.Vector2(350,80)),"Multiplayer")
        self.screenBtns.append({"name":"multiplayerBtn","button":menuBtn})
        menuBtn = UIButton.UIButton(buttonSurf,pg.Rect(pg.Vector2(pg.Vector2(self.screenSurf.get_rect().center[0],menuBtnsOffsetY+300)),pg.Vector2(350,80)),"Options")
        self.screenBtns.append({"name":"multiplayerBtn","button":menuBtn})
        menuBtn = UIButton.UIButton(buttonSurf,pg.Rect(pg.Vector2(pg.Vector2(self.screenSurf.get_rect().center[0],menuBtnsOffsetY+400)),pg.Vector2(350,80)),"Quit")
        self.screenBtns.append({"name":"multiplayerBtn","button":menuBtn})
        
    def update(self):
        super().update()