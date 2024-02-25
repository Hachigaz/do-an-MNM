import pygame as pg
import src.controller.GameScreen as GameScreen
import src.view.UI.UIObject as UIObject
import src.view.UI.Components.UIButton as UIButton
import src.model.GameObject.Textures as Textures
class CharacterSelect(GameScreen.SubScreen):
    def __init__(self, screenSurf: pg.Surface, parentScreen: GameScreen.GameScreen) -> None:
        super().__init__(screenSurf, parentScreen)
        
        buttonSurf = next(item for item in Textures.loadedSurfaces if item["name"]=="blue_button00")["surface"]
        
        screenCenterPos:pg.Vector2=  pg.Vector2(self.screenSurf.get_rect().center)
        screenSize:pg.Vector2=  pg.Vector2(self.screenSurf.get_rect().width,self.screenSurf.get_rect().height)
        
        characterRowRange = pg.Vector2(0.1*screenSize.x,0.1*screenSize.x)
        
        titleSurf =pg.font.Font("resources/ui/Font/kenvector_future.ttf",40).render("Select Your Character",True,pg.Color(255,255,255))
        gameTitle = UIObject.UIObject(titleSurf,pg.Rect(pg.Vector2(screenCenterPos.x,150),pg.Vector2(titleSurf.get_size())))
        self.uiGroup.add(gameTitle)
        
        menuBtn = UIButton.UIButton(buttonSurf,pg.Rect(pg.Vector2(pg.Vector2(300,400)),pg.Vector2(350,80)),"Back",25)
        self.uiGroup.add(menuBtn)
        