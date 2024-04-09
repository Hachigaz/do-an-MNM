import controller.game_logic.Logic as Logic
import view.screens.GameScreen as GameScreen
import view.screens.LobbyScreen as LobbyScreen 

class LobbyLogic(Logic.Logic):
    def __init__(self) -> None:
        mainScreen = LobbyScreen.LobbyScreen()
        super().__init__(mainScreen)
        
    def end()->None:
        #un laod file
        pass

    def returnToMainMenu(self)->None:
        self.isLogicRunning = False
        
        pass
    pass