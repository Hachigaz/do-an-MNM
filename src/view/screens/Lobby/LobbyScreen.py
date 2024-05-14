import view.screens.GameScreen as GameScreen
import pygame as pg
import components.UI.ui_components.ChatBox as ChatBox

class LobbyPlayer:
    def __init__(self,name:str) -> None:
        self.name:str = name
        pass
    
class LobbyScreen(GameScreen.GameScreen):
    def __init__(self) -> None:
        super().__init__()
        self.messages = ChatBox.MessageList()
        self.chatBox = ChatBox.ChatBox(pg.rect.Rect(pg.Vector2(0,self.screenSurf.get_height()*0.7),pg.Vector2(0.4*self.screenSurf.get_width(),0.3*self.screenSurf.get_height())),self.messages)

        self.players:list[LobbyPlayer] = {}
    pass

    def processPlayerJoin(self,playerName:str):
        self.players[playerName]=LobbyPlayer(playerName)
        pass
    
    def processPlayerLeave(self,playerName:str):
        pass

    def update(self) -> None:
        self.chatBox.update(self.screenSurf)
        
        return super().update()