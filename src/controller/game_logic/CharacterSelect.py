import controller.game_logic.Logic as Logic
import view.screens.CharacterSelectScreen as CharacterSelectScreen
from view.screens.GameScreen import GameScreen
class Character:
    pass

class CharacterSelect(Logic.Logic):
    def doCharacterSelect()->Character:
        characterSelect = CharacterSelect()
        characterSelect.start()
        characterSelect.loop()
        characterSelect.end()
        
        return characterSelect.getSelectedCharacter()
    
    def __init__(self) -> None:
        super().__init__()
        
    def start(self) -> None:
        mainScreen = CharacterSelectScreen.CharacterSelectScreen()
        mainScreen.backToMenuButton.setTriggerFunction(self.doReturnToMenu)
        super().start(mainScreen)
    
    def getSelectedCharacter(self)->Character:
        return self.mainScreen.characterSelectBox.getSelectedValue()
    
    def doReturnToMenu(self)->None:
        self.isLogicRunning = False
    pass