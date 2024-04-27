from __future__ import annotations

import pygame as pg
import model.game_model.Player as Player
from enum import Enum
import pygame as pg


import xml.etree.ElementTree as xmlET



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
        
    
        RenderManager.renderManager.addObject(self)

    def update(self,renderSurface:pg.surface.Surface):
        renderSurface.blit(self.surf,self.rect)
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

class GameObject(pg.sprite.Sprite):
    def __init__(self, rect:pg.rect.Rect, animations:dict[Animation],firstAnim:any = None) -> None:
        super().__init__()        
        self.rect:pg.rect.Rect=rect
        self.animations:dict[Animation] = animations
        
        self.isInverted = False
        
        self.isOneTimeAnim = False
        
        if(firstAnim==None):
            self.currentAnimation:int = list(self.animations.keys())[0]
        else:
            self.currentAnimation = firstAnim
        
        
        RenderManager.renderManager.addObject(self)

    def update(self,renderSurface:pg.surface.Surface):
        if self.isOneTimeAnim:
            currentAnim:Animation = self.animations[self.currentAnimation]
            if currentAnim.currentFrame == len(currentAnim.animationFrames) - 1:
                if currentAnim.isEndOfFrame():
                    self.isOneTimeAnim = False
                    self.changeAnim(self.nextAnim)
                    self.nextAnim = None
                    
        renderSurface.blit(self.animations[self.currentAnimation].getTheFrameAndUpdate(self.isInverted),self.rect)
        pass
    
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

class PlayerStatus(Enum):
    IDLE = 0
    WALKING = 1
    RUNNING = 2
    ON_AIR = 3
    ON_HIT = 4

class Player:
    playerGroup:pg.sprite.Group = pg.sprite.Group()
    def __init__(self,object:GameObject) -> None:
        self.object:GameObject = object
        self.attacks:list[Attack]
        self.isStunned:bool = False
        self.isBlocking:bool = False
        self.isAttacking:bool = False
        self.isMoving:bool = False
        self.isOnAir:bool = False
        self.isIdle: bool = True
        self.jumpForce:float = 0.0
        self.object.changeAnim("idle")
        
        Player.playerGroup.add(object)
        pass
        
    
    def moveLeft(self):
        if(not self.isAttacking):
            self.isMoving = True
            if(self.object.isInverted):
                self.object.invertObj()
                
            self.object.rect.x += 10
            if(not self.isOnAir):
                self.object.changeAnim("run")

        pass
    
    def moveRight(self):
        if(not self.isAttacking):
            self.isMoving = True
            if(not self.object.isInverted):
                self.object.invertObj()
                
            self.object.rect.x -= 10
            if(not self.isOnAir):
                self.object.changeAnim("run")
        pass
    
    def jump(self):
        if(not self.isAttacking and not self.isOnAir):
            self.jumpForce = 20.0
            self.isOnAir = True
            self.object.animations["jump"].lockFrame(5)
            self.object.oneTimeAnim("jump","idle")
            
    def get_hurt(self):
        self.object.oneTimeAnim("hurt")
    
    def attack1(self):
        if(not self.isOnAir):
            self.isAttacking = True
            self.object.oneTimeAnim("attack_1","idle")
        pass
    
    def attack2(self):
        if(not self.isOnAir):
            self.isAttacking = True
            self.object.oneTimeAnim("attack_2","idle")
        pass
    
    def attack3(self):
        if(not self.isOnAir):
            self.isAttacking = True
            self.object.oneTimeAnim("attack_3","idle")
        pass
    
    def block(self):
        pass
    
    def update(self):
        if(self.isAttacking):
            if self.object.getCurrrentAnim().isLastFrame() and self.object.getCurrrentAnim().isEndOfFrame():
                self.isAttacking=False
            
        if(self.isOnAir):
            self.object.rect.y -= self.jumpForce
            if(self.jumpForce>-20):
                self.jumpForce -= 0.75
                if(self.jumpForce<-20):
                    self.jumpForce = -20
                pass
        pass
                    
        for surface in CollideSurface.group:
            if(self.object.rect.colliderect(surface.rect)):
                print(self.object.rect)
                if self.jumpForce<0:
                    self.object.rect.bottom = surface.rect.top
                    if(self.isOnAir):
                        self.isOnAir = False
                        if(self.jumpForce>0):
                            self.jumpForce = 0
                elif self.jumpForce>=0:
                    self.object.rect.top = surface.rect.bottom
                    self.jumpForce = 0
                    pass
                
        if(not self.isMoving or self.isAttacking or self.isBlocking or self.isStunned or self.isOnAir):
            if(not self.isIdle):
                self.object.changeAnim("idle")
                self.isIdle = True
        else:
            self.isIdle = False
    
    pass

