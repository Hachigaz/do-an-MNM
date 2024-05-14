from __future__ import annotations
import pygame as pg

class MapIcon:
    def __init__(self,surf:pg.Surface,map:MapDisplay,localPos:pg.Vector2=pg.Vector2(0,0)) -> None:
        self.surf:pg.Surface = surf
        self.localPos:pg.Vector2=localPos
        self.map = map
        pass
    
    def updatePosition(self,worldPos:pg.Vector2):
        xBound = self.map.mapRange.topleft[0]+self.map.mapRange.width
        yBound = self.map.mapRange.topleft[1]+self.map.mapRange.height
        if(worldPos.x>xBound):
            worldPos.x = self.map.mapRange.width
        elif worldPos.x<self.map.mapRange.topleft[0]:
            worldPos.x = 0
        if(worldPos.y>yBound):
            worldPos.y = self.map.mapRange.height
        elif worldPos.y<self.map.mapRange.topleft[1]:
            worldPos.y = 0
            
        self.localPos = pg.Vector2(worldPos.x/self.map.mapRange.width*self.map.mapSize.x,worldPos.y/self.map.mapRange.height*self.map.mapSize.y)
    
    def render(self,screenSurf:pg.Surface):
        screenSurf.blit(self.surf,self.localPos+self.map.mapPos)
        pass
    pass
class MapDisplay:
    def __init__(self,playerCount:int,screenSize:pg.Vector2,mapRange:pg.rect.Rect) -> None:
        self.playerCount:int = playerCount
        self.mapSize:pg.Vector2 = pg.Vector2(250,250*mapRange.height/mapRange.width)
        self.mapPos:pg.Vector2 = screenSize-self.mapSize
        self.mapRange:pg.rect.Rect = mapRange
        
        self.mapOverlay = pg.surface.Surface(self.mapSize,pg.SRCALPHA, 32)
        self.mapOverlay.fill(pg.color.Color(22, 86, 255,50))
        
        self.playerIcons:list[MapIcon] = []
        for i in range(self.playerCount):
            self.playerIcons.append(MapIcon(pg.transform.scale(pg.image.load("resources/img/ship_icon.png"),(30,30)),self))
        pass
    
    def update(self,playerPos:list[tuple[float,float]]):
        self.updatePlayerPosition(playerPos)
        pass
    
    def updatePlayerPosition(self,playerPos:list[pg.Vector2]):
        
        for i in range(len(self.playerIcons)):
            self.playerIcons[i].updatePosition(playerPos[i])
    
    def render(self,screenSurf:pg.Surface):
        screenSurf.blit(self.mapOverlay,self.mapPos)
        for icon in self.playerIcons:
            icon.render(screenSurf)
        pass