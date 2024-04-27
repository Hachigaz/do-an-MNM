import pygame as pg

import controller.game_logic.Logic as Logic
import controller.game_logic.GameMenu as GameMenu

import view.screens.GameScreen as GameScreen
import view.screens.Gameplay.GameplayScreen as GameplayScreen
import view.screens.Gameplay.PauseScreen as PauseScreen 


import model.game_model.GameModel as GameModel
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
        
        selectedCharacters = ["Converted_Vampire","Countess_Vampire"]
        selectedMap = "map01"
        self.gameModel = GameModel.GameModel(selectedCharacters,selectedMap,GameScreen.GameScreen.screenSurf)
        
        self.currentPlayer = self.gameModel.players[0]
        pass
    
    def end(self) -> Logic.Logic:
        
        
        return super().end()
        
    
    def processInputs(self)->None:
        keys = pg.key.get_pressed()
        if keys[pg.K_ESCAPE]:
            if pg.time.get_ticks() - self.lastPauseGame > 500:
                if(not self.isPauseGame):
                    self.doPauseGame()
                    
        if(self.isPauseGame):
            self.handlePauseInputs(keys)
        else:
            self.handleGameplayInputs(keys)
    
        pass
        
    def handleGameplayInputs(self,keys)->None:
        if(keys[pg.K_w]):
            self.currentPlayer.jump()
        
        if(keys[pg.K_a]):
            self.currentPlayer.moveRight()
            
        if(keys[pg.K_d]):
            self.currentPlayer.moveLeft()
        
        if(keys[pg.K_j]):
            self.currentPlayer.attack1()
        
        if(keys[pg.K_k]):
            self.currentPlayer.attack2()
        
        if(keys[pg.K_l]):
            self.currentPlayer.attack3()
        pass
            
    def handlePauseInputs(self,keys)->None:
        pass
            
    def doPauseGame(self)->None:
        self.lastPauseGame = pg.time.get_ticks()
        self.screenControl.addScreen(self.pauseScreen)
        self.isPauseGame = True
        pass
    
    def update(self) -> None:
        self.processInputs()
        
        self.gameModel.update()
        
        self.screenControl.update()
    
    def doResumeGame(self)->None:
        self.screenControl.removeScreen(self.pauseScreen)
        self.isPauseGame = False
    
    def returnToMainMenu(self)->None:
        self.isLogicRunning = False
        self.returnLogic = GameMenu.GameMenu
        pass
    pass

#input -> render update ->  