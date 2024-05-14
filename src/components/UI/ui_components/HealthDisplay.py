import pygame as pg

class PlayerHealthDisplay:
    def __init__(self,screenSize:pg.Vector2,healthCount:int = 5) -> None:
        self.healthBarOverlay:pg.surface.Surface = pg.Surface((185,60),pg.SRCALPHA, 32)
        self.healthBarOverlay.fill(pg.color.Color(0, 251, 109,50))
        
        self.position = pg.Vector2(0,0)
        
        self.healthCount = healthCount
        self.heartIcon = pg.transform.scale(pg.image.load("resources/img/heart.png"),(40,40))
        
        self.heartPosition = self.position + pg.Vector2(10,10)
        pass
    
    def update(self,healthCount):
        self.healthCount=healthCount
    
    def render(self,renderSurface:pg.surface.Surface):
        renderSurface.blit(self.healthBarOverlay,self.position)
        pos = self.heartPosition.copy()
        
        for i in range(self.healthCount):
            renderSurface.blit(self.heartIcon,pos)
            pos.x += 30