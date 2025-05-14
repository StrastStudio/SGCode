from scenes import Timer
from scenes import AniObject, MovementObject
from copy import deepcopy

class Scene:
    def __init__(self, app):
        self.app = app
        self.Scenes = self.app.Scenes
        self.Images = self.Scenes.Images
        self.Anis = self.Scenes.AnisDict
        self.Statics = self.Scenes.Statics
        self.AddImages = self.Scenes.AddImages
        self.AddAnis = self.Scenes.AddAnis
        self.Texts = self.Scenes.Texts
        self.Offset = self.Scenes.Offset
        self.DrawWithOffestIds = self.Scenes.DrawWithOffestIds
        self.CommandLists = self.Scenes.CommandLists
        self.Scrollers = self.Scenes.Scrollers
        self.Dialogs = self.Scenes.Dialogs
        self.Buttons = self.Scenes.Buttons
        self.Fonts = self.Scenes.Fonts
        self.Sounds = self.Scenes.Sounds
        self.TextFields = self.Scenes.TextFields
        self.GridObjects = self.Scenes.GridObjects
        self.Configs = self.Scenes.Configs
        self.Interactions = self.Scenes.Interactions
        self.ProgressBars = self.Scenes.ProgressBars

    def UpdText(self, Id, Text, Color=(255, 255, 255)):
        WriteFontRet = self.Fonts.WriteFont(self.Texts[Id][-6], Text, Color)
        self.Texts[Id][0] = WriteFontRet[0]
        self.Texts[Id][-7] = Text

    def ChangePosImg(self, Id, X=False, Y=False, Z=False):
        if X: self.Images[Id][2].x = X
        if Y: self.Images[Id][2].y = Y
        if Z: self.Images[Id][2].z = Z

    def ChangePosText(self, Id, X=False, Y=False, Z=False):
        if X: self.Texts[Id][2].x = X
        if Y: self.Texts[Id][2].y = Y
        if Z: self.Texts[Id][2].z = Z

    def CopyAni(self, OriginalList, Id):
        OAni = OriginalList[0]
        AniScene = deepcopy(OriginalList[1])
        Movements = {}
        for Id, Movement in OAni.Movements.items():
            OMv = Movement[0]
            Movements[Id] = [MovementObject(self.app, OAni.StandartPos, None, None, None, OMv.Speed, False, None, None, None, OAni.Offset.x, OAni.Offset.y, False, False, None), deepcopy(Movement[1])]
            Movements[Id][0].Images = deepcopy(OMv.Images)
        Copy = [AniObject(self.app, Movements, OAni.State, OAni.StandartPos, OAni.Id, AniScene), AniScene, OriginalList[2].copy(), deepcopy(OriginalList[3]), OriginalList[-3], deepcopy(OriginalList[-2]), "Animation"]
        Copy[0].AniFunc = OAni.AniFunc
        return Copy