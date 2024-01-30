import src.controller.GameScreen as GameScreen
import src.model.GameObject.Textures as Textures

import pygame as pg


import src.view.UI.UIObject as UIObject
import src.view.UI.Components.UIButton as UIButton

class MenuScreen(GameScreen.GameScreen):
    
    
    def __init__(self,rectScreen:pg.Surface):
        self.rectScreen=rectScreen
        buttonSurf = next(item for item in Textures.loadedSurfaces if item["name"]=="blue_button00")["surface"]
        menuBtn = UIButton.UIButton(pg.Rect(rectScreen.get_rect().center[0],rectScreen.get_rect().center[1],300,100),buttonSurf,"Singleplayer")
        self.screenBtns.append({"name":"singleplayerBtn","button":menuBtn})
        
    def update(self):
        super().update()