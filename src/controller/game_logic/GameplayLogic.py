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
        GAME_SETTING = {
            "player_count":2,
            "health_count":5            
        }
        mainScreen = GameplayScreen.GameplayScreen(GAME_SETTING["player_count"])
        super().start(mainScreen)
        
        self.isPauseGame = False
        self.lastPauseGame = 0
        self.pauseScreen = PauseScreen.PauseScreen()
        self.pauseScreen.resumeBtn.setTriggerFunction(self.doResumeGame)
        self.pauseScreen.quitBtn.setTriggerFunction(self.returnToMainMenu)
        
        
        self.gameModel = GameModel.GameModel(GAME_SETTING,GameScreen.GameScreen.screenSurf,0)
        
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
            # self.currentPlayer.jump()
            self.currentPlayer.moveForward()
        
        if(keys[pg.K_a]):
            self.currentPlayer.spinLeft()
            
        if(keys[pg.K_d]):
            self.currentPlayer.spinRight()
            
        if(keys[pg.K_s]):
            self.currentPlayer.brake()
            
        # if(keys[pg.K_UP]):
        #     self.currentPlayer.rotateCannonUp()
            
        # if(keys[pg.K_DOWN]):
        #     self.currentPlayer.rotateCannonDown()
            
        if(keys[pg.K_SPACE]):
            if(pg.time.get_ticks() - self.currentPlayer.lastFired > 1000):
                self.currentPlayer.lastFired = pg.time.get_ticks()
                self.currentPlayer.fireCannon()
            
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
        self.gameModel.render()
        
        self.mainScreen.mapDisplay.update([pg.Vector2(player.body.position[0],player.body.position[1]) for player in self.gameModel.players])
        self.mainScreen.playerHealthDisplay.update(self.currentPlayer.health)
        
        self.screenControl.update()
        
        self.checkWinCondition()
    
    def doResumeGame(self)->None:
        self.screenControl.removeScreen(self.pauseScreen)
        self.isPauseGame = False
    
    def returnToMainMenu(self)->None:
        self.currentPlayer.health = 0
        
        self.isLogicRunning = False
        self.returnLogic = GameMenu.GameMenu
        pass
    
    def checkWinCondition(self)->None:
        if(len([p for p in self.gameModel.players if p.health==0 ])<2):
            self.showEndGameScreen()
        pass
    pass

    def showEndGameScreen(self):
        if self.currentPlayer.health > 0:
            #you win
            pass
        else:
            #you lose
            pass

#input -> render update ->  


class HostLogic:
    pass

class ClientLogic:
    pass