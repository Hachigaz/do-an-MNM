from __future__ import annotations

import pygame as pg
from pygame.rect import Rect
from pygame.surface import Surface
import pymunk as pm

import math

# import model.game_model.Player as Player
import model.game_model.PhysicSys as PhysicSys

from enum import Enum

import xml.etree.ElementTree as xmlET

import model.game_model.DesTerrain as Terrain

import threading

class AnimationFrame:
    def __init__(self,surf,transitionTime:float) -> None:
        self.surf:pg.surface.Surface = surf
        self.transitionTime:float = transitionTime
        self.isLockedFrame:bool = False
        pass

class Animation:
    currentTick: int
    def __init__(self,frameSurface:pg.surface.Surface,animCount:int,frameSize:pg.Vector2,rect:pg.rect.Rect, transitionTimes:list[float]) -> None:
        self.currentFrame = 0
        self.rect = rect
        resizedFrames = []
        self.resetAnimTick()
        self.totalAnimTime = sum(transitionTimes)
        
        for i in range(animCount):
            resizedFrames.append(AnimationFrame(pg.transform.scale(pg.surface.Surface.subsurface(frameSurface,pg.rect.Rect(frameSize.x*i,0,frameSize.x,frameSize.y)),rect.size),transitionTimes[i]))

        self.animationFrames:list[AnimationFrame] = resizedFrames
        
        self.invertedAnimFrames:list[AnimationFrame] = []
        for i in range(animCount):
            self.invertedAnimFrames.append(AnimationFrame(pg.transform.flip(resizedFrames[i].surf,True,False),transitionTimes[i]))
        pass
    
    def resetAnimTick(self):
        self.lastTick = pg.time.get_ticks()
        pass
    
    def increment(self)->None:
        self.currentFrame += 1
        if(self.currentFrame >= len(self.animationFrames)):
            self.currentFrame = 0
        pass
    
    def getTheFrame(self,isInverted:bool)->pg.surface.Surface:
        if isInverted:
            anim = self.invertedAnimFrames[self.currentFrame]
        else:
            anim = self.animationFrames[self.currentFrame]
            
        return anim.surf
    
    def isLastFrame(self)->bool:
        return self.currentFrame == (len(self.animationFrames) - 1)
        
    def isEndOfFrame(self)->bool:
        anim = self.animationFrames[self.currentFrame]
        if(Animation.currentTick - self.lastTick > anim.transitionTime and not anim.isLockedFrame):
            return True
        else:
            return False
    
    def lockFrame(self,frameIdx:int):
        self.animationFrames[frameIdx].isLockedFrame = True
        self.invertedAnimFrames[frameIdx].isLockedFrame = True
        
    def unlockFrame(self,frameIdx:int):
        self.animationFrames[frameIdx].isLockedFrame = False
        self.invertedAnimFrames[frameIdx].isLockedFrame = False
    
    def getTheFrameAndUpdate(self,isInverted:bool)->pg.surface.Surface:
        if isInverted:
            anim = self.invertedAnimFrames[self.currentFrame]
        else:
            anim = self.animationFrames[self.currentFrame]
            
        if(Animation.currentTick - self.lastTick > anim.transitionTime and not anim.isLockedFrame):
            self.increment()
            self.lastTick = Animation.currentTick
            
        return anim.surf
    
        
    
    def reset(self)->None:
        self.currentFrame = 0
        pass
    pass

