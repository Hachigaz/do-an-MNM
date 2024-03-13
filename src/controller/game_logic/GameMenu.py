import controller.game_logic.Logic as Logic

import view.screens.MenuScreen as MenuScreen
import view.screens.subscreens.menu.MultiplayerScreen as MultiplayerScreen
import controller.game_logic.CharacterSelect as CharacterSelect

class GameMenu(Logic.Logic):
    def __init__(self) -> None:
        mainScreen = MenuScreen.MenuScreen()
        mainScreen.singlePlayerBtn.setTriggerFunction(self.toSinglePlayer)
        mainScreen.multiplayerBtn.setTriggerFunction(self.toMultiplayer)
        mainScreen.quitBtn.setTriggerFunction(self.doQuitGame)
        
        super().__init__(mainScreen)
        
        
        self.multiplayerScreen = MultiplayerScreen.MultiplayerScreen()
        self.multiplayerScreen.backToMenuBtn.setTriggerFunction(self.backToMenu)
        
        self.run()
        
    def start(self)->None:
        pass
        
    def update(self) -> None:
        super().update()
            
    def toSinglePlayer(self)->None:
        #select character
        character = CharacterSelect.CharacterSelect.doCharacterSelect()
        
        pass
    
    def toMultiplayer(self)->None:
        self.currentScreen = self.multiplayerScreen
        pass
    def backToMenu(self)->None:
        self.currentScreen = self.mainScreen