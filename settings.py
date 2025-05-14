import pygame as pg
import xml.etree.ElementTree as ET
from Frame import *

def ReadXmlFile(Name):
    Tree = ET.parse(Name)
    Root = Tree.getroot()
    return Root

Config = ReadXmlFile("app.xml")
ConfigProjectAttribs = Config.attrib

def CreateDisplay():
    global CFrameObj, YUOffset, YBOffset, XLOffset, XROffset, Ow, Oh
    Mode = int(ConfigProjectAttribs["fullscreen"])
    Mode = pg.FULLSCREEN if Mode else pg.SHOWN
    YUOffset = 0
    YBOffset = 0
    XLOffset = 0
    XROffset = 0
    try: 
        if Mode == pg.FULLSCREEN: pass
        else:
            Frame = ConfigProjectAttribs["frame"]
            if Frame != "Standart":
                Mode = pg.NOFRAME
                FrameXml = ReadXmlFile(Frame)
                CFrameObj = CFrame(FrameXml)
                YUOffset = CFrameObj.Images["UpI"].get_height()
                YBOffset = CFrameObj.Images["BottomI"].get_height()
                XLOffset = CFrameObj.Images["LeftI"].get_width()
                XROffset = CFrameObj.Images["RightI"].get_width()
    except: pass
    Ow = int(ConfigProjectAttribs["width"]) if ConfigProjectAttribs["width"] != "Sw" else pg.display.Info().current_w
    Oh = int(ConfigProjectAttribs["height"]) if ConfigProjectAttribs["height"] != "Sh" else pg.display.Info().current_h
    s = pg.display.set_mode((Ow + XLOffset + XROffset, Oh + YUOffset + YBOffset), Mode, vsync=1)
    return s

pg.init()
vec2 = pg.math.Vector2
s = CreateDisplay()
pg.display.set_caption(ConfigProjectAttribs["title"])
clock = pg.time.Clock()