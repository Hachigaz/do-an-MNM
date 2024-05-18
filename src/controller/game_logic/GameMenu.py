import controller.game_logic.Logic as Logic

import view.screens.MenuScreen as MenuScreen
import view.screens.subscreens.menu.MultiplayerScreen as MultiplayerScreen
import view.screens.subscreens.menu.BrowseServerScreen as BrowseServerScreen
import view.screens.subscreens.menu.HostOptionScreen as HostOptionScreen
import view.screens.subscreens.menu.JoinByIPScreen as JoinByIPScreen

import controller.game_logic.CharacterSelect as CharacterSelect

import controller.game_logic.GameplayLogic as GameplayLogic
import controller.game_logic.LobbyLogic as LobbyLogic

import view.screens.subscreens.dialog.dialog as Dialog

import pygame as pg
import socket
import ipaddress
import pickle
import threading

class GameMenu (Logic.Logic):
    def __init__(self) -> None:
        pass
        
    def start(self)->None:
        mainScreen = MenuScreen.MenuScreen()
        mainScreen.singlePlayerBtn.setTriggerFunction(self.toSinglePlayer)
        mainScreen.multiplayerBtn.setTriggerFunction(self.toMultiplayer)
        mainScreen.quitBtn.setTriggerFunction(self.doQuitGame)
        
        # mainScreen.testGameBtn.setTriggerFunction(self.testPlayGame)
        
        super().start(mainScreen)
        
        
        self.multiplayerScreen = MultiplayerScreen.MultiplayerScreen()
        self.multiplayerScreen.backToMenuBtn.setTriggerFunction(self.backToMenu)
        self.multiplayerScreen.hostBtn.setTriggerFunction(self.toHostOption)
        self.multiplayerScreen.browseBtn.setTriggerFunction(self.toBrowseServer)
        self.multiplayerScreen.joinByIPBtn.setTriggerFunction(self.toJoinByIP)
        
        self.hostOptionScreen = HostOptionScreen.HostOptionScreen()
        self.hostOptionScreen.createBtn.setTriggerFunction(self.processCreateGameLobby)
        self.hostOptionScreen.backBtn.setTriggerFunction(self.backToMultiplayer)
        
        self.browseServerScreen = BrowseServerScreen.BrowseServerScreen()
        self.browseServerScreen.backBtn.setTriggerFunction(self.backToMultiplayer)
        self.browseServerScreen.refreshBtn.setTriggerFunction(self.findHost)
        self.browseServerScreen.joinSelectedBtn.setTriggerFunction(self.joinSelected)

        self.joinByIPScreen = JoinByIPScreen.JoinByIPScreen()
        self.joinByIPScreen.connectBtn.setTriggerFunction(self.connectByIp)
        self.joinByIPScreen.backBtn.setTriggerFunction(self.backToMultiplayer)
        
        self.browseButtonLocked = False
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
            dialog = Dialog.Dialog("Enter player name",pg.Vector2(500,200))
            params = [
            dialog,
            [
                self.hostOptionScreen.portInput,
                self.hostOptionScreen.playerNameInput
            ]
            ]
            dialog.confirmButton.setTriggerFunction(self.closeDialog,params)
            self.screenControl.addScreenByIndex(1,dialog)
            self.screenControl.currentScreens[0].disableUI()
            self.hostOptionScreen.portInput.is_clickable = False
            self.hostOptionScreen.playerNameInput.is_clickable = False
            return
        
        if(self.hostOptionScreen.portInput.textInput.value==""):
            dialog = Dialog.Dialog("Enter port number",pg.Vector2(500,200))
            params = [
            dialog,
            [
                self.hostOptionScreen.portInput,
                self.hostOptionScreen.playerNameInput
            ]
            ]
            dialog.confirmButton.setTriggerFunction(self.closeDialog,params)
            self.screenControl.addScreenByIndex(1,dialog)
            self.screenControl.currentScreens[0].disableUI()
            self.hostOptionScreen.portInput.is_clickable = False
            self.hostOptionScreen.playerNameInput.is_clickable = False
            return
        
        playerName = self.hostOptionScreen.playerNameInput.textInput.value
        portNumber = int(self.hostOptionScreen.portInput.textInput.value)
        
        self.isLogicRunning = False
        self.returnLogic = LobbyLogic.HostLobbyLogic
        self.returnLogicParams = [playerName,portNumber]
        
    def closeDialog(self,dialog,enableInputs):
        self.screenControl.removeScreen(dialog)
        self.screenControl.currentScreens[0].enableUI()
        
        for input in enableInputs:
            input.is_clickable=True
        pass
    
    
    def toJoinByIP(self)->None:
        self.screenControl.replaceScreenByIndex(0,self.joinByIPScreen)
        pass
    
    def connectByIp(self):
        ipAddress = self.joinByIPScreen.IPInput.textInput.value
        port = int(self.joinByIPScreen.portInput.textInput.value)
        playerName = self.joinByIPScreen.PlayerNameInput.textInput.value
        
        try:
            ip = ipaddress.IPv4Address(ipAddress)
            
        except ipaddress.AddressValueError:
            dialog = Dialog.Dialog("Enter valid IP Address",pg.Vector2(self.windowSurface.get_width()*0.6,300))
            self.screenControl.addScreenByIndex(1,dialog)
            self.screenControl.currentScreens[0].disableUI()
            self.joinByIPScreen.IPInput.textInput.is_clickable = False
            self.joinByIPScreen.PlayerNameInput.textInput.is_clickable = False
            self.joinByIPScreen.portInput.textInput.is_clickable = False
            
            params = [
            dialog,
            [
                self.joinByIPScreen.PlayerNameInput.textInput,
                self.joinByIPScreen.IPInput.textInput,
                self.joinByIPScreen.portInput.textInput
            ]
            ]
            dialog.confirmButton.setTriggerFunction(self.closeDialog,params)
            return
        
        if port == "":
            dialog = Dialog.Dialog("Enter port number",pg.Vector2(self.windowSurface.get_width()*0.6,300))
            self.screenControl.addScreenByIndex(1,dialog)
            self.screenControl.currentScreens[0].disableUI()
            self.joinByIPScreen.IPInput.textInput.is_clickable = False
            self.joinByIPScreen.PlayerNameInput.textInput.is_clickable = False
            self.joinByIPScreen.portInput.textInput.is_clickable = False
            
            params = [
            dialog,
            [
                self.joinByIPScreen.PlayerNameInput.textInput,
                self.joinByIPScreen.IPInput.textInput,
                self.joinByIPScreen.portInput.textInput
            ]
            ]
            dialog.confirmButton.setTriggerFunction(self.closeDialog,params)
            return

        if playerName == "":
            dialog = Dialog.Dialog("Enter player name",pg.Vector2(self.windowSurface.get_width()*0.6,300))
            self.screenControl.addScreenByIndex(1,dialog)
            self.screenControl.currentScreens[0].disableUI()
            self.joinByIPScreen.IPInput.textInput.is_clickable = False
            self.joinByIPScreen.PlayerNameInput.textInput.is_clickable = False
            self.joinByIPScreen.portInput.textInput.is_clickable = False
            
            params = [
            dialog,
            [
                self.joinByIPScreen.PlayerNameInput.textInput,
                self.joinByIPScreen.IPInput.textInput,
                self.joinByIPScreen.portInput.textInput
            ]
            ]
            dialog.confirmButton.setTriggerFunction(self.closeDialog,params)
            return
        
        self.connectToServer(ipAddress,port,playerName)
        
    def connectToServer(self,ip:str,port:int,playerName:str)->None:
        
        try:
            clientSocket = socket.create_connection((ip,port),5)
        except socket.timeout as e:
            dialog = Dialog.Dialog("Connection timed out",pg.Vector2(self.windowSurface.get_width()*0.6,300))
            self.screenControl.addScreenByIndex(1,dialog)
            self.screenControl.currentScreens[0].disableUI()
            self.joinByIPScreen.IPInput.textInput.is_clickable = False
            self.joinByIPScreen.PlayerNameInput.textInput.is_clickable = False
            self.joinByIPScreen.portInput.textInput.is_clickable = False
            
            params = [
            dialog,
            [
                self.joinByIPScreen.PlayerNameInput.textInput,
                self.joinByIPScreen.IPInput.textInput,
                self.joinByIPScreen.portInput.textInput
            ]
            ]
            dialog.confirmButton.setTriggerFunction(self.closeDialog,params)
            return
        except Exception as e:
            print(e)
            dialog = Dialog.Dialog("Connection error",pg.Vector2(self.windowSurface.get_width()*0.6,300))
            self.screenControl.addScreenByIndex(1,dialog)
            self.screenControl.currentScreens[0].disableUI()
            self.joinByIPScreen.IPInput.textInput.is_clickable = False
            self.joinByIPScreen.PlayerNameInput.textInput.is_clickable = False
            self.joinByIPScreen.portInput.textInput.is_clickable = False
            
            params = [
            dialog,
            [
                self.joinByIPScreen.PlayerNameInput.textInput,
                self.joinByIPScreen.IPInput.textInput,
                self.joinByIPScreen.portInput.textInput
            ]
            ]
            dialog.confirmButton.setTriggerFunction(self.closeDialog,params)
            return
        self.isLogicRunning = False
        self.returnLogic = LobbyLogic.ClientLobbyLogic
        self.returnLogicParams = [playerName,port,clientSocket]
        pass

    def receiveHost(self):
        startTime = pg.time.get_ticks()
        while pg.time.get_ticks() - startTime < 1000:
            try:
                message = pickle.loads(self.UDPSocket.recv(4096))
                ip = (message["ip_address"],message["port"])
                playerName = message["player_name"]
                data = {"ip_address":ip,"player_name":playerName}
                if not data in self.hostList:
                    self.hostList.append(data)
                pass
            except Exception as e:
                print("receivedHost Exception: ",e)
        self.browseServerScreen.serverListTable.updateTable(self.hostList)
        print("got:",self.hostList)
        self.browseButtonLocked = False
        pass
        

    def findHost(self):
        if not self.browseButtonLocked:
            self.browseButtonLocked = True
            self.hostList = []
            self.MCAST_GRP = ''
            self.MCAST_PORT = 22705
            
            MULTICAST_TTL = 2

            self.UDPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            self.UDPSocket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
            self.UDPSocket.sendto(pickle.dumps({"message":"host_find"}), (self.MCAST_GRP, self.MCAST_PORT))
            self.UDPSocket.settimeout(0.2)
            hostReceiveThread = threading.Thread(target=self.receiveHost)
            hostReceiveThread.start()
            
    def joinSelected(self):
        playerName = self.browseServerScreen.playerNameInput.textInput.value
        
        if playerName == "":
            dialog = Dialog.Dialog("Enter player name",pg.Vector2(self.windowSurface.get_width()*0.6,300))
            self.screenControl.addScreenByIndex(1,dialog)
            self.screenControl.currentScreens[0].disableUI()
            self.browseServerScreen.playerNameInput.textInput.is_clickable = False
            
            params = [
            dialog,
            [
                self.browseServerScreen.playerNameInput.textInput
            ]
            ]
            dialog.confirmButton.setTriggerFunction(self.closeDialog,params)
            return
        
        currentSelected = self.browseServerScreen.serverListTable.currentSelected
        if currentSelected != None:
            selectedHost = self.hostList[currentSelected]
            self.connectToServer(selectedHost["ip_address"][0],selectedHost["ip_address"][1],playerName)
        else:
            dialog = Dialog.Dialog("Select a server",pg.Vector2(self.windowSurface.get_width()*0.6,300))
            self.screenControl.addScreenByIndex(1,dialog)
            self.screenControl.currentScreens[0].disableUI()
            self.browseServerScreen.playerNameInput.textInput.is_clickable = False
            
            params = [
            dialog,
            [
                self.browseServerScreen.playerNameInput.textInput
            ]
            ]
            dialog.confirmButton.setTriggerFunction(self.closeDialog,params)
            return