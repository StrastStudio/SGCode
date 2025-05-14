from settings import *
from Scene import *
from copy import deepcopy
from random import choices
import getpass
import os
import ast
import pickle

# Class teampleate
# class SC_01(Scene):
#     def __init__(self, app):
#         self.app = app
#         super().__init__(self.app)

#     def update(self):
#         pass

Data = {
    "BestScore": 0,
    "MV": 0,
    "SV": 0
}

def LoadSave(app):
    global Data
    FullPath = f"C:/Users/{getpass.getuser()}/Documents/Strast Studio/{ConfigProjectAttribs["title"]}"
    if os.path.exists(f"{FullPath}/Save.dat"):
        with open(f"{FullPath}/Save.dat", "rb") as file:
            Read = ast.literal_eval(pickle.load(file))
        Data["BestScore"] = Read["BestScore"]
        Data["MV"] = Read["MV"]
        Data["SV"] = Read["SV"]
        app.Scenes.Sounds.ChangeVolumeMusic(Data["MV"] / 100)
        app.Scenes.Sounds.ChangeVolumeSound(Data["SV"] / 100)

class SC_01(Scene):
    def __init__(self, app):
        self.app = app
        super().__init__(self.app)
        self.RibbonOrig = self.Images["PicSC01RibbonBg"]
        self.RibbonCopy = deepcopy(self.RibbonOrig)
        self.RibbonCopy[2].x -= self.RibbonCopy[0].get_width()
        self.RibbonSpeed = None
        self.RibbonStartX = self.RibbonOrig[2].x
        self.Images["SSEngineRibbonCopy"] = self.RibbonCopy
        self.Anis["ASC01ContainerPaper"][0].AniFunc = self.CPFunc
        self.Anis["ASC01ContainerWaste"][0].AniFunc = self.CWFunc
        self.Anis["ASC01ContainerFood"][0].AniFunc = self.CFFunc
        self.Anis["ASC01ContainerIron"][0].AniFunc = self.CIFunc
        self.Anis["ASC01ContainerGlass"][0].AniFunc = self.CGFunc
        self.Anis["ASC01ContainerPlastic"][0].AniFunc = self.CPlFunc
        self.Containers = {"ASC01ContainerPaper": ["SSC01CPDef", "MVSC01CPOpen", "MVSC01CPClose", "SSC01CPOpen", 0, 0],
                           "ASC01ContainerWaste": ["SSC01CWDef", "MVSC01CWOpen", "MVSC01CWClose", "SSC01CWOpen", 0, 0],
                           "ASC01ContainerFood": ["SSC01CFDef", "MVSC01CFOpen", "MVSC01CFClose", "SSC01CFOpen", 0, 0],
                           "ASC01ContainerIron": ["SSC01CIDef", "MVSC01CIOpen", "MVSC01CIClose", "SSC01CIOpen", 0, 0],
                           "ASC01ContainerGlass": ["SSC01CGDef", "MVSC01CGOpen", "MVSC01CGClose", "SSC01CGOpen", 0, 0],
                           "ASC01ContainerPlastic": ["SSC01CPlDef", "MVSC01CPlOpen", "MVSC01CPlClose", "SSC01CPlOpen", 0, 0]}
        self.Garbage = [f"PicSC01Garbage{i}" for i in range(1, 21 + 1)]
        self.GarbagesPics = {}
        self.First = True
        self.IndexGarbage = 0
        self.FirstCreate = True
        self.Timer = Timer(0, self.MakeGarbage, True)
        self.TimerStartDur = None
        self.DiffRS = None
        self.DiffGTD = None
        self.GarbageZ = None
        self.SelectGarbageId = None
        self.PressId = None
        self.FindChickens = 0
        self.Score = 0
        self.LvTimer = Timer(1000, self.LvTimerFunc, True)
        # self.LvTimerDur = 1000
        self.LvTimerInt = 60
        self.STicks = 0
        self.TPause = None
        self.StartTimer = Timer(0, self.StartTimerFunc, True)
        self.StartTimerDur = 500
        self.StartTimerInt = 4
        self.Stop = False
        self.Sounds.CreateChannel(4)
        self.Sounds.CreateChannel(5)
        self.State = "Start"

    def Restart(self):
        self.LoadConfig()
        self.IndexGarbage = 0
        self.FirstCreate = True
        self.Score = 0
        self.FindChickens = 0
        self.PressId = None
        self.SelectGarbageId = None
        NeedPop = list(self.GarbagesPics.keys())
        for i in NeedPop: self.DeleteGarbage(i)
        self.GarbagesPics = {}
        self.TPause = None
        self.STicks = 0
        self.LvTimerInt = None
        self.First = True
        self.State = "Start"
        self.Stop = False
        self.Containers = {"ASC01ContainerPaper": ["SSC01CPDef", "MVSC01CPOpen", "MVSC01CPClose", "SSC01CPOpen", 0, 0],
                           "ASC01ContainerWaste": ["SSC01CWDef", "MVSC01CWOpen", "MVSC01CWClose", "SSC01CWOpen", 0, 0],
                           "ASC01ContainerFood": ["SSC01CFDef", "MVSC01CFOpen", "MVSC01CFClose", "SSC01CFOpen", 0, 0],
                           "ASC01ContainerIron": ["SSC01CIDef", "MVSC01CIOpen", "MVSC01CIClose", "SSC01CIOpen", 0, 0],
                           "ASC01ContainerGlass": ["SSC01CGDef", "MVSC01CGOpen", "MVSC01CGClose", "SSC01CGOpen", 0, 0],
                           "ASC01ContainerPlastic": ["SSC01CPlDef", "MVSC01CPlOpen", "MVSC01CPlClose", "SSC01CPlOpen", 0, 0]}
        for Value in self.ContainerTypes.values():
            self.Anis[Value[0]][0].State = "Standart"
            Movements = self.Anis[Value[0]][0].Movements
            for Movement in Movements.values():
                Movement[0].ImageIndex = 0
                Movement[0].Temp = 0

    def MakeGarbage(self):
        SrcImg = self.Images[choices(self.Garbage, weights= [99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 1])[0]] # PicSC01Garbage21
        Copy = deepcopy(SrcImg)
        Name = f"StrastStudioGarbage{self.IndexGarbage}"
        self.Images[Name] = Copy
        Copy[-2] = Name
        Copy[-3] = True
        self.IndexGarbage += 1
        if self.IndexGarbage == 100000 + 1: self.IndexGarbage = 0
        self.GarbagesPics[Name] = SrcImg[-2]
        if not self.FirstCreate:
            self.RibbonSpeed += self.DiffRS
            self.RibbonSpeed = min(10, self.RibbonSpeed)
            self.Timer.Duration -= self.DiffGTD
            self.Timer.Duration = max(300, self.Timer.Duration)
        else:
            self.Timer.Duration = self.TimerStartDur
            self.FirstCreate = False

    def LvTimerFunc(self):
        self.LvTimerInt -= 1
        if self.LvTimerInt < 0:
            self.LvTimerInt = 0
            self.Stop = True
            self.Sounds.Channels["4"].stop()
            self.app.ChangeScene("SC_GAMEOVER")
        # self.LvTimer.Duration = self.LvTimerDur
        
    def StartTimerFunc(self):
        self.StartTimerInt -= 1
        if self.StartTimerInt <= -1: 
            self.StartTimerInt = 3
            self.State = "Play"
        else: self.Sounds.PlaySound("SndSC01Start", 5)
        self.StartTimer.Duration = self.StartTimerDur

    def LoadConfig(self):
        SC01Config = self.Configs["SC_01"]
        Ribbon = SC01Config.find("RIBBON").attrib
        self.RibbonSpeed = float(Ribbon["StartRS"])
        self.TimerStartDur = float(Ribbon["StartGTD"])
        self.DiffRS = float(Ribbon["DiffRS"])
        self.DiffGTD = float(Ribbon["DiffGTD"])
        self.GarbageZ = int(Ribbon["GarbageZ"])
        self.GarbageTypes = {}
        self.ContainerTypes = {}
        for Garabge in SC01Config.findall("GARBAGE"):
            Attrib = Garabge.attrib
            self.GarbageTypes[Attrib["id"]] = Attrib["type"]
        for Container in SC01Config.findall("CONTAINER"):
            Attrib = Container.attrib
            self.ContainerTypes[Attrib["msg"]] = [Attrib["id"], Attrib["type"]]
        self.Messages = SC01Config.find("MESSAGES").attrib["list"].split()
        Timers = SC01Config.find("TIMERS").attrib
        self.LvTimerInt = int(Timers["LvTime"])
        self.StartTimerInt = int(Timers["StartTime"]) + 1

    def CPFunc(self, Pos):
        Index = 0 if self.Containers["ASC01ContainerPaper"][4] == 0 else 3
        Static = self.Statics["ASC01ContainerPaper"][self.Containers["ASC01ContainerPaper"][Index]]
        self.app.s.blit(Static["Image"], Pos + Static["Offset"])
    
    def CWFunc(self, Pos):
        Index = 0 if self.Containers["ASC01ContainerWaste"][4] == 0 else 3
        Static = self.Statics["ASC01ContainerWaste"][self.Containers["ASC01ContainerWaste"][Index]]
        self.app.s.blit(Static["Image"], Pos + Static["Offset"])
    
    def CFFunc(self, Pos):
        Index = 0 if self.Containers["ASC01ContainerFood"][4] == 0 else 3
        Static = self.Statics["ASC01ContainerFood"][self.Containers["ASC01ContainerFood"][Index]]
        self.app.s.blit(Static["Image"], Pos + Static["Offset"])
    
    def CIFunc(self, Pos):
        Index = 0 if self.Containers["ASC01ContainerIron"][4] == 0 else 3
        Static = self.Statics["ASC01ContainerIron"][self.Containers["ASC01ContainerIron"][Index]]
        self.app.s.blit(Static["Image"], Pos + Static["Offset"])
    
    def CGFunc(self, Pos):
        Index = 0 if self.Containers["ASC01ContainerGlass"][4] == 0 else 3
        Static = self.Statics["ASC01ContainerGlass"][self.Containers["ASC01ContainerGlass"][Index]]
        self.app.s.blit(Static["Image"], Pos + Static["Offset"])
    
    def CPlFunc(self, Pos):
        Index = 0 if self.Containers["ASC01ContainerPlastic"][4] == 0 else 3
        Static = self.Statics["ASC01ContainerPlastic"][self.Containers["ASC01ContainerPlastic"][Index]]
        self.app.s.blit(Static["Image"], Pos + Static["Offset"])

    def DeleteGarbage(self, Name):
        self.PressId = None
        self.SelectGarbageId = None
        self.Images.pop(Name)

    def update(self):
        if self.First:
            self.Anis["ASC01ContainerPaper"][0].update()
            self.Anis["ASC01ContainerWaste"][0].update()
            self.Anis["ASC01ContainerFood"][0].update()
            self.Anis["ASC01ContainerIron"][0].update()
            self.Anis["ASC01ContainerGlass"][0].update()
            self.Anis["ASC01ContainerPlastic"][0].update()
            self.LoadConfig()
            self.First = False
        if self.State == "Start":
            self.Texts["TextSC01Start"][-3] = True
            if self.TPause != None:
                self.StartTimer.PauseTicks += self.TPause
                self.TPause = None
            self.StartTimer.update()

        if self.State == "Play":
            self.Texts["TextSC01Start"][-3] = False
            if self.TPause != None:
                self.Timer.PauseTicks += self.TPause
                self.LvTimer.PauseTicks += self.TPause
                self.TPause = None
            self.Timer.update()
            self.LvTimer.update()
            self.RibbonOrig[2].x += self.RibbonSpeed * self.app.dt
            self.RibbonCopy[2].x += self.RibbonSpeed * self.app.dt
            NeedPop = []
            for GarbageName in self.GarbagesPics.keys():
                if self.PressId != GarbageName: 
                    self.Images[GarbageName][2].x += self.RibbonSpeed * self.app.dt
                    self.Images[GarbageName][2].z = self.GarbageZ
                if self.Images[GarbageName][2].x >= self.RibbonStartX + self.RibbonOrig[0].get_width() and self.PressId != GarbageName:
                    self.Images.pop(GarbageName)
                    NeedPop.append(GarbageName)
                    if self.SelectGarbageId == GarbageName: self.SelectGarbageId = None
                elif (self.SelectGarbageId == None or self.SelectGarbageId == GarbageName) and (self.PressId == None or self.PressId == self.SelectGarbageId):
                    Rect = pg.Rect(self.Images[GarbageName][2].x, self.Images[GarbageName][2].y, *self.Images[GarbageName][0].get_size())
                    if self.PressId == None:
                        if Rect.collidepoint(self.app.MousePos): self.SelectGarbageId = GarbageName
                        else: self.SelectGarbageId = None
                        if pg.mouse.get_pressed()[0]: self.PressId = self.SelectGarbageId
                    elif self.PressId == self.SelectGarbageId: 
                        self.Images[self.SelectGarbageId][2].x = self.app.MousePos.x - self.Images[self.SelectGarbageId][0].get_width() // 2
                        self.Images[self.SelectGarbageId][2].y = self.app.MousePos.y - self.Images[self.SelectGarbageId][0].get_height() // 2
                        self.Images[self.SelectGarbageId][2].z = -1000
                        if self.GarbageTypes[self.GarbagesPics[self.SelectGarbageId]] == "Курица": 
                            self.Sounds.PlaySound("SndSC01Chicken")
                            self.FindChickens += 1
                            self.Score += 100000
                            self.DeleteGarbage(GarbageName)
                            NeedPop.append(GarbageName)
                        elif self.app.CurMessage in self.Messages:
                            if pg.mouse.get_pressed()[0]:
                                if self.ContainerTypes[self.app.CurMessage][1] == self.GarbageTypes[self.GarbagesPics[self.SelectGarbageId]]: 
                                    self.Sounds.PlaySound("SndSC01Correct")
                                    self.Score += 25
                                else: 
                                    self.Sounds.PlaySound("SndSC01Incorrect")
                                    self.Score -= 25
                                self.DeleteGarbage(GarbageName)
                                NeedPop.append(GarbageName)
            [self.GarbagesPics.pop(Name) for Name in NeedPop]
            if self.RibbonOrig[2].x >= self.RibbonStartX + self.RibbonOrig[0].get_width():
                self.RibbonOrig[2].x = self.RibbonStartX
                self.RibbonCopy[2].x = self.RibbonStartX - self.RibbonCopy[0].get_width()
            for Name, Value in self.Containers.items():
                Static = self.Statics[Name][Value[0]]
                Rect = pg.Rect(*self.Anis[Name][0].StandartPos - Static["Offset"], *Static["Image"].get_size())
                if Value[4] == 1 and Value[5] == 1: self.Anis[Name][0].MovementStop = True
                if not Rect.collidepoint(self.app.MousePos): 
                    if (self.Anis[Name][0].State == Value[1] or self.Anis[Name][0].State == "Standart") and self.Anis[Name][0].MovementStop: self.Anis[Name][0].State = Value[2]
                    elif self.Anis[Name][0].State == Value[2] and self.Anis[Name][0].MovementStop: self.Anis[Name][0].State = "Standart"
                    Value[4] = 0
                    Value[5] = 0
                if Rect.collidepoint(self.app.MousePos): 
                    if (self.Anis[Name][0].MovementStop or self.Anis[Name][0].State == "Standart") and Value[5] == 0:
                        Value[5] = 1
                        self.Anis[Name][0].State = Value[1]
                    elif Value[5] == 1 and self.Anis[Name][0].State == Value[1] and self.Anis[Name][0].MovementStop:                     
                        Value[4] = 1
                        self.Anis[Name][0].State = "Standart"
        self.Score = max(0, self.Score)
        self.UpdText("TextSC01DebugRS", f"Скорость ленты: {self.RibbonSpeed}")
        self.UpdText("TextSC01DebugGS", f"Задержка спавна: {self.Timer.Duration}")
        self.UpdText("TextSC01DebugGC", f"Кол-во мусора: {len(self.GarbagesPics)}")
        self.UpdText("TextSC01FindChickens", f"Найдено куриц: {self.FindChickens}")
        self.UpdText("TextSC01SelGarbage", "")
        self.UpdText("TextSC01UIScore", str(self.Score))
        self.Texts["TextSC01UITime"][-6] = "FontWhiteNISDS"
        if self.LvTimerInt <= 10:
            self.Texts["TextSC01UITime"][-6] = "FontRedNISDS"
            if not self.Sounds.Channels["4"].get_busy() and not self.Stop: self.Sounds.PlaySound("SndSC01Time", 4)
        # if self.State == "Play": self.UpdText("TextSC01UITime", str(self.LvTimerInt))
        # else: self.UpdText("TextSC01UITime", "60")
        self.UpdText("TextSC01UITime", str(self.LvTimerInt))
        self.UpdText("TextSC01Start", str(self.StartTimerInt))
        if self.SelectGarbageId != None: 
            SelGPic = self.Images[self.SelectGarbageId]
            self.UpdText("TextSC01SelGarbage", self.GarbageTypes[self.GarbagesPics[self.SelectGarbageId]])
            self.Texts["TextSC01SelGarbage"][2].x = SelGPic[2].x + SelGPic[0].get_width() // 2 + self.Texts["TextSC01SelGarbage"][0].get_width() // 2
            self.Texts["TextSC01SelGarbage"][2].y = SelGPic[2].y - 50
        keys = pg.key.get_pressed()
        if keys[pg.K_ESCAPE]: 
            self.STicks = pg.time.get_ticks()
            self.app.ChangeScene("SC_PAUSE")
        if self.Buttons["BtnSCCMNHelp"].update():
            self.app.ScenesClassesDict["SC_HELP"].Scene = "SC_01"
            self.STicks = pg.time.get_ticks()
            self.app.ChangeScene("SC_HELP")
        self.Anis["ASC01ContainerPaper"][0].update()
        self.Anis["ASC01ContainerWaste"][0].update()
        self.Anis["ASC01ContainerFood"][0].update()
        self.Anis["ASC01ContainerIron"][0].update()
        self.Anis["ASC01ContainerGlass"][0].update()
        self.Anis["ASC01ContainerPlastic"][0].update()