class StaticGameObject(pg.sprite.Sprite):
    def __init__(self, rect:pg.rect.Rect, surf:pg.surface.Surface) -> None:
        super().__init__()        
        self.rect:pg.rect.Rect=rect
        self.surf:pg.surface.Surface = surf
        
        self.body = pm.Body(1,float("inf"),body_type=pm.Body.STATIC)
        self.body._set_position(rect.center)
        self.poly = pm.Poly.create_box(self.body,rect.size,0)
        self.poly.elasticity=0.0
        self.poly.friction = 1.0
        
        self.poly.collision_type = 1
        
        PhysicSys.PhysicManager.physicManager.addObject(self.body,self.poly)
    
        RenderManager.renderManager.addObject(self)

    def update(self,renderSurface:pg.surface.Surface):
        coord = pg.Vector2(self.body._get_position().x,self.body._get_position().y)-pg.Vector2(self.rect.size[0]/2,self.rect.size[1]/2)
        renderSurface.blit(self.surf,coord)
        pass
    pass

class CollideSurface:
    group:pg.sprite.Group = pg.sprite.Group()
    def __init__(self,surf:pg.Surface,rect:pg.rect.Rect) -> None:
        
        surf = pg.transform.scale(surf,pg.Vector2(rect.width,rect.height))
        
        self.object:StaticGameObject = StaticGameObject(rect,surf)
        
        CollideSurface.group.add(self.object)
        pass
    pass

class Sprite:
    def __init__(self,animations:dict[Animation],firstAnim=None,offsetPos:pg.Vector2=pg.Vector2(0,0),isInverted:bool=False) -> None:
        self.animations:dict[Animation] = animations
        
        self.isOneTimeAnim:bool = False
        
        self.isInverted:bool = isInverted
        
        if(isinstance(offsetPos,tuple)):
            offsetPos = pg.Vector2(offsetPos)
        self.offsetPos=offsetPos
        if(firstAnim==None):
            self.currentAnimation:int = list(self.animations.keys())[0]
        else:
            self.currentAnimation = firstAnim
        pass

    def render(self,renderSurface:pg.surface.Surface,coord:pg.Vector2,angle):
        
        
        angle = math.degrees(-angle)
        surface:pg.surface.Surface = self.animations[self.currentAnimation].getTheFrameAndUpdate(self.isInverted)
        surface = pg.transform.rotate(surface,angle)
        if self.isOneTimeAnim:
            currentAnim:Animation = self.animations[self.currentAnimation]
            if currentAnim.currentFrame == len(currentAnim.animationFrames) - 1:
                if currentAnim.isEndOfFrame():
                    self.isOneTimeAnim = False
                    self.changeAnim(self.nextAnim)
                    self.nextAnim = None
                
        if not self.isInverted:
            offset = self.offsetPos
            offset = pg.Vector2.rotate(offset,angle)
        else:
            offset = pg.Vector2(-self.offsetPos.x,self.offsetPos.y)
            offset = pg.Vector2.rotate(offset,angle)
        coord2 = coord + offset
        coord = coord + offset - pg.Vector2(surface.get_rect().width/2,surface.get_rect().height/2)
        renderSurface.blit(surface,coord)
        pg.draw.circle(renderSurface,pg.color.Color(255,0,0,255),coord2,2)
        
    
    def changeAnim(self,anim):
        if anim != self.currentAnimation:
            self.currentAnimation = anim
            self.animations[self.currentAnimation].reset()
    
    def invertObj(self):
        self.isInverted = not self.isInverted
        self.animations[self.currentAnimation].reset()
        
    def oneTimeAnim(self, playAnim:any, endAnim:any):
        self.changeAnim(playAnim)
        self.nextAnim = endAnim
        self.isOneTimeAnim = True
        
    def getCurrrentAnim(self)->Animation:
        return self.animations[self.currentAnimation]
    pass

