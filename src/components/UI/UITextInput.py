import pygame as pg

import components.UI.UIObject as UIObject

import components.borrowed.pygame_textinput as TextInput

import threading

class UITextInput (UIObject.UIObject):
    def __init__(self,rect:pg.rect.Rect, initText:str, validatorFunc, fontSize:int,is_clickable:bool = False) -> None:
        super().__init__()
        if validatorFunc != None:
            inputManager = TextInput.TextInputManager(initText,validator=validatorFunc)
        else:
            inputManager = TextInput.TextInputManager(initText)
            
        inputFont = pg.font.SysFont("Consolas",fontSize)
        
        self.textInput = TextInput.TextInputVisualizer(inputManager,inputFont,font_color=pg.Color(255,255,255))
        self.textInput.cursor_color=pg.color.Color(255,255,255)
        self.textInput.cursor_width=3
        
        #inputSprite = UIObject.uiSpriteElement(self.textInput.surface,pg.rect.Rect(pg.Vector2(rect.topleft)-pg.Vector2(self.textInput.surface.get_size()),pg.Vector2(self.textInput.surface.get_size())))
        inputSprite = UIObject.uiSpriteElement(self.textInput.surface,pg.rect.Rect(pg.Vector2(rect.topleft)+pg.Vector2(3,3),pg.Vector2(self.textInput.surface.get_size())))
        
        self.rect=rect
        self.rect.height = fontSize*1.5
        self.textInputOverlay = pg.surface.Surface(self.rect.size,pg.SRCALPHA,32)
        self.textInputOverlay.fill(pg.color.Color(255,255,255,20))
            
        self.uiSurfaces.insert(0,inputSprite)
        
        self.is_clickable = is_clickable
        
        self.isInputEnabled = False
    
    def update(self, drawSurface: pg.Surface) -> None:
        inputUpdateThread = threading.Thread(target=self.updateInput)
        inputUpdateThread.start()
        drawSurface.blit(self.textInputOverlay,self.rect.topleft)
        if(self.is_clickable):
            if pg.mouse.get_pressed()[0]==1:
                if(self.rect.collidepoint(pg.mouse.get_pos()[0],pg.mouse.get_pos()[1])):
                    self.enableInput()
                else:
                    self.disableInput()
        
        self.uiSurfaces[0].surface = self.textInput.surface
    
        super().update(drawSurface)
        inputUpdateThread.join()
        
    def updateInput(self):
        if(self.isInputEnabled == True):
            self.textInput.update(pg.event.get())
        
        
    def disableInput(self) -> None:
        self.isInputEnabled = False
        self.textInput.cursor_width=0
        
    def enableInput(self) -> None:
        self.isInputEnabled = True
        self.textInput.cursor_width=3
        
    def toggleInput(self)->None:
        self.isInputEnabled = not self.isInputEnabled
        self.textInput.cursor_width = 3 - self.textInput.cursor_width