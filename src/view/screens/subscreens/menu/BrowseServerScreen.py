import pygame as pg

import components.game_components.Textures as Textures;
import components.UI.UIText as UIText
import components.UI.UIButton as UIButton

import view.screens.GameScreen as GameScreen



class BrowseServerScreen(GameScreen.GameScreen):
    def __init__(self) -> None:
        super().__init__()
        
        buttonSurf = Textures.getLoadedSurfaces("blue_button00")
        
        screenCenterPos:pg.Vector2=  pg.Vector2(self.screenSurf.get_rect().center)
        
        title = UIText.UIText(pg.font.Font("resources/ui/Font/kenvector_future.ttf",40),"Browse",pg.Vector2(screenCenterPos.x,150))
        self.uiGroup.add(title)
        
        menuBtnsOffsetY=200
        self.refreshBtn = UIButton.UIButton(buttonSurf,pg.Rect(pg.Vector2(pg.Vector2(screenCenterPos.x,menuBtnsOffsetY+200)),pg.Vector2(350,80)),"Refresh",25)
        self.uiGroup.add(self.refreshBtn)
        self.joinSelectedBtn = UIButton.UIButton(buttonSurf,pg.Rect(pg.Vector2(pg.Vector2(screenCenterPos.x,menuBtnsOffsetY+300)),pg.Vector2(350,80)),"Join",25)
        self.uiGroup.add(self.joinSelectedBtn)
        self.backBtn = UIButton.UIButton(buttonSurf,pg.Rect(pg.Vector2(pg.Vector2(screenCenterPos.x,menuBtnsOffsetY+400)),pg.Vector2(350,80)),"Back",25)
        self.uiGroup.add(self.backBtn)