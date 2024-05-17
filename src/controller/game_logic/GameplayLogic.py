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
import view.screens.subscreens.dialog.dialog as Dialog

MODEL_BROADCAST_MESSAGE = {
    "proc":"MyPythonGame",
    "stage":"gameplay",
    "func":"game_model_broadcast",
    "data":{
        "game_model":None
    }
}
CLIENT_GAMEPLAY_ACTION_MESSAGE = {
    "proc":"MyPythonGame",
    "stage":"gameplay",
    "func":"player_action",
    "data":{
        "actions":[]
    }
}
CLIENT_QUIT_MESSAGE = {
    "proc":"MyPythonGame",
    "stage":"gameplay",
    "func":"client_quit",
    "data":{
        
    }
}
HOST_QUIT_MESSAGE = {
    "proc":"MyPythonGame",
    "stage":"gameplay",
    "func":"host_quit",
    "data":{
        
    }
}

CLIENT_LOSE_MESSAGE = {
    "proc":"MyPythonGame",
    "stage":"gameplay",
    "func":"client_lose",
    "data":{
        
    }
}

CLIENT_WIN_MESSAGE = {
    "proc":"MyPythonGame",
    "stage":"gameplay",
    "func":"client_win",
    "data":{
        
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
        self.clientSockets:dict[tuple[str,int],socket.socket]=clientSockets
        
        self.currentPlayerIP = currentPlayerIP
        self.GAME_SETTING = {
            "player_count":len(playerList),
            "player_list":playerList,
            "health_count":5        
        }
        print(self.GAME_SETTING)
        
    def start(self) -> None:
        mainScreen = GameplayScreen.GameplayScreen(self.GAME_SETTING["player_count"],0)
        super().start(mainScreen)
        
        self.isPauseGame = False
        self.lastPauseGame = 0
        self.pauseScreen = PauseScreen.PauseScreen()
        self.pauseScreen.resumeBtn.setTriggerFunction(self.doResumeGame)
        self.pauseScreen.quitBtn.setTriggerFunction(self.returnToMainMenu)
        
        self.gameModel:GameModel.GameModel = GameModel.GameModel(self.GAME_SETTING,GameScreen.GameScreen.screenSurf)
        self.currentPlayer = self.gameModel.players[self.currentPlayerIP]
        
        for ip,socket in self.clientSockets.items():
            socketConnectionThread = threading.Thread(target=self.handleConnection,args=[ip,socket])
            socketConnectionThread.start()
        pass
    
    def end(self) -> Logic.Logic:
        self.hostSocket.close()
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
            
        if(keys[pg.K_SPACE]):
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
        hostQuitMessage = HOST_QUIT_MESSAGE
        for k,cli in self.clientSockets.items():
            cli.send(pickle.dumps(hostQuitMessage))
        
        self.isLogicRunning = False
        self.returnLogic = GameMenu.GameMenu
        pass
    
    def broadcastGameModel(self):
        gameModelMessage = MODEL_BROADCAST_MESSAGE
        gameModelMessage["data"]["game_model"]=self.gameModel.getGameModelData()
        gameModelMessage["data"]["player_position_list"]=[pg.Vector2(p.body.position[0],p.body.position[1]) for k,p in self.gameModel.players.items()]
        for ip,socket in self.clientSockets.items():
            gameModelMessage["data"]["viewport_pos"]=self.gameModel.players[ip].body.position
            gameModelMessage["data"]["player_health"]=self.gameModel.players[ip].health
            socket.send(pickle.dumps(gameModelMessage))
        pass
    
    def checkPlayerHealth(self)->None:
        pass
    
    def checkWinCondition(self)->None:
        if(len([p for ip,p in self.gameModel.players.items() if p.isAlive ])<2):
            if self.currentPlayer.health>0:
                self.showWinScreen()
                for k,client in self.clientSockets.items():
                    client.send(pickle.dumps(CLIENT_LOSE_MESSAGE))
                    
            else:
                self.showLoseScreen()
                for k,client in self.clientSockets.items():
                    if self.gameModel.players[k].health>0:
                        client.send(pickle.dumps(CLIENT_WIN_MESSAGE))
                    else:
                        client.send(pickle.dumps(CLIENT_LOSE_MESSAGE))
        pass
    pass

    def showWinScreen(self):
        dialog = Dialog.Dialog("You win",pg.Vector2(self.windowSurface.get_width()*0.6,300),"Quit")
        self.screenControl.addScreenByIndex(2,dialog)
        self.screenControl.currentScreens[0].disableUI()
        
        params = [
        
        ]
        dialog.confirmButton.setTriggerFunction(self.returnToMainMenu,params)
        pass
    
    def showLoseScreen(self):
        dialog = Dialog.Dialog("You lose",pg.Vector2(self.windowSurface.get_width()*0.6,300),"Quit")
        self.screenControl.addScreenByIndex(2,dialog)
        self.screenControl.currentScreens[0].disableUI()
        
        params = [
        
        ]
        dialog.confirmButton.setTriggerFunction(self.returnToMainMenu,params)
        pass
    
    def showDeathScreen(self):
        dialog = Dialog.Dialog("You died",pg.Vector2(self.windowSurface.get_width()*0.6,300),"Continue")
        self.screenControl.addScreenByIndex(2,dialog)
        self.screenControl.currentScreens[0].disableUI()
        
        params = [
        dialog
        ]
        dialog.confirmButton.setTriggerFunction(self.closeDialog,params)
        pass
    
    def closeDialog(self,dialog):
        self.screenControl.removeScreen(dialog)
        self.screenControl.currentScreens[0].enableUI()
        pass

    def handleConnection(self,address,clientSocket:socket.socket):
        isHandlingConnection = True
        print("handling connection:",address)
        while isHandlingConnection:
            try:
                data = pickle.loads(clientSocket.recv(8192))
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
                if(func=="player_action"):
                    actions = funcData["actions"]
                    if "move_forward" in actions:
                        self.gameModel.players[address].moveForward()
                    if "rotate_left" in actions:
                        self.gameModel.players[address].spinLeft()
                    if "rotate_right" in actions:
                        self.gameModel.players[address].spinRight()
                    if "brake" in actions:
                        self.gameModel.players[address].brake()
                    if "fire_cannon" in actions:
                        self.gameModel.players[address].fireCannon()
                if(func=="client_quit"):
                    self.gameModel.players[address].playerDie()
                    self.clientSockets.pop(address)
                    isHandlingConnection = False
            except socket.timeout as e:
                pass
            except Exception as e:
                print("EXCEPTION:", e)
                isHandlingConnection = False
                
        
class ClientLogic(Logic.Logic):
    def __init__(self,currentPlayerIP,clientSocket:socket.socket,playerCount:int,playerIndex) -> None:
        self.currentPlayerIP = currentPlayerIP
        self.clientSocket:socket.socket = clientSocket
        self.gameModelData = None
        self.playerPosList = None
        self.playerHealth = None
        self.playerCount = playerCount
        self.playerIndex = playerIndex
        pass
    
    def start(self) -> None:
        self.gameModel:GameModel.ClientGameModel = GameModel.ClientGameModel(self.windowSurface)
        # self.updateGameModel()
        
        
        mainScreen = GameplayScreen.GameplayScreen(self.playerCount,self.playerIndex)
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
        
        self.gameModel.render()
        if(self.gameModelData!=None):
            self.gameModel.renderGameModelData(self.gameModelData)
        
        if(self.playerPosList!=None):
            self.mainScreen.mapDisplay.update(self.playerPosList)
        if(self.playerHealth!=None):
            self.mainScreen.playerHealthDisplay.update(self.playerHealth)
        
        self.screenControl.update()
       
    def end(self) -> tuple[Logic.Logic, list]:
        self.clientSocket.close()
        return super().end()
            
    def doPauseGame(self)->None:
        self.lastPauseGame = pg.time.get_ticks()
        self.screenControl.addScreen(self.pauseScreen)
        self.isPauseGame = True
        pass     
    
    def doResumeGame(self)->None:
        self.screenControl.removeScreen(self.pauseScreen)
        self.isPauseGame = False
    
    def returnToMainMenu(self)->None:
        clientQuitMessage = CLIENT_QUIT_MESSAGE
        self.clientSocket.send(pickle.dumps(clientQuitMessage))
        
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
        data = pickle.loads(self.clientSocket.recv(8192))
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
            self.playerPosList = funcData["player_position_list"]
            self.playerHealth = funcData["player_health"]
        if(func=="host_quit"):
            self.showHostQuitScreen()
        if(func=="client_win"):
            self.showWinScreen()
        if(func=="client_lose"):
            self.showLoseScreen()
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
        playerActionMessage = CLIENT_GAMEPLAY_ACTION_MESSAGE
        playerActionMessage["data"]["actions"].clear()
        if(keys[pg.K_w]):
            playerActionMessage["data"]["actions"].append("move_forward")
            pass
        
        if(keys[pg.K_a]):
            playerActionMessage["data"]["actions"].append("rotate_left")
            pass
            
        if(keys[pg.K_d]):
            playerActionMessage["data"]["actions"].append("rotate_right")
            pass
            
        if(keys[pg.K_s]):
            playerActionMessage["data"]["actions"].append("brake")
            pass
        
        if(keys[pg.K_SPACE]):
            playerActionMessage["data"]["actions"].append("fire_cannon")
            pass            
        self.clientSocket.send(pickle.dumps(playerActionMessage))
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
        
        

    def showWinScreen(self):
        dialog = Dialog.Dialog("You win",pg.Vector2(self.windowSurface.get_width()*0.6,300),"Quit")
        self.screenControl.addScreenByIndex(2,dialog)
        self.screenControl.currentScreens[0].disableUI()
        
        params = [
        
        ]
        dialog.confirmButton.setTriggerFunction(self.returnToMainMenu,params)
        pass
    
    def showLoseScreen(self):
        dialog = Dialog.Dialog("You lose",pg.Vector2(self.windowSurface.get_width()*0.6,300),"Quit")
        self.screenControl.addScreenByIndex(2,dialog)
        self.screenControl.currentScreens[0].disableUI()
        
        params = [
        
        ]
        dialog.confirmButton.setTriggerFunction(self.returnToMainMenu,params)
        pass
    
    def showDeathScreen(self):
        dialog = Dialog.Dialog("You died",pg.Vector2(self.windowSurface.get_width()*0.6,300),"CONTINUE")
        self.screenControl.addScreenByIndex(2,dialog)
        self.screenControl.currentScreens[0].disableUI()
        
        params = [
        dialog
        ]
        dialog.confirmButton.setTriggerFunction(self.closeDialog,params)
        pass
    
    def showHostQuitScreen(self):
        dialog = Dialog.Dialog("Host has quit the game",pg.Vector2(self.windowSurface.get_width()*0.6,300),"QUIT")
        self.screenControl.addScreenByIndex(2,dialog)
        self.screenControl.currentScreens[0].disableUI()
        
        params = [
        
        ]
        dialog.confirmButton.setTriggerFunction(self.returnToMainMenu,params)
        pass
    
    def closeDialog(self,dialog):
        self.screenControl.removeScreen(dialog)
        self.screenControl.currentScreens[0].enableUI()
        pass
