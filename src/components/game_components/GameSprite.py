import pygame as pg

import xml.etree.ElementTree as xmlET

projectileSize = (64,48)
characterSize = (144,128)

characterPaths = [
    "resources/characters/Converted_Vampire/"                 
]

def loadAllSprites():
    for path in characterPaths:
        
        
        tree = xmlET.parse(path+"data.xml")
        root = tree.getroot()
        characterTree = root[0]
        for child in characterTree:
            texName = child.attrib["name"].replace(".png","")
            texOffset = (float(child.attrib["x"]),float(child.attrib["y"]))
            texSize = (float(child.attrib["width"]),float(child.attrib["height"]))
            textCount = int(child.attrib["anim-count"])
    pass

class AnimatedSprite:
    def __init__(self,animCount,spriteSurf) -> None:
        self.animCount = animCount
        self.spriteSurf = spriteSurf
        pass
    pass

class StaticSprite:
    pass