class Attack:
    def __init__(self,attackObject:GameObject,attackRect:pg.rect.Rect) -> None:
        self.attackObject:GameObject
        self.attackRect:pg.rect.Rect
        pass
    
    def render(self,renderRect:pg.surface.Surface):
        pass
    pass

class AttackManager:
    def __init__(self) -> None:
        pass
    
    def addAttack(self,attack):
        pass
    
    pass

class RenderManager:
    renderManager:RenderManager
    
    def __init__(self) -> None:
        self.renderList:pg.sprite.Group = pg.sprite.Group()
        pass
    
    def addObject(self,object:GameObject)->None:
        self.renderList.add(object)
        
        print(self.renderList)
        pass
    
    def removeObject(self,object:GameObject)->None:
        self.renderList.remove(object)
        pass
    
    def render(self,renderSurface:pg.surface.Surface)->None:
        self.renderList.update(renderSurface)
        pass
    pass

class GameModel:
    def __init__(self,characters:list[str],map:str,renderSurface:pg.surface.Surface) -> None:
        RenderManager.renderManager = RenderManager()
        self.renderSurface:pg.surface.Surface = renderSurface
        
        self.players:list[Player]=[]
        self.loadAssets(characters=characters)
        
        self.loadMap(map)
        self.projectiles = []
        pass
    
    def start(self):
        pass
    
    def loadAssets(self,characters:list[str]):
        projectileSize = (64,48)
        characterSize = (144,128)

        loadPath= "resources/characters/"
        
        
        
        for character in characters:
            print(f"loading character: {character}:")
            tree:xmlET.ElementTree = xmlET.parse(loadPath+character+"/data.xml")
            root:xmlET.Element = tree.getroot()
            characterTree = root[0]
            
            trueSize:pg.Vector2 = pg.Vector2(float(characterTree.attrib["true-width"]),float(characterTree.attrib["true-height"]))
            characterAnims:dict[Animation] = {}
            
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
                preferedSize = pg.Vector2(300,300/surfAspectRatio)
                
                animSurf = pg.image.load(loadPath+character+"/"+texName)
                animation = Animation(animSurf,texCount,pg.Vector2(texSize.x/texCount,texSize.y),pg.rect.Rect(0,0,preferedSize.x,preferedSize.y),transitionTimes)
                characterAnims[animName]=animation
                
                    
            
            
            characterStats = root[1]
            for child in characterStats:
                statName = child.attrib["name"]
                statValue = child.attrib["value"]
                
                pass
            
            projectilesRoot:xmlET.Element = root.find("Projectiles")
            if projectileSize != None:
                pass
                
            
            player = Player(GameObject(pg.rect.Rect(200,300,trueSize.x,trueSize.y),characterAnims))
            
            self.players.append(player)
    
    def loadMap(self,map:str):
        groundSurf = pg.surface.Surface(pg.Vector2(10,10))
        groundSurf.fill(pg.color.Color(100,255,100))
        self.groundSurface = CollideSurface(groundSurf,pg.rect.Rect(0,700,2000,1000))
    
    def update(self):
        Animation.currentTick = pg.time.get_ticks()
        
        for player in self.players:
            player.update()
            
            
        RenderManager.renderManager.render(self.renderSurface)
        
        
        for player in self.players:
            player.isMoving = False