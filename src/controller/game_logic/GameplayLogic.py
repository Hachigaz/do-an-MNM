import pygame as pg 

import controller.game_logic.Logic as Logic
import controller.game_logic.GameMenu as GameMenu

import view.screens.GameScreen as GameScreen
import view.screens.Gameplay.GameplayScreen as GameplayScreen
import view.screens.Gameplay.PauseScreen as PauseScreen 

import socket
import pickle
import threading

import model.game_model.GameModel as GameModel


MODEL_BROADCAST_MESSAGE = {
    "proc":"MyPythonGame",
    "stage":"gameplay",
    "func":"game_model_broadcast",
    "data":{
        "game_model":None
    }
}

class GameplayLogic(Logic.Logic):
    def __init__(self,playerList,currentPlayerIP) -> None:
        super().__init__()
        self.currentPlayerIP = currentPlayerIP
        self.GAME_SETTING = {
            "player_count":len(playerList),
            "player_list":playerList,
            "health_count":5            
        }
        
    def start(self) -> None:
        mainScreen = GameplayScreen.GameplayScreen(self.GAME_SETTING["player_count"])
        super().start(mainScreen)
        
        self.isPauseGame = False
        self.lastPauseGame = 0
        self.pauseScreen = PauseScreen.PauseScreen()
        self.pauseScreen.resumeBtn.setTriggerFunction(self.doResumeGame)
        self.pauseScreen.quitBtn.setTriggerFunction(self.returnToMainMenu)
        
        
        self.gameModel = GameModel.GameModel(self.GAME_SETTING,GameScreen.GameScreen.screenSurf,0)
        
        self.currentPlayer = self.gameModel.players[self.currentPlayerIP]
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


class HostLogic(Logic.Logic):
    def __init__(self,currentPlayerIP,playerList,hostSocket,clientSockets) -> None:
        super().__init__()
        self.playerList:tuple[tuple[str,int],str] = playerList
        self.hostSocket:socket.socket = hostSocket
        self.clientSockets:tuple[tuple[str,int],socket.socket]=clientSockets
        
        self.currentPlayerIP = currentPlayerIP
        self.GAME_SETTING = {
            "player_count":len(playerList),
            "player_list":playerList,
            "health_count":5        
        }
        print(self.GAME_SETTING)
        
    def start(self) -> None:
        mainScreen = GameplayScreen.GameplayScreen(self.GAME_SETTING["player_count"])
        super().start(mainScreen)
        
        self.isPauseGame = False
        self.lastPauseGame = 0
        self.pauseScreen = PauseScreen.PauseScreen()
        self.pauseScreen.resumeBtn.setTriggerFunction(self.doResumeGame)
        self.pauseScreen.quitBtn.setTriggerFunction(self.returnToMainMenu)
        
        self.gameModel:GameModel.GameModel = GameModel.GameModel(self.GAME_SETTING,GameScreen.GameScreen.screenSurf)
        # self.broadcastGameModel()
        self.currentPlayer = self.gameModel.players[self.currentPlayerIP]
        
        for ip,socket in self.clientSockets.items():
            socketConnectionThread = threading.Thread(target=self.handleConnection,args=[ip,socket])
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
        
        gameModelBroadcastThread = threading.Thread(target=self.broadcastGameModel)
        gameModelBroadcastThread.start()
        self.gameModel.render(self.currentPlayerIP)
        
        self.mainScreen.mapDisplay.update([pg.Vector2(player.body.position[0],player.body.position[1]) for ip,player in self.gameModel.players.items()])
        self.mainScreen.playerHealthDisplay.update(self.currentPlayer.health)
        
        self.screenControl.update()
        
        self.checkWinCondition()
        gameModelBroadcastThread.join()
    
    def doResumeGame(self)->None:
        self.screenControl.removeScreen(self.pauseScreen)
        self.isPauseGame = False
    
    def returnToMainMenu(self)->None:
        self.currentPlayer.health = 0
        
        self.isLogicRunning = False
        self.returnLogic = GameMenu.GameMenu
        pass
    
    def broadcastGameModel(self):
        gameModelMessage = MODEL_BROADCAST_MESSAGE
        gameModelMessage["data"]["game_model"]=self.gameModel.getGameModelData()
        for ip,socket in self.clientSockets.items():
            gameModelMessage["data"]["viewport_pos"]=self.gameModel.players[ip].body.position
            socket.send(pickle.dumps(gameModelMessage))
        pass
    
    def checkWinCondition(self)->None:
        if(len([p for ip,p in self.gameModel.players.items() if p.health==0 ])<2):
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
    pass

    def handleConnection(self,address,clientSocket:socket.socket):
        isHandlingConnection = True
        print("handling connection:",address)
        while isHandlingConnection:
            data = pickle.loads(clientSocket.recv(4096))
            if data["proc"]!="MyPythonGame":
                isHandlingConnection=False
                print("Error handling")
                return
            if data["stage"] != "gameplay":
                isHandlingConnection = False
                print("Error handling2")
                return
            func = data["func"]
            funcData = data["data"]
                
        
