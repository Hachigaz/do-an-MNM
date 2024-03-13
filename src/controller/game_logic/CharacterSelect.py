import controller.game_logic.Logic as Logic
import view.screens.CharacterSelectScreen as CharacterSelectScreen
class Character:
    pass

class CharacterSelect(Logic.Logic):
    def doCharacterSelect()->Character:
        characterSelect = CharacterSelect()
        
        characterSelect.run()
        
        return characterSelect.getSelectedCharacter()
    
    def __init__(self) -> None:
        mainScreen = CharacterSelectScreen.CharacterSelectScreen()
        mainScreen.backToMenuButton.setTriggerFunction(self.doReturnToMenu)
        super().__init__(mainScreen)
        
    def start(self) -> None:
        pass
    
    def getSelectedCharacter(self)->Character:
        pass
    
    def doReturnToMenu(self)->None:
        self.isLogicRunning = False
    pass