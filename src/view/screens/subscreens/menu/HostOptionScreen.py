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
        
        self.overlaySize = pg.Vector2(380,450)
        self.inputOverlay = pg.surface.Surface(self.overlaySize,pg.SRCALPHA,32)        
        self.inputOverlay.fill(pg.Color(255,255,255,30))
        self.inputPos = pg.Vector2(self.screenSurf.get_size()[0]/2,self.screenSurf.get_size()[1]/2+30) - pg.Vector2(self.overlaySize.x/2,self.overlaySize.y/2)
        
        self.createBtn = UIButton.UIButton(buttonSurf,pg.Rect(self.inputPos + pg.Vector2(self.overlaySize.x/2,self.overlaySize.y/2+100),pg.Vector2(220,60)),"Create",25)
        self.uiGroup.add(self.createBtn)
        self.backBtn = UIButton.UIButton(buttonSurf,pg.Rect(pg.Vector2(self.screenSurf.get_width()*0.8,self.screenSurf.get_height()*0.8),pg.Vector2(220,60)),"Back",25)
        self.uiGroup.add(self.backBtn)
        
        
        self.portTextInputLabel = UIText.UIText(pg.font.Font("resources/ui/Font/kenvector_future.ttf",20),"Port",self.inputPos + pg.Vector2(10,10),True)
        self.uiGroup.add(self.portTextInputLabel)
        self.portInput = UITextInput.UITextInput(pg.rect.Rect(self.inputPos + pg.Vector2(10,55),(300,0)),"4484",self.portInputValidator,20,True)
        self.uiGroup.add(self.portInput)
        
        self.playerNameTextInputLabel = UIText.UIText(pg.font.Font("resources/ui/Font/kenvector_future.ttf",20),"Player name",pg.Vector2(self.inputPos + pg.Vector2(10,115)),True)
        self.uiGroup.add(self.playerNameTextInputLabel)
        self.playerNameInput = UITextInput.UITextInput(pg.rect.Rect(self.inputPos + pg.Vector2(10,160),(300,0)),"Player",lambda x:len(x)<=20,20,True)
        self.uiGroup.add(self.playerNameInput)
        
    def update(self) -> None:
        self.screenSurf.blit(self.inputOverlay,self.inputPos)
        super().update()
        
    def portInputValidator(self,input):
        if(len(input)>=1 and len(input)<=4):
            return input.isnumeric()
        elif(len(input)==0):
            return True
        else:
            return False