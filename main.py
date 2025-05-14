import pygame as pg
from settings import *
from scenes import Scenes
import sys
from SceneClasses import *
from Cursors import *
import getpass
import os
import pickle
from datetime import datetime
import os

class App:
    def __init__(self, s, clock):
        self.s = pg.Surface((1920, 1080), flags=pg.SRCALPHA)
        self.clock = clock
        self.CursorSurface = self.s.copy()
        self.PutPrev = self.s.copy()
        self.Surf = s
        pg.mouse.set_relative_mode(True)
        self.AnsLoad = False
        self.Scenes = Scenes(self)
        self.MousePos = pg.math.Vector2()
        self.Sensitivity = float(ConfigProjectAttribs["sensitivity"])
        self.MaybeSceneChange = None
        self.MaybeCreatePutPrev = True
        self.Scenes.Sounds.CreateChannel(2)
        self.dt = 0
        self.InitClasses()
        self.Change = True
        self.OldScene = None
        self.Space = True
        self.Click = True
        self.F6 = True

    def InitClasses(self):
        self.CurMessage = None
        LoadSave(self)
        self.CsrNormal = CsrNormal(self)
        self.ScenesClassesDict = {"SC_01": SC_01(self), "SC_PAUSE": SC_PAUSE(self), "SC_SETTINGS": SC_SETTINGS(self), "SC_GAMEOVER": SC_GAMEOVER(self), "SC_02": SC_02(self),
                                  "SC_TITELS": SC_TITELS(self), "SC_INTRO": SC_INTRO(self), "SC_HELP": SC_HELP(self), "SC_EXIT": SC_EXIT(self)}
        
    def ChangeScene(self, Scene, CreatePutPrev=True):
        self.MaybeCreatePutPrev = CreatePutPrev
        self.MaybeSceneChange = Scene
        pg.mixer.Channel(1).stop()
        self.Scenes.Dialogs.update()
        self.Change = True
        self.Scenes.ButtonsCollide.clear()

    def CreatePutPrev(self):
        if self.MaybeCreatePutPrev:
            self.PutPrev = self.s.copy()
        else: self.MaybeCreatePutPrev = True

    def ChangeRes(self, Res):
        self.Surf = pg.Surface(Res)

    def SaveScreenshot(self, Surf):
        if not os.path.exists("SCREENSHOTS"): os.mkdir("SCREENSHOTS")
        pg.image.save(Surf, f"SCREENSHOTS/{str(datetime.now()).replace(":", "-")}.png")

    def update(self):
        if not int(self.clock.get_fps()) == 0:
            keys = pg.key.get_pressed()
            if keys[pg.K_SPACE] and self.Space: 
                self.Scenes.Sounds.Channels["1"].stop()
                self.Space = False
            if not keys[pg.K_SPACE]: self.Space = True
            Rel = pg.mouse.get_rel()
            self.MousePos += pg.math.Vector2(Rel[0] * self.Sensitivity, Rel[1] * self.Sensitivity)
            self.MousePos.x = max(0, min(self.MousePos.x, self.s.get_width()))
            self.MousePos.y = max(0, min(self.MousePos.y, self.s.get_height()))
            self.Scenes.MusicController()
            self.Scenes.Sounds.update()
            for NeedRun in self.Scenes.NeedRun: NeedRun.run()
            if self.Change:
                for Scene, Start in self.Scenes.Starts.items():
                    if self.Scenes.CurrentScene == Scene:
                        if self.OldScene in Start: self.Scenes.CommandLists[Start[self.OldScene]].run()
                        if "All" in Start: self.Scenes.CommandLists[Start["All"]].run()
            self.Change = False
            if self.Scenes.CurrentScene in self.Scenes.Interactions:
                for Name, Interaction in self.Scenes.Interactions[self.Scenes.CurrentScene].items():
                    if Interaction[2]:
                        Rects = []
                        if Interaction[0] in self.Scenes.Images: 
                            Img = self.Scenes.Images[Interaction[0]]
                            Rects = [pg.Rect(Img[2].x, Img[2].y, *Img[0].get_size())]
                        elif Interaction[0] in self.Scenes.AnisDict:
                            Ani = self.Scenes.AnisDict[Interaction[0]][0]
                            State = Ani.State
                            if State == "Standart": 
                                Static = self.Scenes.Statics[Interaction[0]][Ani.GetStaticFunc()]
                                Rects = [pg.Rect(*Ani.StandartPos + Static["Offset"], *Static["Image"].get_size())]
                            else:
                                Movement = Ani.Movements[State][0]
                                Img = Movement.Images[Movement.ImageIndex]
                                Rects = [pg.Rect(*Ani.StandartPos + Movement.Offset, *Img.get_size())]
                        elif Interaction[0] in self.Scenes.GridObjects:
                            GD = self.Scenes.GridObjects[Interaction[0]]
                            for Coord, Value in GD[0].items():
                                if Value != "None":
                                    PieceCoord = Coord.split("_")
                                    PieceCoord = vec2(int(PieceCoord[1]) * GD[-4], int(PieceCoord[0]) * GD[-4])
                                    Rects.append(pg.Rect(GD[2].x + PieceCoord.x, GD[2].y + PieceCoord.y, GD[-4], GD[-4]))
                        else: raise ValueError(f"Interaction '{Name}' have incorrect object!!!!!!!!!!!!!!!!!!!!!")
                        for Rect in Rects:
                            if Interaction[0] in self.Scenes.DrawWithOffestIds: 
                                Rect.x -= self.Scenes.Offset.x
                                Rect.y -= self.Scenes.Offset.y
                            if Rect.collidepoint(self.MousePos) and pg.mouse.get_pressed()[0] and self.Click:
                                self.Scenes.CommandLists[Interaction[1]].run()
                                self.Click = False
            if not pg.mouse.get_pressed()[0]: self.Click = True
            self.Scenes.Dialogs.update()
            if self.Scenes.CurrentScene in self.ScenesClassesDict: self.ScenesClassesDict[self.Scenes.CurrentScene].update()
            if keys[pg.K_F6] and self.F6:
                # self.SaveScreenshot(pg.transform.scale(self.s, (Ow, Oh)))
                self.F6 = False
            if not keys[pg.K_F6]: self.F6 = True
            self.CurMessage = None
            self.Scenes.Cursors[self.Scenes.CurrentCursor].update()
            self.Scenes.CurrentCursor = "CsrNormal"
            for Button in self.Scenes.ButtonsCollide:
                self.Scenes.CurrentCursor = Button.Cursor
            if self.Scenes.CurrentCursor == "CsrNormal": self.CsrNormal.update()
            try: CFrameObj.update()
            except: pass


    def draw(self):
        if not int(self.clock.get_fps()) == 0:
            self.CursorSurface.fill((255, 255, 255, 0))
            if self.MaybeSceneChange == None:
                self.s.fill("black")
                self.Scenes.DrawImages()
            self.Scenes.Dialogs.draw()
            self.Scenes.Cursors[self.Scenes.CurrentCursor].draw()
            if not self.MaybeSceneChange == None:
                self.CreatePutPrev()
                self.OldScene = self.Scenes.CurrentScene
                self.Scenes.CurrentScene = self.MaybeSceneChange
                self.MaybeSceneChange = None
            self.Surf.blit(pg.transform.scale(self.s, (Ow, Oh)), (XLOffset, YUOffset))
            try: CFrameObj.draw(self.Surf, "Tahoma", self.Scenes.Fonts.WriteFont, ConfigProjectAttribs["title"])
            except: pass
            if self.Scenes.CurrentScene != "SC_INTRO": self.Surf.blit(pg.transform.scale(self.CursorSurface, self.Surf.get_size()), (0, 0))

    def ExitFromApp(self):
        Path = f"C:/Users/{getpass.getuser()}/Documents"
        FullPath = f"C:/Users/{getpass.getuser()}/Documents/Strast Studio/{ConfigProjectAttribs["title"]}"
        Data["MV"] = int(self.ScenesClassesDict["SC_SETTINGS"].ScrMV.update())
        Data["SV"] = int(self.Scenes.Sounds.SoundVolume * 100)
        try:
            if not os.path.exists(f"{Path}"): os.mkdir(f"{Path}")
            if not os.path.exists(f"{Path}/Strast Studio"): os.mkdir(f"{Path}/Strast Studio")
            if not os.path.exists(f"{Path}/Strast Studio/{ConfigProjectAttribs["title"]}"): os.mkdir(f"{Path}/Strast Studio/{ConfigProjectAttribs["title"]}")
        except FileExistsError:
            pass
        with open(f"{FullPath}/Save.dat", "wb") as file:
            # file.write(str(Data))
            pickle.dump(str(Data), file)
        sys.exit()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.ExitFromApp()

    def run(self):
        while True:
            self.dt = self.clock.tick(165) / 10
            self.events()
            self.update()
            self.draw()
            pg.display.update()



if __name__ == "__main__":
    app = App(s, clock)
    app.run()