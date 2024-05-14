from __future__ import annotations


import pygame as pg

import view.screens.GameScreen as GameScreen


class Logic:
    isGameRunning:bool = True
    windowSurface:pg.Surface
    def __setup__(windowSurface):
        Logic.windowSurface = windowSurface
        
    def __init__(self) -> None:
        pass
    
    def loop(self)->None:
        self.clock = pg.time.Clock()
        while self.isGameRunning and self.isLogicRunning:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.isGameRunning = False

            self.windowSurface.fill(pg.Color(20,20,20))
            
            self.update()
            
            pg.display.flip()

            self.clock.tick(60)
            
            
    def start(self,mainScreen:GameScreen.GameScreen) -> None:
        self.isLogicRunning = True
        self.mainScreen = mainScreen
        self.screenControl = ScreenRenderControl()
        self.screenControl.addScreenByIndex(0,self.mainScreen)
        self.returnLogic = None
        pass
    
    def setup(self) -> None:
        pass
    
    def update(self) -> None:
        self.screenControl.update()
        pass
    
    def end(self) -> Logic:
        return self.returnLogic
    
    def doQuitGame(self):
        self.isGameRunning = False
        
class ScreenRenderControl:
    def __init__(self) -> None:
        self.currentScreens=[]
        pass
    
    def addScreen(self,screen:GameScreen)->None:
        if not screen in self.currentScreens:
            self.currentScreens.append(screen)
            
    def addScreenByIndex(self,index,screen)->None:
        if not screen in self.currentScreens:
            self.currentScreens.insert(index,screen)
            
    def removeScreen(self,screen:GameScreen)->None:
        if screen in self.currentScreens:
            self.currentScreens.remove(screen)
            
    def replaceScreen(self,oldScreen:GameScreen,newScreen:GameScreen):
        if not newScreen in self.currentScreens:
            if oldScreen in self.currentScreens:
                self.currentScreens.remove(oldScreen)
                self.currentScreens.append(newScreen)
            
    def replaceScreenByIndex(self,index:int,screen:GameScreen):
        if not screen in self.currentScreens:
            if index >= 0 and index <len(self.currentScreens):
                self.currentScreens.pop(index)
                self.currentScreens.insert(index,screen)
        
    def update(self)->None:
        for screen in self.currentScreens:
            screen.update()