class ClientLogic(Logic.Logic):
    def __init__(self,currentPlayerIP,clientSocket:socket.socket) -> None:
        self.currentPlayerIP = currentPlayerIP
        self.clientSocket:socket.socket = clientSocket
        self.gameModelData = None
        pass
    
    def start(self) -> None:
        self.gameModel:GameModel.ClientGameModel = GameModel.ClientGameModel(self.windowSurface)
        # self.updateGameModel()
        
        playerCount = 2
        
        mainScreen = GameplayScreen.GameplayScreen(playerCount)
        super().start(mainScreen)
        
        self.isPauseGame = False
        self.lastPauseGame = 0
        self.pauseScreen = PauseScreen.PauseScreen()
        self.pauseScreen.resumeBtn.setTriggerFunction(self.doResumeGame)
        self.pauseScreen.quitBtn.setTriggerFunction(self.returnToMainMenu)
        # self.currentPlayer = self.gameModel.players[self.currentPlayerIP]
    
        super().start(mainScreen)
    
    def update(self) -> None:
        self.processInputs()
        
        gameModelUpdateThread = threading.Thread(target=self.updateGameModel)
        gameModelUpdateThread.start()
        
        self.gameModel.render((100,100))
        if(self.gameModelData!=None):
            self.gameModel.renderGameModelData(self.gameModelData)
        
        self.mainScreen.mapDisplay.update([pg.Vector2(100,100),pg.Vector2(100,300)])
        self.mainScreen.playerHealthDisplay.update(5)
        
        self.screenControl.update()
       
            
    def doPauseGame(self)->None:
        self.lastPauseGame = pg.time.get_ticks()
        self.screenControl.addScreen(self.pauseScreen)
        self.isPauseGame = True
        pass     
    
    def doResumeGame(self)->None:
        self.screenControl.removeScreen(self.pauseScreen)
        self.isPauseGame = False
    
    def returnToMainMenu(self)->None:
        self.currentPlayer.health = 0
        
        self.isLogicRunning = False
        self.returnLogic = GameMenu.GameMenu
        pass
        
    # def hanndleConnection(self):
    #     isHandlingConnection = True
    #     while isHandlingConnection:
    #         data = pickle.loads(self.clientSocket.recv(4096))
    #         if data["proc"]!="MyPythonGame":
    #             isHandlingConnection=False
    #             print("Error handling")
    #             return
    #         if data["stage"] != "gameplay":
    #             isHandlingConnection = False
    #             print("Error handling2")
    #             return
    #         func = data["func"]
    #         funcData = data["data"]
    #         if(func=="game_model_broadcast"):
    #             self.gameModel = funcData["game_model"]
    #     pass
    
    def updateGameModel(self):
        data = pickle.loads(self.clientSocket.recv(4096))
        if data["proc"]!="MyPythonGame":
            isHandlingConnection=False
            print("Error handling")
            return
        if data["stage"] != "gameplay":
            isHandlingConnection = False
            print("Error handling2")
            return
        func = data["func"]
        funcData = data["data"]
        if(func=="game_model_broadcast"):
            self.gameModelData = funcData["game_model"]
            self.gameModel.updateViewportPosition(funcData["viewport_pos"])
            # self.playerPosList = funcData
        pass
    
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
            pass
        
        if(keys[pg.K_a]):
            pass
            
        if(keys[pg.K_d]):
            pass
            
        if(keys[pg.K_s]):
            pass
        
        if(keys[pg.K_SPACE]):
            pass
            
        pass
            
    def handlePauseInputs(self,keys)->None:
        pass

    def showEndGameScreen(self):
        if self.currentPlayer.health > 0:
            #you win
            pass
        else:
            #you lose
            pass