import pygame as pg

import controller.game_logic.Logic as Logic
import controller.game_logic.GameMenu as GameMenu

import view.screens.GameScreen as GameScreen
import view.screens.Gameplay.GameplayScreen as GameplayScreen
import view.screens.Gameplay.PauseScreen as PauseScreen 

import components.game_components.GameSprite as GameSprite

class GameplayLogic(Logic.Logic):
    def __init__(self) -> None:
        super().__init__()
        
    def start(self) -> None:
        mainScreen = GameplayScreen.GameplayScreen()
        super().start(mainScreen)
        
        self.isPauseGame = False
        self.lastPauseGame = 0
        self.pauseScreen = PauseScreen.PauseScreen()
        self.pauseScreen.resumeBtn.setTriggerFunction(self.doResumeGame)
        self.pauseScreen.quitBtn.setTriggerFunction(self.returnToMainMenu)
        
        GameSprite.loadAllSprites()
        pass
    
    def end(self) -> Logic.Logic:
        #123
        
        
        return super().end()
        
    
    def processInputs(self)->None:
        keys = pg.key.get_pressed()
        if keys[pg.K_ESCAPE]:
            if pg.time.get_ticks() - self.lastPauseGame > 500:
                if(not self.isPauseGame):
                    self.doPauseGame()
        pass
        
    def handleGameplayInputs(self)->None:
        pass
            
    def handlePauseInputs(self)->None:
        pass
            
    def doPauseGame(self)->None:
        self.lastPauseGame = pg.time.get_ticks()
        self.screenControl.addScreen(self.pauseScreen)
        self.isPauseGame = True
        pass
    
    def update(self) -> None:
        self.screenControl.update()
        self.processInputs()
    
    def doResumeGame(self)->None:
        self.screenControl.removeScreen(self.pauseScreen)
        self.isPauseGame = False
    
    def returnToMainMenu(self)->None:
        self.isLogicRunning = False
        self.returnLogic = GameMenu.GameMenu
        pass
    pass