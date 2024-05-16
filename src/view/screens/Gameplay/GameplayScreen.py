import view.screens.GameScreen as GameScreen

import components.UI.ui_components.HealthDisplay as HealthDisplay
import components.UI.ui_components.MapDisplay as MapDisplay

import pygame as pg



class GameplayScreen(GameScreen.GameScreen):
    def __init__(self,playerCount,currentPlayerIndex) -> None:
        super().__init__()
    
        self.playerHealthDisplay = HealthDisplay.PlayerHealthDisplay(pg.Vector2(self.screenSurf.get_size()),5)
        self.mapDisplay = MapDisplay.MapDisplay(playerCount,pg.Vector2(self.screenSurf.get_size()),pg.rect.Rect(0,0,2000,1500),currentPlayerIndex)


    def update(self) -> None:
        self.mapDisplay.render(self.screenSurf)
        self.playerHealthDisplay.render(self.screenSurf)
        return super().update()
    pass