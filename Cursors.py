from settings import *
from Scene import *

class CsrNormal(Scene):
    def __init__(self, app):
        self.app = app
        super().__init__(self.app)
        self.Ani = self.Anis["ACsrNormal"]
        self.Ani[0].AniFunc = self.AniDraw
        self.AniStatics = self.Statics["ACsrNormal"]
        self.AniStaticDef = self.AniStatics["SCsrNormalDef"]
        self.CursorTimer = Timer(5000, self.CursorTimerFunc)
        self.Stop = False
        self.First = True
        
    def CursorTimerFunc(self):
        self.Ani[0].State = "MVCsrNormalDef"

    def Toggle(self):
        self.Ani[-4] = False
        self.Ani[0].Movements["ACsrNormalDef"][0].ImageIndex = 0
        self.Ani[0].State = "Standart"
        self.First = True

    def AniDraw(self, Pos):
        self.app.CursorSurface.blit(self.AniStaticDef["Image"], Pos + self.AniStaticDef["Offset"] + self.Ani[0].Offset)

    def CursorTimerReset(self):
        self.CursorTimer.Deactivate()
        self.CursorTimer.Activate()

    def MoveStop(self):
        self.Ani[0].State = "Standart"
        self.CursorTimer.Activate()        

    def update(self):
        self.CursorTimer.update()
        if self.First:
            self.OldPos = self.app.MousePos.copy()
            if not self.CursorTimer.Active: self.CursorTimer.Activate()
            self.First = False
        self.Ani[-4] = True
        if self.app.MousePos != self.OldPos: self.CursorTimerReset()
        if self.Ani[0].MovementStop: self.MoveStop()
        self.Ani[0].update()
        if self.Ani[0].MovementStop: self.MoveStop()
        self.OldPos = self.app.MousePos.copy()