import components.game_components.Textures as Textures

import pygame as pg

import controller.game_logic.Logic as Logic
import controller.game_logic.GameMenu as GameMenu
import controller.game_logic.GameplayLogic as GameplayLogic
import view.screens.GameScreen as GameScreen

class Game:
    running:bool = True
    def __init__(self) -> None:
        self.run()
        
        
    def run(self)->None:
        self.setup()
        
        self.currentLogic = GameMenu.GameMenu
        self.logicParams = None
        while(self.currentLogic!=None):
            if self.logicParams != None:
                logic = self.currentLogic(*self.logicParams)
            else:
                logic = self.currentLogic()
            logic.start()
            logic.loop()
            endLogic = logic.end()
            self.currentLogic = endLogic[0]
            self.logicParams=endLogic[1]
            pass
                
        self.endGame()
    
    def setup(self)->None:
        # screen:pg.Surface = pg.display.set_mode((1366, 768),pg.NOFRAME)
        screen:pg.Surface = pg.display.set_mode((1366, 768))
        pg.display.set_icon(pg.image.load("resources/tank_sprites/tank/tank_idle.webp"))
        # screen:pg.Surface = pg.display.set_mode((1366, 768),pg.FULLSCREEN)
        # screen:pg.Surface = pg.display.set_mode((800, 600),pg.NOFRAME)
        # screen:pg.Surface = pg.display.set_mode((800, 600),pg.FULLSCREEN)
        Logic.Logic.__setup__(screen)
        GameScreen.GameScreen.__setup__(screen)
        #load ui textures
        Textures.loadTextures()
    
    def endGame(self)->None:
        pg.quit()