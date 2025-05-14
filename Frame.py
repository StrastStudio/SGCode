import pygame as pg

pg.init()

class CFrame:
    def __init__(self, FrameXml):
        self.Frame = FrameXml
        self.Attribs = self.Frame.attrib
        self.Work = self.Attribs["work"]
        self.ImagesDict = {"Left": self.Frame.find("LEFTPIC").attrib,
                       "Right": self.Frame.find("RIGHTPIC").attrib,
                       "Up": self.Frame.find("UPPIC").attrib,
                       "UpLen": self.Frame.find("UPLENPIC").attrib,
                       "Bottom": self.Frame.find("BOTTOMPIC").attrib,
                       "BottomLen": self.Frame.find("BOTTOMLENPIC").attrib}
        if self.Work.startswith("Folder: "):
            Folder = self.Work.split("Folder: ")[1]
            self.Images = {}
            for Name, Image in self.ImagesDict.items():
                self.Images[f"{Name}I"] = pg.image.load(f"{Folder}/{Image["source"]}")
                if "crop" in Image:
                    Splitted = Image["crop"].split()
                    self.Images[f"{Name}I"] = self.Images[f"{Name}I"].subsurface(int(Splitted[0]), int(Splitted[1]), int(Splitted[2]), int(Splitted[3]))
    
    def update(self):
        pass

    def draw(self, Surf, Font, WriteFunc, PName):
        Surf.blit(pg.transform.scale(self.Images["LeftI"], (self.Images["LeftI"].get_width(), Surf.get_height())), (0, 5))
        Surf.blit(pg.transform.scale(self.Images["RightI"], (self.Images["RightI"].get_width(), Surf.get_height())), (Surf.get_width() - self.Images["RightI"].get_width(), 5))
        Surf.blit(self.Images["UpI"], (0, 0))
        Surf.blit(self.Images["UpI"], (Surf.get_width() - self.Images["UpI"].get_width(), 0))
        ULI = self.Images["UpLenI"]
        Surf.blit(pg.transform.scale(ULI, (Surf.get_width() - self.Images["UpI"].get_width(), ULI.get_height())), (self.Images["UpI"].get_width() // 2, 0))
        Surf.blit(self.Images["BottomI"], (0, Surf.get_height() - self.Images["BottomI"].get_height()))
        Surf.blit(self.Images["BottomI"], (Surf.get_width() - self.Images["BottomI"].get_width(), Surf.get_height() - self.Images["BottomI"].get_height()))
        BLI = self.Images["BottomLenI"]
        Surf.blit(pg.transform.scale(BLI, (Surf.get_width() - self.Images["BottomI"].get_width(), BLI.get_height())), (self.Images["BottomI"].get_width() // 2, Surf.get_height() - BLI.get_height()))      
        Name = WriteFunc(Font, PName, (255, 255, 255))[0]
        Surf.blit(Name, (10, self.Images["UpI"].get_height() // 2 - Name.get_height() // 2))