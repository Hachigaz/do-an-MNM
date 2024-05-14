import pygame as pg

import components.game_components.Textures as Textures;
import components.UI.UIText as UIText
import components.UI.UIButton as UIButton

import components.UI.UITextInput as UITextInput

import view.screens.GameScreen as GameScreen



class HostOptionScreen(GameScreen.GameScreen):
    def __init__(self) -> None:
        super().__init__()
        
        buttonSurf = Textures.getLoadedSurfaces("blue_button00")
        
        screenCenterPos:pg.Vector2=  pg.Vector2(self.screenSurf.get_rect().center)
        
        title = UIText.UIText(pg.font.Font("resources/ui/Font/kenvector_future.ttf",40),"Host",pg.Vector2(screenCenterPos.x,150))
        self.uiGroup.add(title)
        
        menuBtnsOffsetY=200
        self.createBtn = UIButton.UIButton(buttonSurf,pg.Rect(pg.Vector2(pg.Vector2(screenCenterPos.x,menuBtnsOffsetY+200)),pg.Vector2(350,80)),"Create",25)
        self.uiGroup.add(self.createBtn)
        self.backBtn = UIButton.UIButton(buttonSurf,pg.Rect(pg.Vector2(pg.Vector2(screenCenterPos.x,menuBtnsOffsetY+300)),pg.Vector2(350,80)),"Back",25)
        self.uiGroup.add(self.backBtn)
        
        
        self.portTextInputLabel = UIText.UIText(pg.font.Font("resources/ui/Font/kenvector_future.ttf",20),"Port",pg.Vector2(100,100),True)
        self.uiGroup.add(self.portTextInputLabel)
        self.portInput = UITextInput.UITextInput(pg.rect.Rect(100,200,300,0),"22705",self.portInputValidator,20,True)
        self.uiGroup.add(self.portInput)
        
        self.playerNameTextInputLabel = UIText.UIText(pg.font.Font("resources/ui/Font/kenvector_future.ttf",20),"Player name",pg.Vector2(100,300),True)
        self.uiGroup.add(self.playerNameTextInputLabel)
        self.playerNameInput = UITextInput.UITextInput(pg.rect.Rect(100,400,300,0),"Player",None,20,True)
        self.uiGroup.add(self.playerNameInput)
        
    def update(self) -> None:
        super().update()
        
    def portInputValidator(self,input):
        if(len(input)>=1 and len(input)<=6):
            return input.isnumeric()
        elif(len(input)==0):
            return True
        else:
            return False