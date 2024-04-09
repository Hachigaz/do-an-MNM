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
        
        self.startMenuLogic()
                
        self.endGame()
    
    def setup(self)->None:
        screen:pg.Surface = pg.display.set_mode((1366, 768),pg.NOFRAME)
        Logic.Logic.__setup__(screen)
        GameScreen.GameScreen.__setup__(screen)
        #load ui textures
        Textures.loadTextures()
    
    def startMenuLogic(self):
        logic = GameMenu.GameMenu()
        logic.start()
        logic.loop()
        returnLogic = logic.end()
        
        if not returnLogic == None:
            self.startGameplayLogic()
    
    def startGameplayLogic(self):
        logic = GameplayLogic.GameplayLogic()
        logic.start()
        logic.loop()
        returnLogic = logic.end()
        
        if not returnLogic == None:
            self.startMenuLogic()
    
    def endGame(self)->None:
        pg.quit()