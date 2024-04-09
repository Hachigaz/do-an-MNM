import pygame as pg

import components.game_components.Textures as Textures;
import components.UI.UIText as UIText
import components.UI.UIButton as UIButton
import components.UI.ui_components.ChatBox as ChatBox

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
        self.refreshBtn = UIButton.UIButton(buttonSurf,pg.Rect(pg.Vector2(pg.Vector2(screenCenterPos.x,menuBtnsOffsetY+200)),pg.Vector2(350,80)),"Create",25)
        self.uiGroup.add(self.refreshBtn)
        self.backBtn = UIButton.UIButton(buttonSurf,pg.Rect(pg.Vector2(pg.Vector2(screenCenterPos.x,menuBtnsOffsetY+300)),pg.Vector2(350,80)),"Back",25)
        self.uiGroup.add(self.backBtn)
        
        self.portInput = UITextInput.UITextInput(pg.rect.Rect(100,100,0,0),"22705",self.portInputValidator,20)
        #self.uiGroup.add(self.portInput)
        
        self.messages = ChatBox.MessageList()
        self.chatBox = ChatBox.ChatBox(pg.rect.Rect(pg.Vector2(0,self.screenSurf.get_height()*0.7),pg.Vector2(0.4*self.screenSurf.get_width(),0.3*self.screenSurf.get_height())),self.messages)
        
    def update(self) -> None:
        super().update()
        self.chatBox.update(self.screenSurf)
        
    def portInputValidator(self,input):
        if(len(input)>=1 and len(input)<=6):
            return input.isnumeric()
        elif(len(input)==0):
            return True
        else:
            return False