class GameObject(pg.sprite.Sprite):
    group:pg.sprite.Group = pg.sprite.Group()
    def __init__(self, rect:pg.rect.Rect,collideBox:pg.rect.Rect,body:pm.body.Body = pm.Body(100,100000,pm.Body.DYNAMIC)) -> None:
        super().__init__()
        self.rect:pg.rect.Rect=rect
        
        
        self.body:pm.Body = body
        self.body._set_position((rect.center[0], rect.center[1]))
        
        self.poly:pm.Poly = pm.Poly.create_box(self.body,collideBox.size)
        self.poly.elasticity=0.0
        self.poly.friction=1.0
        self.poly.object = self
        self.sprites:dict[Sprite] = {}
        
        self.isInverted:bool = False
        
        PhysicSys.PhysicManager.physicManager.addObject(self.body,self.poly)
        
        RenderManager.renderManager.addObject(self)
        self.group.add(self)
        

    def invertSprites(self):
        self.isInverted = not self.isInverted
        for key,sprite in self.sprites.items():
            sprite.invertObj()

    def render(self,renderSurface:pg.surface.Surface,viewport):
        for key,sprite in self.sprites.items():
            sprite.render(renderSurface,pg.Vector2((self.body.position[0] - viewport.pos[0],self.body.position[1]-viewport.pos[1])),self.body.angle)
        pass

    def destroy(self):
        RenderManager.renderManager.removeObject(self)
        PhysicSys.PhysicManager.physicManager.removeObject(self.body,self.poly)
    
class Player(GameObject):
    def __init__(self, rect: Rect,healthCount:int) -> None:
        collideBox = pg.rect.Rect(0,0,75,65)
        super().__init__(rect, collideBox, pm.Body(100,float("inf"),pm.Body.DYNAMIC))
        
        self.sprites["tank"]=Sprite(GameModel.assets["spriteAnims"]["tank"])
        
        self.cannonAngle = 0.0
        self.firingPower = 10.0
        
        self.lastFired = 0.0
        
        self.health = healthCount
        
        
        self.poly.collision_type = 3
        pass    
    
    # def isOnAir(self)->bool:
    #     if self.object.body.velocity[1]<-10 or self.object.body.velocity[1]>10:
    #         return True
    #     else:
    #         return False
    
    # def moveLeft(self):
    #     self.isMoving = True
    #     if(self.isInverted):
    #         self.invertSprites()
            
    #     self.body.velocity = 40.0,self.body.velocity[1]

    #     pass
    
    # def moveRight(self):
    #     self.isMoving = True
    #     if(not self.isInverted):
    #         self.invertSprites()
            
    #     self.body.velocity = -40.0,self.body.velocity[1]
    #     pass
    
    # def rotateCannonUp(self):
    #     self.cannonAngle+=0.5
    #     if(self.cannonAngle>70.0):
    #         self.cannonAngle = 70.0
    #     pass
    
    # def rotateCannonDown(self):
    #     self.cannonAngle-=0.5
    #     if(self.cannonAngle<0.0):
    #         self.cannonAngle = 0.0
    #     pass
    
    def fireCannon(self):
        direction = self.getCannonDirection()
        offset = 50
        velocity = self.firingPower*10
        finalOffset = (self.body.position[0] + offset*direction.x,self.body.position[1]+ offset*direction.y)
        finalVelocity = (velocity*direction.x,velocity*direction.y)

        # print(finalOffset, finalVelocity, direction, velocity, offset)
        
        projectile = Projectile(pg.rect.Rect(finalOffset,(20,20)),finalVelocity)
        pass
    
    # def jump(self):
    #     self.body.velocity = self.body.velocity[0],-60.0
            
            
    def spinLeft(self):
        self.body.angle -= 0.04
        pass
    
    def spinRight(self):
        self.body.angle += 0.04
        pass
    
    def moveForward(self):
        moveVector = pg.Vector2.rotate(pg.Vector2(0.0,-70.0),math.degrees(self.body.angle))
        self.body.velocity = (moveVector.x,moveVector.y)
        pass    
    
    def moveBackward(self):
        pass
    
    def brake(self):
        if abs(self.body.velocity[0]) > 0:
            if(self.body.velocity[0]>0):
                self.body.velocity = (self.body.velocity[0]-2,self.body.velocity[1])
            else:
                self.body.velocity = (self.body.velocity[0]+2,self.body.velocity[1])
            if abs(self.body.velocity[0]) < 3:
                self.body.velocity = (0,self.body.velocity[1])
        if abs(self.body.velocity[1]) > 0:
            if(self.body.velocity[1]>0):
                self.body.velocity = (self.body.velocity[0],self.body.velocity[1]-2)
            else:
                self.body.velocity = (self.body.velocity[0],self.body.velocity[1]+2)
            if abs(self.body.velocity[1]) < 3:
                self.body.velocity = (self.body.velocity[0],0)
    
    def destroy(self):
        self.playerGroup.remove(self)
        super().destroy()
        
    def update(self):
        self.debugDraw(RenderManager.renderManager.viewport)
        pass
    
    def getCannonAngle(self)->float:
        if(not self.isInverted):
            return -self.cannonAngle + math.degrees(self.body.angle)
        else:
            return self.cannonAngle  + math.degrees(self.body.angle)
        pass
    
    def getCannonDirection(self)->pg.Vector2:
        if(not self.isInverted):
            directionVector = pg.Vector2(0,-1)
            cannonAngle = -self.cannonAngle + math.degrees(self.body.angle)
        else:
            directionVector = pg.Vector2(0,1)
            cannonAngle = self.cannonAngle  + math.degrees(self.body.angle)
        
        directionVector = pg.Vector2.rotate(directionVector,cannonAngle)
        
        return directionVector
    
    def debugDraw(self,viewport):
        # if(not self.isInverted):
        #     angleVector = pg.Vector2(100,0)
        #     cannonAngle = -self.cannonAngle + math.degrees(self.body.angle)
        # else:
        #     angleVector = pg.Vector2(-100,0)
        #     cannonAngle = self.cannonAngle  + math.degrees(self.body.angle)
            
        if(not self.isInverted):
            angleVector = pg.Vector2(0,-100)
            cannonAngle = -self.cannonAngle + math.degrees(self.body.angle)
        else:
            angleVector = pg.Vector2(0,100)
            cannonAngle = self.cannonAngle  + math.degrees(self.body.angle)
        
        angleVector = pg.Vector2.rotate(angleVector,cannonAngle)
        positionVector = pg.Vector2(self.body.position) - pg.Vector2(viewport.pos)
        
        
        pg.draw.lines(RenderManager.renderManager.renderSurface,pg.Color(255,255,255,255),False,[(positionVector.x,positionVector.y),(positionVector.x+angleVector.x,positionVector.y+angleVector.y)])
        pass
    pass

