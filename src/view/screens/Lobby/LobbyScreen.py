import view.screens.GameScreen as GameScreen
import pygame as pg
import components.UI.ui_components.ChatBox as ChatBox
import components.UI.UIButton as UIButton
import components.UI.UIText as UIText

import components.game_components.Textures as Textures;

class LobbyScreen(GameScreen.GameScreen):
    def __init__(self,isHosting = False) -> None:
        super().__init__()
        
        title = UIText.UIText(pg.font.Font("resources/ui/Font/kenvector_future.ttf",40),"Lobby",pg.Vector2(0.5*self.screenSurf.get_width(),100))
        self.uiGroup.add(title)
        
        buttonSurf = Textures.getLoadedSurfaces("blue_button00")
        
        self.messages = ChatBox.MessageList()
        self.chatBox = ChatBox.ChatBox(pg.rect.Rect(pg.Vector2(0,self.screenSurf.get_height()*0.7),pg.Vector2(0.4*self.screenSurf.get_width(),0.3*self.screenSurf.get_height())),self.messages)

        self.returnToMenuBtn = UIButton.UIButton(buttonSurf,pg.Rect(pg.Vector2(pg.Vector2(0.9*self.screenSurf.get_width(),0.9*self.screenSurf.get_height())),pg.Vector2(200,50)),"Leave",25)
        self.uiGroup.add(self.returnToMenuBtn)
        
        if isHosting:
            self.startGameBtn = UIButton.UIButton(buttonSurf,pg.Rect(pg.Vector2(pg.Vector2(0.75*self.screenSurf.get_width(),0.9*self.screenSurf.get_height())),pg.Vector2(200,50)),"Start",25)
            self.uiGroup.add(self.startGameBtn)
        
        self.playerListSize = pg.Vector2(0.3*self.screenSurf.get_width(),0.2*self.screenSurf.get_height())
        
        self.playerListOverlay = pg.surface.Surface(self.playerListSize,pg.SRCALPHA,32)
        self.playerListPos = pg.Vector2(0,0)

        self.playerListTitle = UIText.UIText(pg.font.Font("resources/ui/Font/kenvector_future.ttf",23),"Players",self.playerListPos+pg.Vector2(10,10),True)
        # self.playerListTitle = UIText.UIText(pg.font.SysFont("Arial",20),"Players",self.playerListPos+pg.Vector2(10,10),True)
        self.uiGroup.add(self.playerListTitle)
        
        self.playerListOverlay.fill(pg.color.Color(255,255,255,50))
        self.playerRenderList:dict[str:UIText.UIText] = {}
    pass

    def addPlayer(self,ipAddress,playerName:str):
        self.playerRenderList[ipAddress] = UIText.UIText(pg.font.Font("resources/ui/Font/kenvector_future.ttf",20),playerName,self.playerListPos + pg.Vector2(20,40+22*len(self.playerRenderList)),True)

    def removePlayer(self,ip,playerName:str):
        self.playerRenderList.pop(ip)

    def update(self) -> None:
        self.chatBox.update(self.screenSurf)
        
        self.chatBox.textInput.update(self.screenSurf)
        
        self.screenSurf.blit(self.playerListOverlay,self.playerListPos)
        
        for key,name in self.playerRenderList.items():
            name.update(self.screenSurf)
               
        return super().update()