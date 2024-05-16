import pygame as pg

import components.game_components.Textures as Textures;
import components.UI.UIText as UIText
import components.UI.UIButton as UIButton
import components.UI.UITextInput as UITextInput

import view.screens.GameScreen as GameScreen



class JoinByIPScreen(GameScreen.GameScreen):
    def __init__(self) -> None:
        super().__init__()
        
        buttonSurf = Textures.getLoadedSurfaces("blue_button00")
        
        title = UIText.UIText(pg.font.Font("resources/ui/Font/kenvector_future.ttf",40),"Join by IP",pg.Vector2(self.screenSurf.get_width()/2,150))
        self.uiGroup.add(title)
                
        self.overlaySize = pg.Vector2(380,450)
        self.inputOverlay = pg.surface.Surface(self.overlaySize,pg.SRCALPHA,32)        
        self.inputOverlay.fill(pg.Color(255,255,255,30))
        self.inputPos = pg.Vector2(self.screenSurf.get_size()[0]/2,self.screenSurf.get_size()[1]/2+30) - pg.Vector2(self.overlaySize.x/2,self.overlaySize.y/2)
        
        self.IPInputLabel = UIText.UIText(pg.font.Font("resources/ui/Font/kenvector_future.ttf",20),"IP",self.inputPos + pg.Vector2(10,10),True)
        self.uiGroup.add(self.IPInputLabel)
        self.IPInput = UITextInput.UITextInput(pg.rect.Rect(self.inputPos + pg.Vector2(10,55),(300,0)),"192.168.1.18",None,20,True)
        self.uiGroup.add(self.IPInput)
        
        self.portTextInputLabel = UIText.UIText(pg.font.Font("resources/ui/Font/kenvector_future.ttf",20),"Port",self.inputPos + pg.Vector2(10,115),True)
        self.uiGroup.add(self.portTextInputLabel)
        self.portInput = UITextInput.UITextInput(pg.rect.Rect(self.inputPos + pg.Vector2(10,160),(300,0)),"4484",self.portInputValidator,20,True)
        self.uiGroup.add(self.portInput)
        
        self.PlayerNameInputLabel = UIText.UIText(pg.font.Font("resources/ui/Font/kenvector_future.ttf",20),"Player name",self.inputPos + pg.Vector2(10,220),True)
        self.uiGroup.add(self.PlayerNameInputLabel)
        self.PlayerNameInput = UITextInput.UITextInput(pg.rect.Rect(self.inputPos + pg.Vector2(10,265),(300,0)),"Player",lambda x:len(x)<=20,20,True)
        self.uiGroup.add(self.PlayerNameInput)
        
        self.connectBtn = UIButton.UIButton(buttonSurf,pg.Rect(pg.Vector2(self.inputPos + pg.Vector2(self.overlaySize.x/2-125,330)),pg.Vector2(250,60)),"Connect",25,True)
        self.uiGroup.add(self.connectBtn)
        
        self.backBtn = UIButton.UIButton(buttonSurf,pg.Rect(pg.Vector2(pg.Vector2(self.screenSurf.get_width()*0.8,self.screenSurf.get_height()*0.8)),pg.Vector2(200,50)),"Back",25,True)
        self.uiGroup.add(self.backBtn)
        
        
    def update(self) -> None:
        self.screenSurf.blit(self.inputOverlay,self.inputPos)
        return super().update()
    
    def portInputValidator(self,input):
        if(len(input)>=1 and len(input)<=4):
            return input.isnumeric()
        elif(len(input)==0):
            return True
        else:
            return False