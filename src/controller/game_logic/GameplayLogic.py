import controller.game_logic.Logic as Logic
import view.screens.GameScreen as GameScreen
import view.screens.GameplayScreen as GameplayScreen

class GameplayLogic(Logic.Logic):
    def __init__(self) -> None:
        mainScreen = GameplayScreen.GameplayScreen()
        super().__init__(mainScreen)
        
        self.pauseScreen = PauseScreen.PauseScreen()
        self.pauseScreen.quitButton.setTriggerFunction(self.returnToMainMenu)
        
    def end()->None:
        #un laod file
        pass
    def returnToMainMenu(self)->None:
        self.isLogicRunning = False
        self.end()
        pass
    pass