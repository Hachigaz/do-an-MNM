import pygame as pg

import components.UI.UIObject as UIObject

import components.borrowed.pygame_textinput as TextInput

class UITextInput (UIObject.UIObject):
    def __init__(self,rect:pg.rect.Rect, initText:str, validatorFunc, fontSize:int) -> None:
        super().__init__()
        inputManager = TextInput.TextInputManager(initText,validator=validatorFunc)
        inputFont = pg.font.SysFont("Consolas",fontSize)
        
        self.textInput = TextInput.TextInputVisualizer(inputManager,inputFont,font_color=pg.Color(255,255,255))
        self.textInput.cursor_color=pg.color.Color(255,255,255)
        self.textInput.cursor_width=3
        
        #inputSprite = UIObject.uiSpriteElement(self.textInput.surface,pg.rect.Rect(pg.Vector2(rect.topleft)-pg.Vector2(self.textInput.surface.get_size()),pg.Vector2(self.textInput.surface.get_size())))
        inputSprite = UIObject.uiSpriteElement(self.textInput.surface,pg.rect.Rect(pg.Vector2(rect.topleft),pg.Vector2(self.textInput.surface.get_size())))
        
        self.uiSurfaces.insert(0,inputSprite)
        
        self.isInputEnabled = True
    
    def update(self, drawSurface: pg.Surface) -> None:
        
        self.uiSurfaces[0].surface = self.textInput.surface
        if(self.isInputEnabled == True):
            self.textInput.update(pg.event.get())
            
        super().update(drawSurface)
        
    def disableInput(self) -> None:
        self.isInputEnabled = False
        self.textInput.cursor_width=0
        
    def enableInput(self) -> None:
        self.isInputEnabled = True
        self.textInput.cursor_width=3        