class Projectile(GameObject):
    def __init__(self, rect: Rect,velocity:tuple[float,float]) -> None:
        collideBox = pg.rect.Rect(0,0,20,12)
        super().__init__(rect, collideBox,pm.Body(1,100,pm.Body.DYNAMIC))
        
        self.sprites["projectile"] = Sprite(GameModel.assets["spriteAnims"]["projectile"])
        self.body.velocity = velocity
        self.poly.elasticity=1.0
        self.poly.collision_type = 4
        
        self.hitCount = 5
        if(velocity[0]<0):
            self.invertSprites()
    pass

    def wallImpact(arbiter:pm.Arbiter,space:pm.Space,data)->bool:
        # arbiter.shapes[0].object.destroy()
        # Terrain.Terrain.terrain.processCutTerrain(Terrain.Terrain.terrain.circleCursor,(arbiter.shapes[0].body.position))
        # Terrain.Terrain.terrain.processCutTerrain(Terrain.Terrain.terrain.circleCursor,(arbiter.shapes[0].body.position))
        
        projectile:Projectile = arbiter.shapes[0].object
        if(projectile.hitCount==0):
            projectile.impactExplode()
        projectile.hitCount -= 1
        pass
    
    def playerImpact(arbiter:pm.Arbiter,space:pm.Space,data)->bool:
        projectile:Projectile = arbiter.shapes[0].object
        projectile.impactExplode()
        
        player:Player = arbiter.shapes[1].object
        player.health -= 1
        pass
    
    def projectileImpact(arbiter:pm.Arbiter,space:pm.Space,data)->bool:
        projectile:Projectile = arbiter.shapes[0].object
        projectile.impactExplode()
    
        projectile:Projectile = arbiter.shapes[1].object
        projectile.impactExplode()
        pass
    
    def rockImpact(arbiter:pm.Arbiter,space:pm.Space,data)->bool:
        projectile:Projectile = arbiter.shapes[0].object
        projectile.impactExplode()
        pass
    
    def impactExplode(self):
        self.destroy()
        pass
    

    def updateAngle(self):
        angle = math.atan2(self.body.velocity[1],self.body.velocity[0])
        if(self.isInverted):
            angle = angle - math.radians(180)
        self.body.angle = angle
        pass
    
    def update(self):
        pass
    
    def render(self, renderSurface: Surface,viewport):
        self.updateAngle()
        return super().render(renderSurface,viewport)