class SC_PAUSE(Scene):
    def __init__(self, app):
        self.app = app
        super().__init__(self.app)

    def update(self):
        if self.Buttons["BtnSCPAUSEConfirm"].update(): 
            self.app.ChangeScene("SC_01")
            self.app.ScenesClassesDict["SC_01"].TPause = pg.time.get_ticks() - self.app.ScenesClassesDict["SC_01"].STicks
        if self.Buttons["BtnSCPAUSESettings"].update(): 
            self.app.ScenesClassesDict["SC_SETTINGS"].Scene = "SC_PAUSE"
            self.app.ChangeScene("SC_SETTINGS", False)
        if self.Buttons["BtnSCPAUSEMenu"].update():
            self.app.ScenesClassesDict["SC_01"].Restart()
            self.app.ChangeScene("SC_02")
        if self.Buttons["BtnSCCMNHelp"].update():
            self.app.ScenesClassesDict["SC_HELP"].Scene = "SC_PAUSE"
            self.app.ChangeScene("SC_HELP")

    
class SC_SETTINGS(Scene):
    def __init__(self, app):
        self.app = app
        super().__init__(self.app)
        self.ScrMV = self.Scrollers["ScrSCSETMusic"]
        self.ScrSV = self.Scrollers["ScrSCSETSound"]
        self.ScrMV.ChangeValue(self.Sounds.MusicVolume * 100)
        self.ScrSV.ChangeValue(self.Sounds.SoundVolume * 100)
        self.Scene = None

    def update(self):
        global Data
        self.Sounds.ChangeVolumeMusic(self.ScrMV.update() / 100)
        self.Sounds.ChangeVolumeSound(self.ScrSV.update() / 100)
        Data["MV"] = int(self.ScrMV.update())
        Data["SV"] = int(self.Sounds.SoundVolume * 100)
        if self.Buttons["BtnSCSETBack"].update(): 
            self.app.ChangeScene(self.Scene, False)
        if self.Buttons["BtnSCCMNHelp"].update():
            self.app.ScenesClassesDict["SC_HELP"].Scene = "SC_SETTINGS"
            self.app.ChangeScene("SC_HELP", False)

