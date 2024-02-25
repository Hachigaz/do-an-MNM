import src.controller.GameScreen as GameScreen
import src.model.GameObject.Textures as Textures

import pygame as pg


import src.view.UI.UIObject as UIObject
import src.view.UI.Components.UIText as UIText
import src.view.UI.Components.UIButton as UIButton

import src.controller.screens.subscreens.menu.MultiplayerScreen as MultiplayerScreen

class MenuScreen(GameScreen.GameScreen):        
    def __init__(self,screenSurf:pg.Surface):
        super().__init__(screenSurf)
        
        
        #get loaded surfaces
        buttonSurf = Textures.getLoadedSurfaces("blue_button00")
        
        screenCenterPos:pg.Vector2=  pg.Vector2(self.screenSurf.get_rect().center)
        
        titleSurf =pg.font.Font("resources/ui/Font/kenvector_future.ttf",40).render("Bom man",True,pg.Color(255,255,255))
        gameTitle = UIText.UIText(titleSurf,pg.Rect(pg.Vector2(screenCenterPos.x,150),pg.Vector2(titleSurf.get_size())))
        self.uiGroup.add(gameTitle)
        
        menuBtnsOffsetY=200
        menuBtn = UIButton.UIButton(buttonSurf,pg.Rect(pg.Vector2(pg.Vector2(screenCenterPos.x,menuBtnsOffsetY+100)),pg.Vector2(350,80)),"Singleplayer",25)
        self.uiGroup.add(menuBtn)
        
        menuBtn = UIButton.UIButton(buttonSurf,pg.Rect(pg.Vector2(pg.Vector2(screenCenterPos.x,menuBtnsOffsetY+200)),pg.Vector2(350,80)),"Multiplayer",25)
        self.uiGroup.add(menuBtn)
        self.multiplayerScreen = MultiplayerScreen.MultiplayerScreen(self.screenSurf,self)
        menuBtn.setTriggerFunction(self.toMultiplayerScreen)
        
        menuBtn = UIButton.UIButton(buttonSurf,pg.Rect(pg.Vector2(pg.Vector2(screenCenterPos.x,menuBtnsOffsetY+300)),pg.Vector2(350,80)),"Options",25)
        menuBtn.is_disabled = True
        self.uiGroup.add(menuBtn)
        
        menuBtn = UIButton.UIButton(buttonSurf,pg.Rect(pg.Vector2(pg.Vector2(screenCenterPos.x,menuBtnsOffsetY+400)),pg.Vector2(350,80)),"Quit",25)
        self.uiGroup.add(menuBtn)
        menuBtn.setTriggerFunction(self.doQuit)
            
    def toMultiplayerScreen(self):
        #ko update screen này nữa mà update screen multiplayer
        self.currentScreen = self.multiplayerScreen
        
    def doQuit(self):
        pg.event.post(pg.event.Event(pg.QUIT))