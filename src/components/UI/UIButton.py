import components.UI.UIObject as UIObject

import pygame as pg

class UIButton(UIObject.UIObject):
    def __init__(self,surface:pg.Surface,rect:pg.Rect,text:str,fontSize:int,is_using_topleft = False)->None:
        super().__init__()
        
        surface = pg.transform.scale(surface,rect.size)
        if(not is_using_topleft):
            surfaceRect=pg.Rect((pg.Vector2(rect.topleft)-pg.Vector2(surface.get_size())/2),pg.Vector2(surface.get_size()))
        else:
            surfaceRect= rect
        self.uiSurfaces.insert(0,UIObject.uiSpriteElement(surface,surfaceRect))
        
        self.setFontSize(fontSize)
        self.setText(text)
        
        hover_surface_effect=pg.Surface(surface.get_size(),pg.SRCALPHA).convert_alpha()
        hover_surface_effect.fill((255,255,255,100))
        
        self.hoverEffects.insert(0,UIObject.uiSpriteElement(hover_surface_effect,surfaceRect))
        
        disabled_effect=pg.Surface(surface.get_size(),pg.SRCALPHA).convert_alpha()
        disabled_effect.fill((50,50,50,200))
        
        self.disabledEffects.insert(0,UIObject.uiSpriteElement(disabled_effect,surfaceRect))
        self.is_pressed = False
        self.prev_is_pressed = False
        self.trigger_func=None
        self.value = None
        pass
    

    def update(self,drawSurface:pg.Surface)->None:
        #draw button
        for sprite in self.uiSurfaces:
            sprite.draw(drawSurface)
        
        if(not self.is_disabled):
            #update trang thai
            self.prev_is_pressed = self.is_pressed    
            #check mouse co nam trong surface k
            if(self.uiSurfaces[0].rect.collidepoint(pg.Vector2(pg.mouse.get_pos()))):
                for sprite in self.hoverEffects:
                    sprite.draw(drawSurface)
                if(pg.mouse.get_pressed()[0]==1):
                    self.is_pressed = True
                else:
                    self.is_pressed = False
            #call function neu bam nut
            if(self.trigger_func!=None):
                if(self.is_pressed == False and self.prev_is_pressed == True):
                    if self.params==None:
                        self.trigger_func()
                    else:
                        self.trigger_func(*self.params)
        else:
            for sprite in self.disabledEffects:
                sprite.draw(drawSurface)
        pass
    
    def setFontSize(self,size:int):
        self.text_font = pg.font.Font("resources/ui/Font/kenvector_future_thin.ttf",size)
    
    def setText(self,text:str)->None:
        text_surface = self.text_font.render(text,True,pg.Color(255,255,255))
        text_rect=pg.Rect(pg.Vector2(self.uiSurfaces[0].rect.center)-(pg.Vector2(text_surface.get_size())/2),pg.Vector2(text_surface.get_size()))
        self.uiSurfaces.insert(1,UIObject.uiSpriteElement(text_surface,text_rect))
        
    def setTriggerFunction(self,func,params=None):
        self.trigger_func = func
        self.params = params