class SC_GAMEOVER(Scene):
    def __init__(self, app):
        self.app = app
        super().__init__(self.app)

    def update(self):
        global Data
        if self.app.ScenesClassesDict["SC_01"].Score >= Data["BestScore"]: Data["BestScore"] = self.app.ScenesClassesDict["SC_01"].Score
        self.UpdText("TextSCGOScore", f"Счёт: {self.app.ScenesClassesDict["SC_01"].Score}; Рекорд: {Data["BestScore"]}")
        if self.Buttons["BtnSCGORetry"].update(): 
            self.app.ChangeScene("SC_01")
            self.app.ScenesClassesDict["SC_01"].Restart()
        if self.Buttons["BtnSCGOMenu"].update():
            self.app.ScenesClassesDict["SC_01"].Restart()
            self.app.ChangeScene("SC_02")
        if self.Buttons["BtnSCCMNHelp"].update():
            self.app.ScenesClassesDict["SC_HELP"].Scene = "SC_GAMEOVER"
            self.app.ChangeScene("SC_HELP", False)

class SC_02(Scene):
    def __init__(self, app):
        self.app = app
        super().__init__(self.app)

    def update(self):
        if self.Buttons["BtnSC02Exit"].update(): self.app.ChangeScene("SC_EXIT")
        if self.Buttons["BtnSC02Titels"].update(): self.app.ChangeScene("SC_TITELS")
        if self.Buttons["BtnSC02Play"].update(): self.app.ChangeScene("SC_01")
        if self.Buttons["BtnSC02Settings"].update(): 
            self.app.ScenesClassesDict["SC_SETTINGS"].Scene = "SC_02"
            self.app.ChangeScene("SC_SETTINGS")
        if self.Buttons["BtnSCCMNHelp"].update():
            self.app.ScenesClassesDict["SC_HELP"].Scene = "SC_02"
            self.app.ChangeScene("SC_HELP")

