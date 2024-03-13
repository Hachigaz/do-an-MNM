import components.game_components.Textures as Textures

import pygame as pg

import controller.game_logic.Logic as Logic
import controller.game_logic.GameMenu as GameMenu
import view.screens.GameScreen as GameScreen

class Game:
    running:bool = True
    def __init__(self) -> None:
        self.run()
        
        
    def run(self)->None:
        self.setup()
        
        GameMenu.GameMenu()
        
        self.endGame()
    
    def setup(self)->None:
        screen:pg.Surface = pg.display.set_mode((1920, 1080),pg.NOFRAME)
        Logic.Logic.__setup__(screen)
        GameScreen.GameScreen.__setup__(screen)
        #load ui textures
        Textures.loadTextures()
    
    def endGame(self)->None:
        pg.quit()