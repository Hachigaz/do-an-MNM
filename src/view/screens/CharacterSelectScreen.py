import pygame as pg
import view.screens.GameScreen as GameScreen

import components.UI.UIText as UIText 
import components.UI.UIButton as UIButton
import components.UI.UISelectBox as UISelectBox
import components.UI.UIObject as UIObject

import components.game_components.Textures as Textures
class CharacterSelectScreen(GameScreen.GameScreen):
    def __init__(self) -> None:
        super().__init__()
        
        buttonSurf = next(item for item in Textures.loadedSurfaces if item["name"]=="blue_button00")["surface"]
        
        screenRect=self.screenSurf.get_rect()
        screenCenterPos:pg.Vector2=  pg.Vector2(screenRect.center)
        
        
        backgroundSurf = pg.transform.scale(pg.image.load("resources/ui/PNG/main-background.jpg"),self.screenSurf.get_rect().size)
        backgroundRect = pg.Rect(0,0,backgroundSurf.get_rect().width,backgroundSurf.get_rect().height)
        gameBackground = UIObject.uiSpriteElement(backgroundSurf,backgroundRect)
        backgroundObj = UIObject.UIObject()
        backgroundObj.uiSurfaces.insert(0,gameBackground)
        
        backgroundDim = pg.Surface(backgroundRect.size,pg.SRCALPHA).convert_alpha()
        backgroundDim.fill((120,120,120,100))
        backgroundDimObj = UIObject.uiSpriteElement(backgroundDim,backgroundRect)
        backgroundObj.uiSurfaces.insert(1,backgroundDimObj)
        
        self.uiGroup.add(backgroundObj)
        
        self.characterSelectBox = UISelectBox.UISelectBox(pg.Rect(pg.Vector2(screenRect.center),pg.Vector2(screenRect.width-300,400)),pg.Vector2(250,600))
        self.characterSelectBox.addItem(1,"Character 1",None)
        self.characterSelectBox.addItem(2,"Character 2",None)
        self.characterSelectBox.addItem(3,"Character 3",None)
        self.characterSelectBox.addItem(4,"Character 4",None)
        self.characterSelectBox.addItem(5,"Character 5",None)
        self.uiGroup.add(self.characterSelectBox)
        
        title = UIText.UIText(pg.font.Font("resources/ui/Font/kenvector_future.ttf",40),"Select Your Character",pg.Vector2(screenCenterPos.x,150))
        self.uiGroup.add(title)
        
        
        
        
        self.backToMenuButton = UIButton.UIButton(buttonSurf,pg.Rect(pg.Vector2(pg.Vector2(screenCenterPos.x,screenRect.bottom-100)),pg.Vector2(350,80)),"Back",25)
        self.uiGroup.add(self.backToMenuButton)