class SC_TITELS(Scene):
    def __init__(self, app):
        self.app = app
        super().__init__(self.app)
        self.Speed = 1

    def End(self):
        self.Images["PicSCTITText"][2].y = self.app.s.get_height()
        self.app.ChangeScene("SC_02")

    def update(self):
        self.Images["PicSCTITText"][2].y -= self.Speed * self.app.dt
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE] or self.Images["PicSCTITText"][2].y + self.Images["PicSCTITText"][0].get_height() <= 0: self.End()

class SC_INTRO(Scene):
    def __init__(self, app):
        self.app = app
        super().__init__(self.app)
        self.ImageIndex = 0
        self.Alpha = 0
        self.Strast = self.Images["PicSCINTROStrast"]
        self.Strast[0].set_alpha(self.Alpha)
        self.GameLogo = self.Images["PicSCINTROGameLogo"]
        self.GameLogo[0].set_alpha(self.Alpha)
        self.ImagesList = [self.Strast, self.GameLogo]
        self.Direction = 1
        self.MaybeSpace = True
    
    def Skip(self):
        self.Direction = 1
        self.ImageIndex += 1

    def update(self):
        keys = pg.key.get_pressed()
        self.ImagesList[self.ImageIndex][0].set_alpha(self.Alpha)
        self.Alpha += 0.8 * self.Direction * self.app.dt
        if self.Alpha >= 350: self.Direction = -1
        if self.Alpha <= 0: 
            self.Alpha = 0
            self.Skip()
        if keys[pg.K_SPACE] and self.MaybeSpace: 
            self.Alpha = 0
            self.ImagesList[self.ImageIndex][0].set_alpha(self.Alpha)
            self.Skip()
            self.MaybeSpace = False
        if not keys[pg.K_SPACE]: self.MaybeSpace = True
        if self.ImageIndex >= len(self.ImagesList): 
            self.ImageIndex = 0
            self.app.ChangeScene("SC_02")


