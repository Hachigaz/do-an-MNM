from __future__ import annotations

import pygame as pg
import pymunk as pm

import shapely as sp
import shapely.affinity as spaffinity

import numpy as np

import model.game_model.PhysicSys as PhysicSys

class CursorFrag:
    def __init__(self,pointList:list[tuple[float,float]],pos:tuple[float,float]) -> None:
        self.pointList : tuple[float,float]=pointList
        self.pos:tuple[float,float] = pos
        self.spPoly:sp.Polygon =  sp.Polygon(self.pointList)
    
        self.centroid = (self.spPoly.centroid.x,self.spPoly.centroid.y)
        self.poly:pm.Poly = pm.Poly(None,self.pointList)
        pass
    
class Fragment:
    def __init__(self,pointList:list[tuple[float,float]],pos:tuple[float,float],inners:list[list[tuple[float,float]]]=None,bodyType = pm.body.Body.STATIC,collision_type:int = 1) -> None:
        self.pointList : tuple[float,float]=pointList
        
        # self.body.body_type = pm.Body.DYNAMIC
        # self.body.activate()
        # self.body.sleep()
        
        self.spPoly:sp.Polygon =  sp.Polygon(self.pointList,inners)
        
        self.body:pm.Body=pm.Body(1,100,bodyType)
        
        # print(self.spPoly.centroid)
        # self.body.position=(self.spPoly.centroid.x,self.spPoly.centroid.y)
        
        self.body.position = pos
        
        self.poly:pm.Poly = pm.Poly(self.body,self.pointList)
        self.poly.friction=1.0
        self.poly.elasticity=1.0
        self.poly.collision_type = collision_type
        
        self.lineWidth:int = 1
        self.drawColor:pg.color.Color = pg.color.Color(255,255,255,255)
        
        PhysicSys.PhysicManager.physicManager.addObject(self.body,self.poly)
        pass
    
    def update(self):
        pass
    
    def getLocalTransformedShape(self)->sp.Polygon:
        orientation = self.body.angle
        pShape = spaffinity.rotate(self.spPoly,orientation,(self.spPoly.centroid.x,self.spPoly.centroid.y),True)
        return pShape
        pass
    
    def getTransformedShape(self)->sp.Polygon:
        position = self.body.position
        orientation = self.body.angle
        
        pShape = spaffinity.rotate(self.spPoly,orientation,(self.spPoly.centroid.x,self.spPoly.centroid.y),True)
        pShape = spaffinity.translate(pShape,position.x,position.y)
        return pShape
    
    def getTransformedShapeWithHoles(self)->sp.Polygon:
        position = self.body.position
        orientation = self.body.angle
        
        pShape = spaffinity.translate(self.spPoly,position.x,position.y)
        return spaffinity.rotate(pShape,orientation,(self.spPoly.centroid.x,self.spPoly.centroid.y),True)    
    
    def render(self,screenSurf,viewport)->None:
        drawShape:sp.Polygon = self.getLocalTransformedShape()
        drawPos = pg.Vector2(self.body.position) - pg.Vector2(viewport.pos)
        drawShape = spaffinity.translate(drawShape,drawPos.x,drawPos.y)
        
        pg.draw.lines(screenSurf,self.drawColor,True,drawShape.exterior.coords[:-1],self.lineWidth)
        
        
        pg.draw.circle(screenSurf,pg.color.Color(255,255,255,255),drawPos,1,2)
        
        for inner in drawShape.interiors:
            pg.draw.lines(screenSurf,pg.color.Color(255,0,0,255),True,inner.coords[:-1],self.lineWidth)

    def destroyFragment(self):
        PhysicSys.PhysicManager.physicManager.removeObject(self.body,self.poly)
        TerrainManager.terrainManager.removeFragment(self)
    
    def isPointInFragment(self,point:tuple[float,float])->bool:
        return spaffinity.translate(self,point[0],point[1]).contains(sp.Point(point))

    def isCursorInFrag(self,cursorFrag:CursorFrag):
        localizedMousePos = (cursorFrag.pos[0]-self.body.position[0],cursorFrag.pos[1]-self.body.position[1])
        cursorShape = spaffinity.translate(cursorFrag.spPoly,localizedMousePos[0],localizedMousePos[1])
        
        isCurInFrag = False
        for p in cursorShape.exterior.coords[:-1]:
            if(not isCurInFrag):
                isCurInFrag |= self.spPoly.contains(sp.Point(p[0],p[1]))
            else: 
                break
        
        return isCurInFrag
        
    def isCursorInFragLoc(self,localizedCurFrag:sp.Polygon):
        isCurInFrag = False
        for p in localizedCurFrag.exterior.coords[:-1]:
            if(not isCurInFrag):
                isCurInFrag |= self.spPoly.contains(sp.Point(p[0],p[1]))
            else: 
                break
        
        return isCurInFrag
    
    def isFragInCursor(self,cursorFrag:CursorFrag):
        localizedMousePos = (cursorFrag.pos[0]-self.body.position[0],cursorFrag.pos[1]-self.body.position[1])
        cursorShape = spaffinity.translate(cursorFrag.spPoly,localizedMousePos[0],localizedMousePos[1])
        
        return cursorShape.contains(self.spPoly)
    
    def isFragInCursorLoc(self,localizedCurFrag:sp.Polygon):
        return localizedCurFrag.contains(self.spPoly)
        
    def cutFrag(self, cursorFrag:CursorFrag):
        oldPos = self.body.position
        localizedMousePos = (cursorFrag.pos[0]-oldPos[0],cursorFrag.pos[1]-oldPos[1])
        cursorShape = spaffinity.translate(cursorFrag.spPoly,localizedMousePos[0],localizedMousePos[1])
        if(self.isCursorInFragLoc(cursorShape)):
            newShape:sp.Polygon = self.spPoly.difference(cursorShape)
            if not newShape.is_empty:
                if newShape.geom_type == "Polygon":
                    interiors = []
                    for inter in newShape.interiors:
                        interiors.append(inter.coords[:-1])
                    if len(interiors) == 0:
                        interiors = None
                    self.destroyFragment()
                    newPos = (oldPos[0]+newShape.centroid.x,oldPos[1]+newShape.centroid.y)
                    newShape = spaffinity.translate(newShape,-newShape.centroid.x,-newShape.centroid.y)
                        
                    TerrainManager.terrainManager.addFragment(Fragment(newShape.exterior.coords[:-1],newPos,interiors,self.body.body_type))
                    
                elif newShape.geom_type == "MultiPolygon":
                    self.destroyFragment()
                    for shape in newShape.geoms:
                        newPos = (oldPos[0]+shape.centroid.x,oldPos[1]+shape.centroid.y)
                        shape = spaffinity.translate(shape,-shape.centroid.x,-shape.centroid.y)
                        
                        interiors = []
                        for inter in shape.interiors:
                            interiors.append(inter.coords[:-1])
                        if len(interiors) == 0:
                            interiors = None
                            
                        TerrainManager.terrainManager.addFragment(Fragment(shape.exterior.coords[:-1],newPos,interiors,pm.body.Body.STATIC))
                    pass
                else:
                    self.destroyFragment()
                    pass
            else:
                self.destroyFragment()
                pass  
        elif self.isFragInCursorLoc(cursorShape):
            self.destroyFragment()
    
    def convertToStatic():
        pass
    
    def convertToDynamic():
        pass

