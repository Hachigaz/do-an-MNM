import pygame as pg
import components.UI.UIObject as UIObject

class UIText(UIObject.UIObject):
        def __init__(self,textSurf:pg.Surface,textRect:pg.Rect) -> None:
                super().__init__()
                rect=pg.Rect((pg.Vector2(textRect.topleft)-pg.Vector2(textSurf.get_size())/2),pg.Vector2(textSurf.get_size()))
                self.uiSurfaces.insert(0,UIObject.uiSprite(textSurf,rect))