class SC_HELP(Scene):
    def __init__(self, app):
        self.app = app
        super().__init__(self.app)
        self.PlayBtn = self.Buttons["BtnSCHELPPlay"]
        self.PlayBtn.Active = True
        self.StopBtn = self.Buttons["BtnSCHELPStop"]
        self.StopBtn.Active = False
        self.Pics = {
            "SC_02": ["PicSCHELPSC02Pic0", "PicSCHELPSC02Pic1", "PicSCHELPSC02Pic2", "PicSCHELPSC02Pic3"],
            "SC_SETTINGS": ["PicSCHELPSCSETPic0", "PicSCHELPSCSETPic1", "PicSCHELPSCSETPic2"],
            "SC_01": ["PicSCHELPSC01Pic0", "PicSCHELPSC01Pic1", "PicSCHELPSC01Pic2"],
            "SC_PAUSE": ["PicSCHELPSCPAUSEPic0", "PicSCHELPSCPAUSEPic1", "PicSCHELPSCPAUSEPic2"],
            "SC_GAMEOVER": ["PicSCHELPSCGAMEOVERPic0", "PicSCHELPSCGAMEOVERPic1", "PicSCHELPSCGAMEOVERPic2"],
        }
        self.PicsDialogs = {
            "PicSCHELPSC02Pic0": "TKSCHELPSC02Help000",
            "PicSCHELPSC02Pic1": "TKSCHELPSC02Help001",
            "PicSCHELPSC02Pic2": "TKSCHELPSC02Help002",
            "PicSCHELPSC02Pic3": "TKSCHELPSC02Help003",
            "PicSCHELPSCSETPic0": "TKSCHELPSCSETHelp000",
            "PicSCHELPSCSETPic1": "TKSCHELPSCSETHelp001",
            "PicSCHELPSCSETPic2": "TKSCHELPSCSETHelp002",
            "PicSCHELPSC01Pic0": "TKSCHELPSC01Help000",
            "PicSCHELPSC01Pic1": "TKSCHELPSC01Help001",
            "PicSCHELPSC01Pic2": "TKSCHELPSC01Help002",
            "PicSCHELPSCPAUSEPic0": "TKSCHELPSCPAUSEHelp000",
            "PicSCHELPSCPAUSEPic1": "TKSCHELPSCPAUSEHelp001",
            "PicSCHELPSCPAUSEPic2": "TKSCHELPSCPAUSEHelp002",
            "PicSCHELPSCGAMEOVERPic0": "TKSCHELPSCGAMEOVERHelp000",
            "PicSCHELPSCGAMEOVERPic1": "TKSCHELPSCGAMEOVERHelp001",
            "PicSCHELPSCGAMEOVERPic2": "TKSCHELPSCGAMEOVERHelp002",
                            }
        self.Scene = "SC_02"
        self.CurrentId = 0
        self.NextDialog = None
        self.First = False
        self.AutoNext = False

    def ChangeDialog(self):
        self.Sounds.Channels["1"].stop()
        self.PlayBtn.Active, self.StopBtn.Active = False, True
        self.NextDialog = self.PicsDialogs[self.Pics[self.Scene][self.CurrentId]]

    def DialogController(self):
        if self.Dialogs.CurrentDialogId == None and not self.Dialogs.DialogPlay() and self.NextDialog != None:
            self.Dialogs.CurrentDialogId = self.NextDialog
            self.NextDialog = None

        if self.Dialogs.CurrentAni not in [None, ""]:
            self.Anis[self.Dialogs.CurrentAni][0].State = self.Dialogs.AniMovement

    def update(self):
        for List in self.Pics.values():
            for Id in List:
                self.Images[Id][-3] = False
        self.Images[self.Pics[self.Scene][self.CurrentId]][-3] = True
        if self.PlayBtn.update():
            self.PlayBtn.Active, self.StopBtn.Active = False, True
            self.NextDialog = self.PicsDialogs[self.Pics[self.Scene][self.CurrentId]]
            self.AutoNext = True
            self.First = True
        if self.StopBtn.update():
            self.PlayBtn.Active, self.StopBtn.Active = True, False
            self.Sounds.Channels["1"].stop()
            self.NextDialog = None
        
        Change = False
        self.Buttons["BtnSCHELPNext"].Disabled = self.Buttons["BtnSCHELPBack"].Disabled = False
        if self.CurrentId == 0: self.Buttons["BtnSCHELPBack"].Disabled = True
        if self.CurrentId == len(self.Pics[self.Scene]) - 1: self.Buttons["BtnSCHELPNext"].Disabled = True
        if not self.First and self.StopBtn.Active and not self.Sounds.Channels["1"].get_busy() and not self.Buttons["BtnSCHELPNext"].Disabled and self.AutoNext: 
            self.CurrentId, Change = self.CurrentId + 1, True
        if self.Buttons["BtnSCHELPNext"].update(): self.CurrentId, Change, self.AutoNext = self.CurrentId + 1, True, False
        if self.Buttons["BtnSCHELPBack"].update(): self.CurrentId, Change, self.AutoNext = self.CurrentId - 1, True, False
        if Change: self.ChangeDialog()
        
        if self.NextDialog == None and not self.Sounds.Channels["1"].get_busy(): 
            self.PlayBtn.Active, self.StopBtn.Active = True, False
        self.DialogController()
        self.First = False
        if self.Buttons["BtnSCHELPCross"].update():
            self.PlayBtn.Active, self.StopBtn.Active = True, False
            self.CurrentId = 0
            self.NextDialog = None
            self.First = False
            self.AutoNext = False
            self.Sounds.Channels["1"].stop()
            if self.Scene == "SC_01":
                self.app.ScenesClassesDict["SC_01"].TPause = pg.time.get_ticks() - self.app.ScenesClassesDict["SC_01"].STicks
            self.app.ChangeScene(self.Scene, False)

