import view.UI.UIObject as UIobject

import model.GameObject.Textures as Textures

import pygame as pg

class MenuReturnBtn(UIobject):
    def __init__(self,rect:pg.Rect)->None:
        super().__init__(rect,Textures.loadedSurfaces["blue_button00"])
        pass
    
    def draw(self)->None:
        pass
    
    pass