class TerrainManager:
    terrainManager:TerrainManager = []
    
    def __init__(self) -> None:
        self.terrainFragments:list[Fragment] = []
        pass
    
    def addFragment(self,fragment:Fragment):
        if not fragment in self.terrainFragments:
            self.terrainFragments.append(fragment)
        pass
    
    def removeFragment(self,fragment:Fragment):
        if fragment in self.terrainFragments:
            self.terrainFragments.remove(fragment)
        pass
    
    def update(self):
        for fragment in self.terrainFragments:
            fragment.update()
            
    def render(self,screenSurf:pg.surface.Surface,viewport):
        for fragment in self.terrainFragments:
            fragment.render(screenSurf,viewport)
    
class Terrain:
    terrain:Terrain=None
    def __init__(self) -> None:
        self.rectCursor = [(-20,-20),(-20,20),(20,20),(20,-20)]
        self.circleCursor = sp.Point(0,0).buffer(30,8).exterior.coords[:-1]
        TerrainManager.terrainManager = TerrainManager()
        self.selectedCursor = self.circleCursor
        terrain = [(1000,0),(1000,500),(0,500),(0,0)]
        
        map = [
            {
                "rect":pm.Poly.create_box(None,(2000,100)).get_vertices(),
                "pos":(1000,1500)
            },
            {
                "rect":pm.Poly.create_box(None,(2000,100)).get_vertices(),
                "pos":(1000,0)
            },
            {
                "rect":pm.Poly.create_box(None,(40,1500)).get_vertices(),
                "pos":(0,750)
            },
            {
                "rect":pm.Poly.create_box(None,(40,1500)).get_vertices(),
                "pos":(2000,750)
            }
        ]
        
        for rect in map:       
            TerrainManager.terrainManager.addFragment(Fragment(rect["rect"],rect["pos"]))
            
        pass
    
    def start(self):
        self.terrainFragments = []
        pass
    
    def update(self):
        # mousePos = pg.mouse.get_pos()
        
        # if pg.mouse.get_pressed()[0] :
        #     self.processCutTerrain(self.selectedCursor,mousePos)
        # if pg.mouse.get_pressed()[2] :
        #     self.changeFragBodyType(self.selectedCursor,mousePos)
        
            
        TerrainManager.terrainManager.update()
        pass
    
    def render(self,screenSurf:pg.surface.Surface,viewport):
        # mousePos = pg.mouse.get_pos()
        # pg.draw.lines(screenSurf,pg.color.Color(0,0,255,255),True,[(p[0]+mousePos[0],p[1]+mousePos[1]) for p in self.selectedCursor],1)
        
        TerrainManager.terrainManager.render(screenSurf,viewport)
    
    def processCutTerrain(self,fragCursor:list[tuple[float,float]],pos:tuple[float,float]):
        cutFrag = CursorFrag(fragCursor,pos)
        for fragment in TerrainManager.terrainManager.terrainFragments:
            fragment:Fragment
            fragment.cutFrag(cutFrag)
        pass