class SC_EXIT(Scene):
    def __init__(self, app):
        self.app = app
        super().__init__(self.app)
        self.First = True
        self.Start()

    def Start(self):
        self.Sounds.Channels["1"].stop()
        self.NextDialog = "TKSCEXIT000"
        self.State = "Choice"
        self.Set = False

    def update(self):
        if self.First:
            self.Start()
            self.First = False
        
        if self.State == "Choice":
            if self.Buttons["BtnSCEXITYes"].update(): self.State = "Yes"
            if self.Buttons["BtnSCEXITNo"].update(): self.State = "No"

        if self.State == "Yes": 
            if not self.Set:
                self.Sounds.Channels["1"].stop()
                self.NextDialog = "TKSCEXIT001"
                self.Set = True
            elif not self.Dialogs.DialogPlay(): 
                self.First = True
                self.app.ExitFromApp()

        if self.State == "No":
            if not self.Set:
                self.Sounds.Channels["1"].stop()
                self.NextDialog = "TKSCEXIT002"
                self.Set = True
            elif not self.Dialogs.DialogPlay(): 
                self.First = True
                self.app.ChangeScene("SC_02")

        if self.Dialogs.CurrentDialogId == None and not self.Dialogs.DialogPlay() and self.NextDialog != None:
            self.Dialogs.CurrentDialogId = self.NextDialog
            self.NextDialog = None

        if self.Dialogs.CurrentAni not in [None, ""]:
            self.Anis[self.Dialogs.CurrentAni][0].State = self.Dialogs.AniMovement