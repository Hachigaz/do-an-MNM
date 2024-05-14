import controller.game_logic.Logic as Logic

import view.screens.MenuScreen as MenuScreen
import view.screens.subscreens.menu.MultiplayerScreen as MultiplayerScreen
import view.screens.subscreens.menu.BrowseServerScreen as BrowseServerScreen
import view.screens.subscreens.menu.HostOptionScreen as HostOptionScreen

import controller.game_logic.CharacterSelect as CharacterSelect

import controller.game_logic.GameplayLogic as GameplayLogic
import controller.game_logic.LobbyLogic as LobbyLogic

import view.screens.subscreens.dialog.dialog as Dialog

import pygame as pg

class GameMenu (Logic.Logic):
    def __init__(self) -> None:
        pass
        
    def start(self)->None:
        mainScreen = MenuScreen.MenuScreen()
        mainScreen.singlePlayerBtn.setTriggerFunction(self.toSinglePlayer)
        mainScreen.multiplayerBtn.setTriggerFunction(self.toMultiplayer)
        mainScreen.quitBtn.setTriggerFunction(self.doQuitGame)
        
        mainScreen.testGameBtn.setTriggerFunction(self.testPlayGame)
        
        super().start(mainScreen)
        
        
        self.multiplayerScreen = MultiplayerScreen.MultiplayerScreen()
        self.multiplayerScreen.backToMenuBtn.setTriggerFunction(self.backToMenu)
        self.multiplayerScreen.hostBtn.setTriggerFunction(self.toHostOption)
        self.multiplayerScreen.browseBtn.setTriggerFunction(self.toBrowseServer)
        
        self.hostOptionScreen = HostOptionScreen.HostOptionScreen()
        self.hostOptionScreen.createBtn.setTriggerFunction(self.processCreateGameLobby)
        self.hostOptionScreen.backBtn.setTriggerFunction(self.backToMultiplayer)
        
        self.browseServerScreen = BrowseServerScreen.BrowseServerScreen()
        self.browseServerScreen.backBtn.setTriggerFunction(self.backToMultiplayer)
        
        self.nextLogic:Logic = None
        pass
        
    def update(self) -> None:
        super().update()
            
    def toSinglePlayer(self)->None:
        #select character
        character = CharacterSelect.CharacterSelect.doCharacterSelect()
        
        pass
    
    def toMultiplayer(self)->None:
        self.screenControl.replaceScreenByIndex(0,self.multiplayerScreen)
        pass
    
    
    #multiplayer
    
    def toBrowseServer(self)->None:
        self.screenControl.replaceScreenByIndex(0,self.browseServerScreen)
        pass
    
    def toHostOption(self)->None:
        self.screenControl.replaceScreenByIndex(0,self.hostOptionScreen)
        pass
    
    #browse
    
    def joinLobby(self):
        pass
    
    def refreshServers(self)->None:
        pass
    
    def backToMenu(self)->None:
        self.screenControl.replaceScreenByIndex(0,self.mainScreen)
        pass
        
    def backToMultiplayer(self)->None:
        self.screenControl.replaceScreenByIndex(0,self.multiplayerScreen)
        pass 
            
    def testPlayGame(self)->None:
        self.isLogicRunning = False
        self.returnLogic = GameplayLogic.GameplayLogic
        
    def processCreateGameLobby(self):
        if(self.hostOptionScreen.playerNameInput.textInput.value==""):
            dialog = Dialog.Dialog("Please enter player name",pg.Vector2(500,200))
            dialog.confirmButton.setTriggerFunction(self.closeDialog,dialog)
            self.screenControl.addScreenByIndex(1,dialog)
            self.screenControl.currentScreens[0].disableUI()
            self.hostOptionScreen.portInput.is_clickable = False
            self.hostOptionScreen.playerNameInput.is_clickable = False
            return
        
        if(self.hostOptionScreen.portInput.textInput.value==""):
            dialog = Dialog.Dialog("Please enter port number",pg.Vector2(500,200))
            dialog.confirmButton.setTriggerFunction(self.closeDialog,dialog)
            self.screenControl.addScreenByIndex(1,dialog)
            self.screenControl.currentScreens[0].disableUI()
            self.hostOptionScreen.portInput.is_clickable = False
            self.hostOptionScreen.playerNameInput.is_clickable = False
            return            
        
        playerName = self.hostOptionScreen.playerNameInput.textInput.value
        portNumber = self.hostOptionScreen.portInput.textInput.value
        
        self.isLogicRunning = False
        self.returnLogic = LobbyLogic.LobbyLogic(playerName,portNumber)
        
    def closeDialog(self,dialog):
        self.screenControl.removeScreen(dialog)
        self.screenControl.currentScreens[0].enableUI()
        self.hostOptionScreen.portInput.is_clickable = True
        self.hostOptionScreen.playerNameInput.is_clickable = True
        pass