class RenderManager:
    renderManager:RenderManager
    
    class Viewport:
        def __init__(self,viewportSize:tuple[int,int],renderSize:tuple[int,int],pos:tuple[0,0] = (0,0)) -> None:
            self.viewportSize = viewportSize
            self.pos:tuple[int,int] = pos
            self.renderSize = renderSize
            self.rect = pg.rect.Rect(pos[0]-renderSize[0]/2,pos[1]/renderSize[1],renderSize[0],renderSize[1])
            self.renderRatio = (viewportSize[0]/renderSize[0],viewportSize[1]/renderSize[1])
            self.revRenderRatio = (renderSize[0]/viewportSize[0],renderSize[1]/viewportSize[1])
            pass
        def setPosition(self,pos:tuple[0,0])->None:
            newPos = pg.Vector2(pos) - pg.Vector2(self.viewportSize[0]/2,self.viewportSize[1]/2)
            self.pos = (newPos.x,newPos.y)
    
    def __init__(self,renderSurface:pg.surface.Surface) -> None:
        self.renderSurface:pg.surface.Surface = renderSurface    
        self.viewport:RenderManager.Viewport = RenderManager.Viewport((self.renderSurface.get_width(),self.renderSurface.get_height()),(2500,1500))
        
        self.renderList:pg.sprite.Group = pg.sprite.Group()
        pass
    
    def addObject(self,object:GameObject)->None:
        self.renderList.add(object)
        pass
    
    def removeObject(self,object:GameObject)->None:
        self.renderList.remove(object)
        pass
    
    def render(self)->None:
        for sprite in self.renderList:
            sprite.render(self.renderSurface,self.viewport)
        pass
    pass

