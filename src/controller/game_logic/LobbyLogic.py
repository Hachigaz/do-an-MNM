import controller.game_logic.Logic as Logic
import controller.game_logic.GameMenu as GameMenu
import controller.game_logic.GameplayLogic as GameplayLogic

import view.screens.GameScreen as GameScreen
import view.screens.Lobby.LobbyScreen as LobbyScreen 
import socket as socket
import pickle
import threading
import struct

import pygame as pg
import view.screens.subscreens.dialog.dialog as Dialog


PLAYER_JOIN_MESSAGE = {
    "proc":"MyPythonGame",
    "stage":"lobby",
    "func":"join_lobby",
    "data":{
        "player_name":None,
        "ip_address":None
    }
}

PLAYER_JOIN_MESSAGE_RES = {
    "proc":"MyPythonGame",
    "stage":"lobby",
    "func":"join_lobby_res",
    "data":{
        "player_list":None
    }
}

CLIENT_SEND_MESSAGE = {
    "proc":"MyPythonGame",
    "stage":"lobby",
    "func":"send_message",
    "data":{
        "player":None,
        "message":None
    }
}

CLIENT_INCOMING_MESSAGE = {
    "proc":"MyPythonGame",
    "stage":"lobby",
    "func":"incoming_message",
    "data":{
        "player_name":None
    }
}

PLAYER_LEAVE_MESSAGE = {
    "proc":"MyPythonGame",
    "stage":"lobby",
    "func":"player_leave",
    "data":{
        "player_name":None,
        "ip_address":None
    }
}

START_GAME_MESSAGE = {
    "proc":"MyPythonGame",
    "stage":"lobby",
    "func":"start_game",
    "data":{
        
    }
}

MAX_TIMEOUT = 1

class LobbyPlayer:
    def __init__(self,name:str) -> None:
        self.name:str = name
        pass
    
class LobbyLogic(Logic.Logic):
    def __init__(self,playerName:str,portNumber:int) -> None:
        self.playerName:str = playerName
        self.portNumber:int =portNumber
    pass

