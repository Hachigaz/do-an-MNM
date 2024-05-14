import controller.game_logic.Logic as Logic
import view.screens.GameScreen as GameScreen
import view.screens.Lobby.LobbyScreen as LobbyScreen 
import socket as socket
class HostLobbyLogic(Logic.Logic):
    def __init__(self,playerName:str,portNumber:str) -> None:
        super().__init__()
        self.portNumber:str=portNumber
    
    def start(self) -> None:
        mainScreen = LobbyScreen.LobbyScreen()
        super().start(mainScreen)    
    
        socket.create_server(("",self.portNumber))
    
    def end()->None:
        
        pass

    def returnToMainMenu(self)->None:
        self.isLogicRunning = False
        
        pass
    pass

class ClientLobbyLogic(Logic.Logic):
    pass