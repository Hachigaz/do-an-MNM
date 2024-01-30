from enum import Enum

import src.controller.GameScreen as GameScreen
from src.controller.screens import MenuScreen

import src.model.GameObject.Textures as Textures

import pygame as pg

class GameState(Enum):
    MENU = 1
    SETTING = 2
    INGAME = 3
    LOBBY = 4


class Game:
    gameState:GameState
    gameScreen:GameScreen
    screen:pg.Surface
    
    def __init__(self) -> None:
        self.loadResources()
        
        self.screen = pg.display.set_mode((1280, 720))
        self.clock = pg.time.Clock()
        
        
        self.gameState = GameState.MENU
        self.gameScreen = MenuScreen.MenuScreen(self.screen)
        
        self.renderLoop()
        pass

    def loadResources(self)->None:
        #load UIs
        Textures.loadTextures()
        pass
    
    def renderLoop(self)->None:
        self.running = True
        while self.running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill(pg.Color(0,0,0))
            
            # RENDER YOUR GAME HERE
            self.gameScreen.update()
            # flip() the display to put your work on screen
            pg.display.flip()

            self.clock.tick(60)  # limits FPS to 60

        self.endGame()
    
    def endGame(self)->None:
        pg.quit()