class HostLobbyLogic(Logic.Logic):
    def __init__(self,playerName:str,portNumber:int) -> None:
        self.playerName:str = playerName
        self.portNumber:int =portNumber
    
    def start(self) -> None:
        MAX_PLAYERS=4
        mainScreen = LobbyScreen.LobbyScreen(True)
        super().start(mainScreen)
        
        mainScreen.returnToMenuBtn.setTriggerFunction(self.returnToMainMenu)
        self.mainScreen.chatBox.sendButton.setTriggerFunction(self.sendMessage)
        self.mainScreen.startGameBtn.setTriggerFunction(self.startGame)
        
        
        self.playerList:dict[str,str]={}
        self.processPlayerJoin("host",self.playerName)
        
        
        self.isGameStarting = False
        self.isHandlingClients = True
        self.clientSockets:dict[str,socket.socket]={}
        self.clientSocketThreads:dict[str,threading.thread]={}
        self.hostSocket:socket.socket = socket.create_server(("",self.portNumber),family=socket.AF_INET,dualstack_ipv6=False)
        self.hostSocket.listen(MAX_PLAYERS-1)
        self.hostSocket.settimeout(MAX_TIMEOUT)
        self.startClientHandler()
        
        print("started hosting on ",self.hostSocket)


        MCAST_GRP = '224.1.1.1'
        MCAST_PORT = 22705

        IS_ALL_GROUPS = True

        self.UDPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.UDPSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if IS_ALL_GROUPS:
            # on this port, receives ALL multicast groups
            self.UDPSocket.bind(('', MCAST_PORT))
        else:
            # on this port, listen ONLY to MCAST_GRP
            self.UDPSocket((MCAST_GRP, MCAST_PORT))
        mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

        self.UDPSocket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        self.hostFindThread = threading.Thread(target=self.receiveHostFindMessage)
        self.hostFindThread.start()

    def receiveHostFindMessage(self):
        self.isReceivingHostFind = True
        while self.isReceivingHostFind:
            data,ip = self.UDPSocket.recvfrom(4096)
            data = pickle.loads(data)
            if data["message"]=="host_find":
                response = {
                    "message":"host_find_res",
                    "ip_address":socket.gethostbyname(socket.gethostname()),
                    "port":self.portNumber,
                    "player_name":self.playerName
                }
                print("got address",ip)
                self.UDPSocket.sendto(pickle.dumps(response),ip)
        pass

    def returnToMainMenu(self)->None:
        self.isLogicRunning = False
        self.returnLogic=GameMenu.GameMenu
        pass

    def startClientHandler(self):
        self.isHandlingClients = True
        self.clientHandlerThread = threading.Thread(target=self.handleClients)
        self.clientHandlerThread.start()
        
    def handleClients(self):
        while self.isHandlingClients:
            try:
                clientSocket,address = self.hostSocket.accept()
                print("client connected: ",address)
                self.clientSockets[address]=clientSocket
                self.clientSocketThreads[address] = threading.Thread(target=self.handleConnection,args=[address,clientSocket])
                self.clientSocketThreads[address].start()
                pass
            except socket.timeout as exception:
                # print(exception)
                pass
    
    def handleConnection(self,address,clientSocket:socket.socket):
        isHandlingConnection = True
        print("handling connection:",address)
        while isHandlingConnection and not self.isGameStarting:
            data = pickle.loads(clientSocket.recv(4096))
            if data["proc"]!="MyPythonGame":
                isHandlingConnection=False
                print("Error handling")
                return
            if data["stage"] != "lobby":
                isHandlingConnection = False
                print("Error handling2")
                return
            func = data["func"]
            funcData = data["data"]
            if(func=="join_lobby"):
                playerName = funcData["player_name"]
                
                playerJoinMessage = PLAYER_JOIN_MESSAGE
                playerJoinMessage["data"]["player_name"]=playerName
                playerJoinMessage["data"]["address"]=address
                
                print("player list:")
                for ip,client in self.clientSockets.items():
                    print(ip,client)
                for ip,client in self.clientSockets.items():
                    if(client != clientSocket):
                        client.send(pickle.dumps(playerJoinMessage))
                
                self.processPlayerJoin(address,playerName) 
                
                playerJoinResMessage = PLAYER_JOIN_MESSAGE_RES
                playerJoinResMessage["data"]["player_list"]=self.playerList
                clientSocket.send(pickle.dumps(playerJoinResMessage))
                
            if(func == "send_message"):
                playerName = funcData["player"]
                message = funcData["message"]
                self.mainScreen.chatBox.addMessage(playerName,message)
                messageData = CLIENT_INCOMING_MESSAGE
                messageData["data"]["player"]=playerName
                messageData["data"]["message"]=message
                
                for ip,client in self.clientSockets.items():
                    client.send(pickle.dumps(messageData))
                pass
            
            if func=="player_leave" and not self.isGameStarting:
                playerName = funcData["player_name"]
                ip = funcData["ip_address"]
                print(playerName)
                print(ip)
                self.processPlayerLeave(ip,playerName)
                
                messageData = PLAYER_LEAVE_MESSAGE
                messageData["data"]["player_name"]=playerName
                messageData["data"]["ip_address"]=ip
                for ip,client in self.clientSockets.items():
                    client.send(pickle.dumps(messageData))
            pass 
        pass
    
    def processPlayerJoin(self,address,playerName:str):
        self.playerList[address] = playerName
        self.mainScreen.addPlayer(address,playerName)
        pass
    
    def processPlayerLeave(self,ip,playerName:str):
        print("PLAYER LEAVE: ",ip)
        self.playerList.pop(ip)
        self.mainScreen.removePlayer(ip,playerName)
        pass

    def sendMessage(self):
        message:str = self.mainScreen.chatBox.textInput.textInput.value
        
        messageData = CLIENT_INCOMING_MESSAGE
        messageData["data"]["player"]=self.playerName
        messageData["data"]["message"]=message
        
        for ip,client in self.clientSockets.items():
            client.send(pickle.dumps(messageData))
            # print("message sent to client ",client)
            pass
        
        self.mainScreen.chatBox.submitMessage(self.playerName)
        pass

    def startGame(self):
        if(len(self.playerList)>1):
            self.isGameStarting = True
            self.isLogicRunning = False
            self.returnLogic = GameplayLogic.HostLogic
            self.returnLogicParams = [
                "host",
                self.playerList,
                self.hostSocket,
                self.clientSockets
            ]
            
            
            startGameMessage = START_GAME_MESSAGE
            startGameMessage["data"]["player_count"]=len(self.playerList)
            playerIndex = 1 
            for ip,client in self.clientSockets.items():
                startGameMessage["data"]["player_index"]=playerIndex
                client.send(pickle.dumps(startGameMessage))
                playerIndex+=1
            pass
        else:
            dialog = Dialog.Dialog("Not enough player",pg.Vector2(500,200))
            params = [
                dialog,
                None
            ]
            dialog.confirmButton.setTriggerFunction(self.closeDialog,params)
            self.screenControl.addScreenByIndex(1,dialog)
            self.screenControl.currentScreens[0].disableUI()
        
    def closeDialog(self,dialog,enableInputs=None):
        self.screenControl.removeScreen(dialog)
        self.screenControl.currentScreens[0].enableUI()
        
        if(enableInputs!= None):
            for input in enableInputs:
                input.is_clickable=True
            pass

    def socketUpdate(self):
        # newSocket = self.hostSocket.accept()
        # message = pickle.loads(self.hostSocket.recv(4096))
        # print(message)
        pass
    
    def update(self) -> None:
        socketUpdateThread = threading.Thread(target=self.socketUpdate, args=())

        # Start the thread
        socketUpdateThread.start()
        super().update()
        socketUpdateThread.join()
    
    def end(self) -> tuple[Logic.Logic, list]:
        self.isReceivingHostFind = False
        self.isHandlingClients = False
        self.clientHandlerThread.join()
        if not self.isGameStarting:
            self.hostSocket.close()
        return super().end()

