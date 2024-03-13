import pygame as pg

import view.screens.GameScreen as GameScreen

class Logic:
    isGameRunning:bool = True
    windowSurface:pg.Surface
    def __setup__(windowSurface):
        Logic.windowSurface = windowSurface
        
    def __init__(self, mainScreen:GameScreen.GameScreen) -> None:
        self.isLogicRunning = True
        self.mainScreen = mainScreen
        self.currentScreen = mainScreen
        pass
    
    def loop(self)->None:
        self.clock = pg.time.Clock()
        while self.isGameRunning and self.isLogicRunning:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.isGameRunning = False

            self.windowSurface.fill(pg.Color(0,0,0))
            
            self.update()
            
            pg.display.flip()

            self.clock.tick(60)
            
            
    def start(self) -> None:
        pass
    
    def setup(self) -> None:
        pass
    
    def update(self) -> None:
        self.currentScreen.update()
        pass
    
    def run(self)->None:
        self.start()
        self.loop()
        self.end()
        pass
    
    #end duoc goi khi logic ket thuc khong chay nua isLogicRunning = false
    def end(self) -> None:
        pass
    
    def doQuitGame(self):
        self.isGameRunning = False