class GameModel:
    gameModel:GameModel = None
    assets:dict = {}
    
    def __init__(self,game_setting,renderSurface:pg.surface.Surface,currentPlayer:int) -> None:
        RenderManager.renderManager = RenderManager(renderSurface)
        PhysicSys.PhysicManager.physicManager = PhysicSys.PhysicManager()
        
        PhysicSys.PhysicManager.physicManager.projToWallImp.post_solve = Projectile.wallImpact
        PhysicSys.PhysicManager.physicManager.projToPlayerImp.post_solve = Projectile.playerImpact
        PhysicSys.PhysicManager.physicManager.projToProjImp.post_solve = Projectile.projectileImpact
        
        self.renderSurface:pg.surface.Surface = renderSurface
        self.currentPlayer:int = currentPlayer
        

        self.loadMap()
        
        self.objectUpdateGroups:list[pg.sprite.Group]=[Player.group,Projectile.group]
        
        self.players:list[Player]=[]
        self.game_setting = game_setting
        self.loadAssets()
        self.projectiles = []
        
        Terrain.Terrain.terrain = Terrain.Terrain()
        Terrain.Terrain.terrain.start()
        pass
    
    def start(self):
        pass
    
    def loadAssets(self):

        loadPath = "resources/tank_sprites/"
        sprites = [
            {
                "sprite":"tank",
                "size":100
            },
            {
                "sprite":"projectile",
                "size":20
            }
        ]
        GameModel.assets["spriteAnims"]={}
        
        for sprite in sprites:
            print(f"loading sprite: {sprite['sprite']}:")
            tree:xmlET.ElementTree = xmlET.parse(loadPath+sprite['sprite']+"/data.xml")
            root:xmlET.Element = tree.getroot()
            characterTree = root[0]
            
            anims:dict[Animation] = {}
            
            for subAnim in characterTree:
                print(f"loading animation: {subAnim.attrib['animation_name']}")
                
                animName = subAnim.attrib["animation_name"]
                texName = subAnim.attrib["name"]
                texOffset = pg.Vector2(float(subAnim.attrib["x"]),float(subAnim.attrib["y"]))
                texSize = pg.Vector2(float(subAnim.attrib["width"]),float(subAnim.attrib["height"]))
                texCount = int(subAnim.attrib["anim-count"])
                
                
                transitionTimes : list[float] = []
                for animFrame in subAnim:
                    transitionTimes.append(float(animFrame.attrib["transition-time"]))
                
                
                surfAspectRatio = (texSize.x/texCount)/texSize.y
                preferedSize = pg.Vector2(sprite["size"],sprite["size"]/surfAspectRatio)
                
                animSurf = pg.image.load(loadPath+sprite["sprite"]+"/"+texName)
                # animSurf.fill(pg.Color(255,255,255,255))
                animation = Animation(animSurf,texCount,pg.Vector2(texSize.x/texCount,texSize.y),pg.rect.Rect(0,0,preferedSize.x,preferedSize.y),transitionTimes)
                anims[animName]=animation
            
            GameModel.assets["spriteAnims"][sprite["sprite"]]=anims
            
        for i in range(self.game_setting["player_count"]):
            player = Player(pg.rect.Rect(200,100,100,100/2),self.game_setting["health_count"])
            self.players.append(player)
    
    def loadMap(self):
        # groundSurf = pg.surface.Surface(pg.Vector2(10,10))
        # groundSurf.fill(pg.color.Color(100,255,100))
        # self.groundSurface = CollideSurface(groundSurf,pg.rect.Rect(0,500,2000,1000))
        
        
        # # groundSurf = pg.surface.Surface(pg.Vector2(10,10))
        # # groundSurf.fill(pg.color.Color(100,255,100))
        # # self.groundSurface = CollideSurface(groundSurf,pg.rect.Rect(0,300,500,500))
        
        # groundSurf = pg.surface.Surface(pg.Vector2(10,10))
        # groundSurf.fill(pg.color.Color(100,255,100))
        # self.groundSurface = CollideSurface(groundSurf,pg.rect.Rect(1000,300,300,500))
        pass
    
    def update(self):
        # PhysicSys.PhysicManager.physicManager.debugUpdate(self.renderSurface)
        PhysicSys.PhysicManager.physicManager.update()
        
        terrainUpdateThread = threading.Thread(target=Terrain.Terrain.terrain.update)
        terrainUpdateThread.start()
        
        Animation.currentTick = pg.time.get_ticks()
        
        for group in self.objectUpdateGroups:
            for object in group:
                object.update()
            
            

        terrainUpdateThread.join()
        
        for player in self.players:
            player.isMoving = False
            
    def render(self):
        RenderManager.renderManager.viewport.setPosition(self.players[self.currentPlayer].body.position)
        
        terrainRenderThread = threading.Thread(target=Terrain.Terrain.terrain.render,args=[self.renderSurface,RenderManager.renderManager.viewport])
        terrainRenderThread.start()
        
        RenderManager.renderManager.render()
        
        terrainRenderThread.join()
        
    def getPlayerHealth(self,player):
        self.currentPlayer