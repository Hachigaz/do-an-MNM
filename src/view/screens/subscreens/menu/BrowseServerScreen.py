import pygame as pg

import components.game_components.Textures as Textures;
import components.UI.UIText as UIText
import components.UI.UIButton as UIButton
import components.UI.UITextInput as UITextInput
import components.UI.ui_components.ServerListTable as ServerListTable

import view.screens.GameScreen as GameScreen



class BrowseServerScreen(GameScreen.GameScreen):
    def __init__(self) -> None:
        super().__init__()
        
        self.serverListTable = ServerListTable.ServerListTable(self.screenSurf)
        
        buttonSurf = Textures.getLoadedSurfaces("blue_button00")
        
        screenCenterPos:pg.Vector2=  pg.Vector2(self.screenSurf.get_rect().center)
        
        title = UIText.UIText(pg.font.Font("resources/ui/Font/kenvector_future.ttf",35),"Browse",pg.Vector2(screenCenterPos.x,50))
        self.uiGroup.add(title)
        
        menuBtnsOffsetY=200
        self.refreshBtn = UIButton.UIButton(buttonSurf,pg.Rect(pg.Vector2(self.serverListTable.tablePos.x,self.serverListTable.tablePos.y+self.serverListTable.tableSize.y+80),pg.Vector2(200,60)),"Refresh",25)
        self.uiGroup.add(self.refreshBtn)
        self.joinSelectedBtn = UIButton.UIButton(buttonSurf,pg.Rect(pg.Vector2(self.serverListTable.tablePos.x + 220,self.serverListTable.tablePos.y+self.serverListTable.tableSize.y+80),pg.Vector2(200,60)),"Join",25)
        self.uiGroup.add(self.joinSelectedBtn)
        self.backBtn = UIButton.UIButton(buttonSurf,pg.Rect(pg.Vector2(self.screenSurf.get_width()*0.8,self.serverListTable.tablePos.y+self.serverListTable.tableSize.y+80),pg.Vector2(200,60)),"Back",25)
        self.uiGroup.add(self.backBtn)
        
        
        self.playerNameTextInputLabel = UIText.UIText(pg.font.Font("resources/ui/Font/kenvector_future.ttf",20),"Player name",pg.Vector2(0.8*self.screenSurf.get_width(),self.serverListTable.tablePos.y + 100),True)
        self.uiGroup.add(self.playerNameTextInputLabel)
        self.playerNameInput = UITextInput.UITextInput(pg.rect.Rect(pg.Vector2(0.8*self.screenSurf.get_width(),self.serverListTable.tablePos.y + 150),(300,0)),"Player",lambda x:len(x)<=20,20,True)
        self.uiGroup.add(self.playerNameInput)
        
    
    def update(self) -> None:
        self.serverListTable.update(self.screenSurf)
        return super().update()