class ClientLobbyLogic(Logic.Logic):
    def __init__(self,playerName:str,portNumber:int,clientSocket:socket.socket) -> None:
        self.playerName:str = playerName
        self.portNumber:int =portNumber
        self.clientSocket:socket.socket=clientSocket
        self.isGameStarting = False
        
    def start(self) -> None:
        mainScreen = LobbyScreen.LobbyScreen()
        super().start(mainScreen)
        mainScreen.returnToMenuBtn.setTriggerFunction(self.returnToMainMenu)
        self.mainScreen.chatBox.sendButton.setTriggerFunction(self.sendMessage)
        
        
        self.clientSocket.settimeout(MAX_TIMEOUT)
        self.startConnectionHandler()
        
        playerJoinMessage = PLAYER_JOIN_MESSAGE
        playerJoinMessage["data"]["player_name"]=self.playerName
        
        self.clientSocket.send(pickle.dumps(playerJoinMessage))
    

    def startConnectionHandler(self):
        self.isHandlingConnections = True
        self.connectionHandlerThread = threading.Thread(target=self.handleConnections)
        self.connectionHandlerThread.start()
        
    def handleConnections(self):
        while self.isHandlingConnections and not self.isGameStarting:
            try:
                data = pickle.loads(self.clientSocket.recv(4096))
                if data["proc"]!="MyPythonGame":
                    raise Exception("error_handling1")
                if data["stage"] != "lobby":
                    raise Exception("error_handling2")
                func = data["func"]
                funcData = data["data"]
                if(func=="join_lobby_res"):
                    for ip,playerName in funcData["player_list"].items():
                        self.processPlayerJoinMessage(ip,playerName)
                    pass
                if(func=="incoming_message"):
                    playerName = funcData["player"]
                    message = funcData["message"]
                    self.mainScreen.chatBox.addMessage(playerName,message)
                    pass
                pass
                if(func=="join_lobby"):
                    playerName = funcData["player_name"]
                    ip = funcData["ip_address"]
                    self.processPlayerJoinMessage(ip,playerName)
                    
                if func=="player_leave":
                    playerName = funcData["player_name"]
                    ip = funcData["ip_address"]
                    self.processPlayerLeaveMessage(ip,playerName)
                if func=="start_game":
                    self.isGameStarting=True
                    self.playerCount = funcData["player_count"]
                    self.playerIndex = funcData["player_index"]
                    self.startGame()
                pass 
            except socket.timeout as e:
                print(e)
                pass
            except Exception as e:
                print("Exception: ",e)
                self.returnToMainMenu()
    
    def startGame(self):
        self.isLogicRunning= False
        self.returnLogic = GameplayLogic.ClientLogic
        self.returnLogicParams = [
            self.clientSocket.getsockname(),
            self.clientSocket,
            self.playerCount,
            self.playerIndex
        ]
        pass 
    
    def sendMessage(self):
        sendMessage = CLIENT_SEND_MESSAGE
        sendMessage["data"]["player"]=self.playerName
        sendMessage["data"]["message"]=self.mainScreen.chatBox.textInput.textInput.value
        self.mainScreen.chatBox.clearInputValue()
        self.clientSocket.send(pickle.dumps(sendMessage))
        pass
        
    def processPlayerJoinMessage(self,ip,playerName):
        self.mainScreen.addPlayer(ip,playerName)
        pass
    
    def processPlayerLeaveMessage(self,ip,playerName):
        self.mainScreen.removePlayer(ip,playerName)
        pass
        
    def playerLeaveLobby(self):
        leaveMessage = PLAYER_LEAVE_MESSAGE
        leaveMessage["data"]["player_name"]=self.playerName
        leaveMessage["data"]["ip_address"]=self.clientSocket.getsockname()
        
        self.clientSocket.send(pickle.dumps(leaveMessage))
        
    def end(self) -> tuple[Logic.Logic, list]:
        self.playerLeaveLobby()
        self.connectionHandlerThread.join()
        if not self.isGameStarting:
            self.clientSocket.close()
        return super().end()
        
    def returnToMainMenu(self)->None:
        self.isHandlingConnections = False
        self.isLogicRunning = False
        self.returnLogic=GameMenu.GameMenu
        pass
    pass