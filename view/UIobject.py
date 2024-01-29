import pygame as pg
UIgroup = pg.sprite.Group

class UIObject(pg.sprite.Sprite):
    def __init__(self) -> None:
        self.add(UIgroup)
        pass