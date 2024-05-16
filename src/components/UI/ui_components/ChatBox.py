import pygame as pg

import components.UI.UIButton as UIButton
import components.UI.UITextInput as UITextInput
import components.UI.UIText as UIText
import components.UI.UIObject as UIObject

import datetime as datetime

import components.game_components.Textures as Textures

class Message:
    def __init__(self,message:str,userSent:str) -> None:
        self.message = message
        self.userSent = userSent
        self.timeSent = datetime.datetime.now().strftime("%H:%M:%S")

class MessageList:
    def __init__(self) -> None:
        self.messages = []
        
    def addMessage(self,message:Message)->None:
        self.messages.append(message)

class ChatBox:
    def __init__(self, rect:pg.rect.Rect,messageList:MessageList) -> None:
        self.textInput:UITextInput.UITextInput = UITextInput.UITextInput(pg.rect.Rect(pg.Vector2(rect.left,rect.top+rect.height*0.8+20),pg.Vector2(rect.width*0.8,rect.height*0.2)),"",lambda x:len(x)<=35,20)
        
        inputCoverSurf = pg.surface.Surface(pg.Vector2(50,50),pg.SRCALPHA, 32)
        inputCoverSurf.fill(pg.Color(120,120,120,200))
        self.textInputCover:UIObject.UIObject = UIObject.UISprite(inputCoverSurf,pg.rect.Rect(pg.Vector2(rect.left,rect.top+rect.height*0.8),pg.Vector2(rect.width*0.8,rect.height*0.2)),True)
        
        
        self.sendButton:UIButton.UIButton = UIButton.UIButton(Textures.getLoadedSurfaces("blue_button00"),pg.rect.Rect(pg.Vector2(rect.left+0.8*rect.width,rect.top+0.8*rect.height),pg.Vector2(rect.width*0.2,rect.height*0.2)),"Send",15,True)
        
        self.messageList:MessageList = messageList
        messageCoverSurf = pg.surface.Surface(pg.Vector2(50,50),pg.SRCALPHA, 32)
        messageCoverSurf.fill(pg.Color(100,100,100,70))
        self.messageListCover = UIObject.UISprite(messageCoverSurf,pg.rect.Rect(pg.Vector2(rect.topleft),pg.Vector2(rect.width,rect.height)),True)
        
        self.numberOfVisibleMessages = 6
        self.messageDisplayTexts = []
        #messageFont = pg.font.Font("resources/ui/Font/kenvector_future.ttf",18)
        messageFont = pg.font.SysFont("Consolas",18)
        for i in range(self.numberOfVisibleMessages):
            self.messageDisplayTexts.append(UIText.UIText(messageFont,"",pg.Vector2(rect.left,rect.top+0.12*rect.height*i),True))
        pass
    
    def submitMessage(self,playerName)->None:
        messageText = self.textInput.textInput.value
        if messageText!="":
            message = Message(messageText,playerName)
            self.messageList.addMessage(message)
            
            self.clearInputValue()
            self.updateMessages()
            
    def clearInputValue(self):
        self.signalClear = True
        self.textInput.textInput.value = ""
        
    def addMessage(self,playerName,message):
        self.messageList.addMessage(Message(message,playerName))
        self.updateMessages()

    def updateMessages(self)->None:
        lastMesssages = self.messageList.messages[-self.numberOfVisibleMessages:]
        for index,item in enumerate(lastMesssages):
            self.messageDisplayTexts[index].updateText(item.timeSent +" "+ item.userSent+": "+item.message)
        
    def update(self,drawSurface:pg.surface.Surface)->None:
        self.messageListCover.update(drawSurface)
        self.textInputCover.update(drawSurface)
        
        self.sendButton.update(drawSurface)
        for item in self.messageDisplayTexts:
            item.update(drawSurface)
            
        
        if(self.textInputCover.uiSurfaces[0].rect.collidepoint(pg.Vector2(pg.mouse.get_pos()))):
            if(pg.mouse.get_pressed()[0]==1):
                self.textInput.enableInput()
        else:
            if(pg.mouse.get_pressed()[0]==1):
                self.textInput.disableInput()