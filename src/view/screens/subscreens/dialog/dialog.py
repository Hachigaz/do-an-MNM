import view.screens.GameScreen as GameScreen
import components.UI.UIText as UIText
import components.UI.UIButton as UIButton

import components.game_components.Textures as Textures

import pygame as pg

class Dialog(GameScreen.GameScreen):
    def __init__(self,message:str,dialogSize:pg.Vector2, buttonText="OK") -> None:
        super().__init__()
        
        screenCenterPos:pg.Vector2=  pg.Vector2(self.screenSurf.get_rect().center)
        self.dialogPos:pg.Vector2= screenCenterPos
        self.dialogSize:pg.Vector2 = dialogSize
        buttonSurf = Textures.getLoadedSurfaces("blue_button00")
        
        self.dialogOverlay = pg.surface.Surface(dialogSize,pg.SRCALPHA,32)
        self.dialogOverlay.fill(pg.Color(80,80,200,240))
        
        self.messageText = UIText.UIText(pg.font.Font("resources/ui/Font/kenvector_future.ttf",20),message,pg.Vector2(self.dialogPos,-100),False) 
        self.uiGroup.add(self.messageText)
        self.confirmButton = UIButton.UIButton(buttonSurf,pg.Rect(pg.Vector2(pg.Vector2(self.dialogPos+pg.Vector2(0,100))),pg.Vector2(200,60)),buttonText,20)
        self.uiGroup.add(self.confirmButton)
        
    def update(self) -> None:
        self.screenSurf.blit(self.dialogOverlay,self.dialogPos-self.dialogSize/2)
        return super().update()
    
    pass