from __future__ import annotations

import quads as quads
import pymunk as pm
import pygame as pg

class NodeData:    
    def __init__(self,pointList:list[tuple[float,float]]) -> None:
        self.pointList:list[tuple[float,float]] = pointList
        
        pass


    def draw(self,screenSurf)->None:

        pass

class TerrainNode:
    MAX_LEVEL = 8
    
    def __init__(self,pTopLeft,pTopRight,pBottomLeft,pBottomRight,level:int) -> None:
        self.nodes:list[TerrainNode|None] = [None,None,None,None] 
        self.level = level
        
        self.nTopLeft:TerrainNode|None = self.nodes[0]
        self.nTopRight:TerrainNode|None = self.nodes[1]
        self.nBottomLeft:TerrainNode|None = self.nodes[3]
        self.nBottomRight:TerrainNode|None = self.nodes[2]
        
        
        self.points:list[tuple[float,float]] = [pTopLeft,pTopRight,pBottomRight,pBottomLeft]
        
        self.pTopLeft:tuple[float,float]=self.points[0]
        self.pTopRight:tuple[float,float]=self.points[1]
        self.pBottomLeft:tuple[float,float]=self.points[3]
        self.pBottomRight:tuple[float,float]=self.points[2]
        
            
        self.isLast = True
        self.isActive = True
        pass
    
    def draw(self,screenSurf:pg.surface.Surface):
        if(self.isActive):
            drawPoints = []
            for point in self.points:
                drawPoints.append((point[0]*screenSurf.get_width(),point[1]*screenSurf.get_height()))
            # pg.draw.polygon(screenSurf,pg.color.Color(255,255,255),self.points)
            pg.draw.lines(screenSurf,pg.color.Color(255,255,255),True,drawPoints,1)
        
        else:
            for node in self.nodes:
                if node != None:
                    node.draw(screenSurf)
    
    def subdivide(self)->None:
        # print(self,self.points)
        # for point in self.points:
        #     print(point)
            
        # for node in self.nodes:
        #     print(node)
        
        midTop = ((self.pTopLeft[0]+self.pTopRight[0])/2,(self.pTopLeft[1]+self.pTopRight[1])/2)
        midRight = ((self.pTopRight[0]+self.pBottomRight[0])/2,(self.pTopRight[1]+self.pBottomRight[1])/2)
        midBottom = ((self.pBottomLeft[0]+self.pBottomRight[0])/2,(self.pBottomLeft[1]+self.pBottomRight[1])/2)
        midLeft = ((self.pTopLeft[0]+self.pBottomLeft[0])/2,(self.pTopLeft[1]+self.pBottomLeft[1])/2)
        center = ((midLeft[0]+midRight[0])/2,(midLeft[1]+midRight[1])/2)
        
        
        self.nTopLeft = TerrainNode(self.pTopLeft,midTop,midLeft,center,self.level+1)
        self.nTopRight = TerrainNode(midTop,self.pTopRight,center,midRight,self.level+1)
        self.nBottomLeft = TerrainNode(midLeft,center,self.pBottomLeft,midBottom,self.level+1)
        self.nBottomRight = TerrainNode(center,midRight,midBottom,self.pBottomRight,self.level+1)
        
        self.nodes=[self.nTopLeft,self.nTopRight,self.nBottomRight,self.nBottomLeft]
        
        # for node in self.nodes:
        #     print(node.points)
        #     print()
        self.isLast = False
        self.isActive = False
        pass
    
    def converge(self)->None:
        if(self.level > 0):
            for node in self.nodes:
                node = None
                self.isLast = True
                
            self.nTopLeft = None
            self.nTopRight = None
            self.nBottomLeft = None
            self.nBottomRight = None
class QuadTerrain:
    def __init__(self) -> None:
        self.tree = TerrainNode((0.0,0.0),(1.0,0.0),(0.0,1.0),(1.0,1.0),0)
        
        # self.tree.subdivide()
        
            
        # self.subdivide(self.tree)
        
        pass
    
    def subdivide(self,node):
        node.subdivide()
        if(node.level < 6):
            for n in node.nodes:
                self.subdivide(n)
    
    def update(self,screenSurf:pg.surface.Surface):
        mousePos = pg.mouse.get_pos()
        mousePos = (mousePos[0]/screenSurf.get_width(),mousePos[1]/screenSurf.get_height())
        self.draw(screenSurf)
        pass
    
    def destroyTerrain(self,node,pointList:list[tuple[float,float]]):
        pass
        
    
    def divide():
        pass
    
    def draw(self,screenSurf:pg.surface.Surface):
        self.tree.draw(screenSurf)
        pass
    pass