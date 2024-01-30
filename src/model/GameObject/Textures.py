import pygame as pg
import xml.etree.ElementTree as xmlET

uiMapPaths = [
    "resources/ui/Spritesheet/blueSheet.png",
    "resources/ui/Spritesheet/yellowSheet.png",
    "resources/ui/Spritesheet/redSheet.png",
    "resources/ui/Spritesheet/greenSheet.png",
    "resources/ui/Spritesheet/greySheet.png",
    ]
uiMapXmlPaths = [
    "resources/ui/Spritesheet/blueSheet.xml",
    "resources/ui/Spritesheet/yellowSheet.xml",
    "resources/ui/Spritesheet/redSheet.xml",
    "resources/ui/Spritesheet/greenSheet.xml",
    "resources/ui/Spritesheet/greySheet.xml",
]

loadedSurfaces:[{"name":str,"surface":pg.Surface}] = []

def loadTextures()->None:
    for (path,xmlPath) in zip(uiMapPaths,uiMapXmlPaths):
        texSurface = pg.image.load(path)

        tree = xmlET.parse(xmlPath)
        root = tree.getroot()
        for child in root:
            texName = child.attrib["name"].replace(".png","")
            texOffset = (float(child.attrib["x"]),float(child.attrib["y"]))
            texSize = (float(child.attrib["width"]),float(child.attrib["height"]))

            loadedSurfaces.append({"name":texName,"surface":texSurface.subsurface(texOffset,texSize)})
    
    pass