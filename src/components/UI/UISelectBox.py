import components.UI.UIObject as UIObject

import components.game_components.Textures as Textures

import pygame as pg

class BoxItem(UIObject.UIObject):
    def __init__(self,surf:pg.Surface,rect:pg.Rect, itemValue,image:pg.Surface=None,text:str =None,isSelected: bool = False):
        super().__init__()
        rect = pg.Rect(pg.Vector2(rect.topleft)-pg.Vector2(rect.size)/2,rect.size)
        
        self.is_selected = isSelected
        self.uiSurfaces.insert(0,UIObject.uiSpriteElement(surf,rect))
        self.value = itemValue
        
        
        hover_surface_effect=pg.Surface(surf.get_size(),pg.SRCALPHA).convert_alpha()
        hover_surface_effect.fill((255,255,255,100))
        
        self.hoverEffects.insert(0,UIObject.uiSpriteElement(hover_surface_effect,rect))
        
        disabled_effect=pg.Surface(surf.get_size(),pg.SRCALPHA).convert_alpha()
        disabled_effect.fill((50,50,50,200))
        
        self.disabledEffects.insert(0,UIObject.uiSpriteElement(disabled_effect,rect))
        
        self.text = text
        self.image = image
        if text != None:
            self.setFontSize(20)
            self.setText(text)
        else:
            # self.uiSurfaces[1].surface = None
            # self.uiSurfaces[1].rect = None
            pass
            
        if(image!=None):
            imageSize = image.get_rect().size
            imagePos = pg.Vector2(self.uiSurfaces[0].rect.top)-pg.Vector2(imageSize)/2

            self.uiSurfaces.insert(2,UIObject.uiSpriteElement(image,pg.Rect(imagePos.x,imagePos.y,imageSize.x,imageSize.y)))
        else:
            # self.uiSurfaces[2].surface = None
            # self.uiSurfaces[2].rect = None
            pass
        pass
    
    def update(self, drawSurface:pg.Surface):
        for surface in self.uiSurfaces:
            surface.draw(drawSurface)
        
        
        if(not self.is_disabled and not self.is_selected):
            if(self.uiSurfaces[0].rect.collidepoint(pg.Vector2(pg.mouse.get_pos()))):
                for sprite in self.hoverEffects:
                    sprite.draw(drawSurface)
        else:
            for sprite in self.disabledEffects:
                sprite.draw(drawSurface)
        
        
    def setFontSize(self,size:int):
        self.text_font = pg.font.Font("resources/ui/Font/kenvector_future_thin.ttf",size)
    
    def setText(self,text:str)->None:
        text_surface = self.text_font.render(text,True,pg.Color(255,255,255))
        text_pos = pg.Vector2(self.uiSurfaces[0].rect.centerx,self.uiSurfaces[0].rect.bottom)-pg.Vector2(text_surface.get_size())/2
        text_pos.y -= 40
        text_rect=pg.Rect(text_pos,pg.Vector2(text_surface.get_size()))
        self.uiSurfaces.insert(1,UIObject.uiSpriteElement(text_surface,text_rect))
        

class UISelectBox(pg.sprite.Sprite):
    def __init__(self,rect:pg.Rect,itemSize:pg.Vector2) -> None:
        super().__init__()
        self.rect = pg.Rect(pg.Vector2(rect.topleft)-pg.Vector2(rect.size)/2,rect.size)
        self.itemCount = 0
        self.items = []
        self.itemSize = itemSize
    
    def addItem(self, newItemValue, newItemText:str = None, newItemImg:pg.Surface = None):
        self.itemCount = len(self.items)+1
        
        newItems = []
        
        itemSize = self.itemSize
        surface = pg.transform.scale(pg.image.load("resources/ui/PNG/frame.png"),itemSize)
        
        for i in range(self.itemCount):
            itemPos = pg.Vector2(self.rect.midleft) + pg.Vector2((i+1)*self.rect.width/(self.itemCount+1),0)
            
            itemImg = None
            itemText = None
            itemValue = None
            if i < self.itemCount - 1:
                itemImg = self.items[i].image
                itemText = self.items[i].text
                itemValue = self.items[i].value
            else:
               itemValue =  newItemValue
               itemText = newItemText
               itemImg = newItemImg
            item = BoxItem(surface,pg.Rect(itemPos.x,itemPos.y,itemSize.x,itemSize.y),itemValue,itemImg,itemText)
            newItems.append(item)
        self.items.clear()
        self.items = newItems
            
            
        
    def update(self,drawSurface:pg.Surface)->None:
        for item in self.items:
            item.update(drawSurface)
            if(not item.is_selected and item.uiSurfaces[0].rect.collidepoint(pg.Vector2(pg.mouse.get_pos()))):
                if(pg.mouse.get_pressed()[0]==1):
                    item.is_selected = True
                    print(self.getSelectedValue())
                    for item2 in self.items:
                        if item2 != item:
                            item2.is_selected=False
                            
    def getSelectedValue(self):
        for item in self.items:
            if item.is_selected:
                return item.value