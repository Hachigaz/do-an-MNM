from __future__ import annotations

import pygame as pg

class HostRowElement:
    def __init__(self,pos,hostIpSurf,hostNameSurf,rect) -> None:
        self.pos:pg.Vector2 = pos
        self.hostIpSurf = hostIpSurf
        self.hostNameSurf = hostNameSurf
        self.rect = rect
        pass
    
    def draw(self, screenSurf:pg.Surface,table:ServerListTable):
        drawPos = self.pos
        screenSurf.blit(self.hostIpSurf,drawPos)
        screenSurf.blit(self.hostNameSurf,drawPos+pg.Vector2(table.tableSize.x*0.6,0))

class ServerListTable:
    def __init__(self,screenSurf:pg.Surface) -> None:
        self.tableSize = pg.Vector2(screenSurf.get_width()*0.6,screenSurf.get_height()*0.6)
        self.tablePos = pg.Vector2(screenSurf.get_width()*0.1,screenSurf.get_height()/2)-pg.Vector2(0,self.tableSize.y/2)
        
        self.tableOverlay = pg.surface.Surface(self.tableSize,pg.SRCALPHA,32)
        self.tableOverlay.fill(pg.color.Color(255,255,255,50))
        
        self.selectedOverlay  = pg.surface.Surface(pg.Vector2(self.tableSize.x,1.4*20),pg.SRCALPHA,32)
        self.selectedOverlay.fill(pg.color.Color(255,255,255,50))
        
        self.renderFont = pg.font.SysFont("Arial",20)
        self.rowAddressLabel = self.renderFont.render("Address",True,pg.color.Color(255,255,255))
        self.rowPlayerNameLabel = self.renderFont.render("Host Name",True,pg.color.Color(255,255,255))
        
        self.rowOffsetX = 10
        self.rowOffsetY = 30
        self.rowYGap = 30
        self.playerNameOffsetX = 0.3*screenSurf.get_width()
        
        self.currentSelected = None
        self.tableRowElements = []
        pass
    
    def updateTable(self,hostList):
        self.hostList = hostList
        self.tableRowElements = []
        for index,row in enumerate(self.hostList,start=0):
            hostAddress = self.renderFont.render(row["ip_address"][0]+":"+str(row["ip_address"][1]),True,pg.color.Color(255,255,255))
            hostName = self.renderFont.render(row["player_name"],True,pg.color.Color(255,255,255))
            drawPos = pg.Vector2(self.tablePos.x+self.rowOffsetX,self.tablePos.y+index*self.rowYGap+self.rowOffsetY)
            self.tableRowElements.append(HostRowElement(drawPos,hostAddress,hostName,pg.rect.Rect(drawPos,pg.Vector2(self.tableSize.x,1.4*20))))
        
    def update(self,screenSurf:pg.Surface):
        screenSurf.blit(self.tableOverlay,self.tablePos)
        
        drawPos = pg.Vector2(self.tablePos.x+self.rowOffsetX,self.tablePos.y)
        screenSurf.blit(self.rowAddressLabel,drawPos)
        screenSurf.blit(self.rowPlayerNameLabel,drawPos+pg.Vector2(self.tableSize.x*0.6,0))


        mousePos = pg.mouse.get_pos()
        
        for idx,row in enumerate(self.tableRowElements,start=0):
            row.draw(screenSurf,self)
            if pg.mouse.get_pressed()[0]:
                if row.rect.collidepoint(mousePos):
                    self.currentSelected = idx
            if self.currentSelected == idx:
                screenSurf.blit(self.selectedOverlay,pg.Vector2(row.pos.x-self.rowOffsetX,row.pos.y))
            

        
    pass