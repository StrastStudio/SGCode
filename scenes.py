from settings import *
import json
import os
from video import Video
import numpy as np
from copy import deepcopy
from ast import literal_eval
from Resources import *
from random import choice

ScenesDictFiles = ResScenesDictFiles
Rects = ResRects

class Scenes:
    def __init__(self, app):
        self.app = app
        self.Sounds = Sounds()
        self.ScenesPutPrev = []
        self.Scenes = self.LoadScenes()
        self.AppendSounds()
        self.Dialogs = Dialogs(self)
        self.ButtonsFromScenesList = self.LoadButtonsFromScenes()
        self.ButtonsCollide = []
        self.CurrentScene = ConfigProjectAttribs["start"]
        self.ButtonsImagesList = {}
        self.CursorImages = {}
        self.CurrentCursor = "CsrNormal"
        self.Images = self.LoadImages()
        self.AnisDict = {}
        self.Statics = self.LoadStatics()
        self.LoadAnis()
        self.Fonts = Fonts()
        self.AddAnis = {}
        self.AddImages = {}
        self.AddMaterials()
        self.PlayMusicScene = self.CurrentScene
        self.LoadVideos()
        self.Buttons = {}
        self.CreateButtons()
        self.LoadTexts()
        self.ProcessingProgressBars()
        self.ProcessingTextFields()
        self.LoadCursors()
        self.ScrollerPressed = None
        self.LoadScrollers()
        self.LoadCommandLists()
        self.LoadGribObjects()
        self.LoadStarts()
        self.LoadInteractions()
        self.NeedRun = []
        self.Offset = vec2()
        self.DrawWithOffestIds = []
        self.DrawPutPrev = True
        self.Configs = {}

    def LoadInteractions(self):
        self.Interactions = {}
        for Scene in self.Scenes.values():
            SceneName = Scene.attrib["id"]
            self.Interactions[SceneName] = {}
            Interactions = Scene.findall("INTERACTION")
            if Interactions != []:
                for Interaction in Interactions:
                    InteractionAttrib = Interaction.attrib
                    self.Interactions[SceneName][InteractionAttrib["id"]] = [InteractionAttrib["Object"], InteractionAttrib["CLId"], True]

    def LoadStarts(self):
        self.Starts = {}
        for Scene in self.Scenes.values():
            SceneName = Scene.attrib["id"]
            Starts = Scene.findall("START")
            if Starts != []:
                for Start in Starts:
                    StartAttribs = Start.attrib
                    SceneNameStart = StartAttribs["Sc"]
                    if SceneNameStart == SceneName: SceneNameStart = "All"
                    if SceneName not in self.Starts: self.Starts[SceneName] = {}
                    self.Starts[SceneName] = {SceneNameStart: StartAttribs["CLId"]}

    def LoadGribObjects(self):
        self.GridObjects = {}
        for Scene in self.Scenes.values():
            GridObjects = Scene.findall("GRIDOBJECT")
            if GridObjects != []:
                for GridObject in GridObjects:
                    Grid = {}
                    GridObjectAttrib = GridObject.attrib
                    Rows = int(GridObjectAttrib["rows"])
                    Cols = int(GridObjectAttrib["cols"])
                    for Col in range(Cols):
                        for Row in range(Rows):
                            Name = f"{Col}_{Row}"
                            Grid[Name] = "0"
                    for Piece in GridObject.findall("PIECE"):
                        Attrib = Piece.attrib
                        match Attrib["method"]:
                            case "0":
                                Name = f"{Attrib["col"]}_{Attrib["row"]}"
                                Grid[Name] = Attrib["value"]
                            case "1":
                                From = vec2(int(Attrib["Frow"]), int(Attrib["Fcol"]))
                                To = vec2(int(Attrib["Trow"]) + 1, int(Attrib["Tcol"]) + 1)
                                for y in range(int(From.y), int(To.y)):
                                    for x in range(int(From.x), int(To.x)):
                                        Name = f"{y}_{x}"
                                        Grid[Name] = Attrib["value"]
                    Images = {}
                    for Image in GridObject.findall("IMAGE"):
                        Attrib = Image.attrib
                        Images[Attrib["value"]] = Attrib["pic"]
                    Visible = False if "flags" in GridObjectAttrib and GridObjectAttrib["flags"] == "0" else True
                    self.GridObjects[GridObjectAttrib["id"]] = [Grid, Scene.attrib["id"], pg.math.Vector3(int(GridObjectAttrib["x"]), int(GridObjectAttrib["y"]), int(GridObjectAttrib["z"])),
                                                               Cols, Rows, Images, int(GridObjectAttrib["TileSize"]), Visible, GridObjectAttrib["id"], "GridObject"]

    def LoadCommandLists(self):
        self.CommandLists = {}
        for Scene in self.Scenes.values():
            CommandLists = Scene.findall("COMMAND_LIST")
            if CommandLists != []:
                for CommandListObj in CommandLists:
                    CommandListAttrib = CommandListObj.attrib
                    Commands = CommandListObj.findall("COMMAND")
                    CommandsDict = []
                    if Commands != []:
                        for CommandObj in Commands:
                            CommandsDict.append(CommandObj.attrib)
                    self.CommandLists[CommandListAttrib["id"]] = CommandList(self, CommandsDict)
                            

    def LoadScrollers(self):
        I = 0
        self.Scrollers = {}
        for Scene in self.Scenes.values():
            Scrollers = Scene.findall("SCROLLER")
            if Scrollers != []:
                for ScrollerObj in Scrollers:
                    ScrollerAttrib = ScrollerObj.attrib
                    Offset = vec2(0, 0)
                    if "OffsetX" in ScrollerAttrib: Offset.x = int(ScrollerAttrib["OffsetX"])
                    if "OffsetY" in ScrollerAttrib: Offset.y = int(ScrollerAttrib["OffsetY"])
                    self.Scrollers[ScrollerAttrib["id"]] = Scroller(self, ScrollerAttrib["Bg"], ScrollerAttrib["Pointer"], ScrollerAttrib["Value"], I, int(ScrollerAttrib["x"]), int(ScrollerAttrib["y"]), Offset)
                    I += 1

    def LoadVideos(self):
        self.Videos = {}
        for Scene in self.Scenes.values():
            Videos = Scene.findall("VIDEO")
            if Videos != []:
                for VideoObj in Videos:
                    VideoAttrib = VideoObj.attrib
                    self.Videos[VideoAttrib["id"]] = Video(VideoObj.attrib["file"])
                    self.Videos[VideoAttrib["id"]].volume = self.Sounds.SoundVolume
                    self.Videos[VideoAttrib["id"]].toggle_pause()

    def AppendSounds(self):
        self.Sounds.CreateChannel(1)
        self.MusicFiles = {}
        for Scene in self.Scenes.values():
            Music = Scene.findall("MUSIC")
            Sound = Scene.findall("SOUND")
            if Sound != []:
                for SoundObj in Sound:
                    SoundAttribs = SoundObj.attrib
                    File = None
                    Path = SoundAttribs["file"]
                    if SoundAttribs["file"].startswith("File: "): 
                        File = Scene.attrib["id"]
                        Path = SoundAttribs["file"].replace("File: ", "")
                    self.Sounds.LoadSound(Path, SoundAttribs["id"], File)
            if Music != []: self.MusicFiles[Scene.attrib["id"]] = Music[0].attrib["file"]

    def MusicController(self):
        if self.PlayMusicScene != self.CurrentScene or not pg.mixer.music.get_busy():
            try: 
                self.MusicFiles[self.CurrentScene]
                MStop()
                LAPMusic(self.MusicFiles[self.CurrentScene], self)
                self.PlayMusicScene = self.CurrentScene
            except KeyError: pass

    def LoadStatics(self):
        StaticImages = ResStaticImages
        
        StaticDict = {}
        for Scene in self.Scenes.values():
            for Ani in Scene.findall("ANI"):
                Name = Ani.attrib["id"]
                StaticDict[Name] = {}
                for Static in Ani.findall("STATIC"):
                    StaticDict[Name][Static.attrib["id"]] = {}
                    StaticDict[Name][Static.attrib["id"]]["Image"] = StaticImages[Static.attrib["id"]]
                    StaticDict[Name][Static.attrib["id"]]["Offset"] = vec2(0, 0)
                    if "y" in Static.attrib: StaticDict[Name][Static.attrib["id"]]["Offset"].y = int(Static.attrib["y"])
                    if "x" in Static.attrib: StaticDict[Name][Static.attrib["id"]]["Offset"].x = int(Static.attrib["x"])
                    StaticDict[Name][Static.attrib["id"]]["Id"] = Static.attrib["id"]
        return StaticDict
    
    def ProcessingTextFields(self):
        self.TextFields = {}
        for Scene in self.Scenes.values():
            TextFields = Scene.findall("TEXTFIELD")
            if TextFields != []:
                for TextFieldsObject in TextFields:
                    TextFieldsAttrib = TextFieldsObject.attrib
                    self.TextFields[TextFieldsAttrib["id"]] = TextField(self.app, int(TextFieldsAttrib["x"]), int(TextFieldsAttrib["y"]), int(TextFieldsAttrib["w"]), int(TextFieldsAttrib["h"]), int(TextFieldsAttrib["z"]),
                                                                        int(TextFieldsAttrib["limit"]), TextFieldsAttrib["font"], int(TextFieldsAttrib["active"]), Scene.attrib["id"])
    
    def LoadButtonsFromScenes(self):
        Buttons = {}
        for Scene in self.Scenes.values():
            Buttons[Scene.attrib["id"]] = Scene.findall("BUTTON")
        return Buttons

    def LoadScenes(self):
        Scenes = {}
        ScenesFromConfig = Config.findall("SCENE")
        for Scene in ScenesFromConfig:
            SceneId = SceneLoad = None
            SceneAttribs = Scene.attrib
            SceneId = SceneAttribs["id"]
            SceneLoad = ReadXmlFile(SceneAttribs["file"])
            Scenes[SceneId] = SceneLoad
            try:
                if int(SceneLoad.attrib["put_prev"]) == 1: self.ScenesPutPrev.append(SceneId)
            except: pass
        return Scenes
    
    def LoadCursors(self):
        Cursors = ResCursors

        self.ProcessingCursors(Cursors)

    def ProcessingCursors(self, CursorsList):
        self.Cursors = {}
        for Scene in self.Scenes.values():
            Cursors = Scene.findall("CURSOR")
            if Cursors != []:
                for CursorsObject in Cursors:
                    CursorsAttrib = CursorsObject.attrib
                    Offset = vec2()
                    if "offset" in CursorsAttrib: Offset = CursorsAttrib["offset"].split()
                    Offset = vec2(int(Offset[0]), int(Offset[1]))
                    try: 
                        self.Cursors[CursorsAttrib["id"]] = Cursor(self.app, self, Offset, Move=CursorsAttrib["mov"])
                    except:
                        self.Cursors[CursorsAttrib["id"]] = Cursor(self.app, self, Offset, CursorsList[CursorsAttrib["id"]])

    def LoadImages(self):
        Images = ResImages

        Images = self.ProcessingImages(Images)
        
        return Images

    def AddMaterials(self):
        for Scene in self.Scenes.values():
            AddAnis = Scene.findall("ADDANI")
            AddImages = Scene.findall("ADDPICTURE")
            for AddAniObject in AddAnis:
                AddAniObjectAttribs = AddAniObject.attrib
                if not AddAniObjectAttribs["id"] in self.AddAnis:
                    self.AddAnis[AddAniObjectAttribs["id"]] = {Scene.attrib["id"]: vec2(int(AddAniObjectAttribs["x"]), int(AddAniObjectAttribs["y"]))}
                else:
                    self.AddAnis[AddAniObjectAttribs["id"]][Scene.attrib["id"]] = vec2(int(AddAniObjectAttribs["x"]), int(AddAniObjectAttribs["y"]))
                self.AnisDict[AddAniObjectAttribs["id"]][0].Poses[Scene.attrib["id"]] = vec2(int(AddAniObjectAttribs["x"]), int(AddAniObjectAttribs["y"]))
            for AddImageObject in AddImages:
                AddImageObjectAttribs = AddImageObject.attrib
                if not AddImageObjectAttribs["id"] in self.AddImages:
                    self.AddImages[AddImageObjectAttribs["id"]] = {Scene.attrib["id"]: vec2(int(AddImageObjectAttribs["x"]), int(AddImageObjectAttribs["y"]))}
                else:
                    self.AddImages[AddImageObjectAttribs["id"]][Scene.attrib["id"]] = vec2(int(AddImageObjectAttribs["x"]), int(AddImageObjectAttribs["y"]))
                
    def LoadTexts(self):
        self.Texts = {}
        for Scene in self.Scenes.values():
            Texts = Scene.findall("TEXT")
            if len(Texts) != 0:
                for Text in Texts:
                    Attribs = Text.attrib
                    Align = None
                    if "align" in Attribs: Align = Attribs["align"]
                    if int(Attribs["ttf"]) == 1:
                        ColorSplit = Attribs["color"].split()
                        WriteFontRet = self.Fonts.WriteFont(Attribs["font"], Attribs["text"], (int(ColorSplit[0]), int(ColorSplit[1]), int(ColorSplit[2])), Align=Align)
                    else: WriteFontRet = self.Fonts.WriteFont(Attribs["font"], Attribs["text"], Align=Align)
                    Rendered = WriteFontRet[0]
                    Align = WriteFontRet[1]
                    Visible = False if "flags" in Attribs and Attribs["flags"] == "0" else True
                    self.Texts[Attribs["id"]] = [Rendered, Scene.attrib["id"], pg.math.Vector3(int(Attribs["x"]), int(Attribs["y"]), int(Attribs["z"])), Attribs["text"], Attribs["font"], Align, "Text", Visible, Attribs["id"], "Image"]
            
    def LoadAnis(self):
        Anis = ResAnis

        self.ProcessingAnis(Anis)

    def ProcessingAnis(self, Anis):
        if len(Anis) == 0: return {}
        else: 
            ScenesAnisPos = {}
            Movements = {}
            Phases = {}
            for Scene in self.Scenes.values():
                for Ani in Scene.findall("ANI"):
                    AnisAtrribs = Ani.attrib
                    ScenesAnisPos[AnisAtrribs["id"]] = pg.math.Vector3(int(AnisAtrribs["x"]), int(AnisAtrribs["y"]), int(AnisAtrribs["z"]))
                    Movements[AnisAtrribs["id"]] = {}
                    Phases[AnisAtrribs["id"]] = {}
                    for Movement in Ani.findall("MOVEMENT"):
                        MovementAttribs = Movement.attrib
                        if "AnsLoad" in MovementAttribs and MovementAttribs["AnsLoad"] == "1" and self.app.AnsLoad == False: continue
                        Phases[AnisAtrribs["id"]][MovementAttribs["id"]] = Movement.findall("PHASE")
                        try: 
                            File = MovementAttribs["file"]
                            Folder = None
                            Prefix = MovementAttribs["prefix"] if "prefix" in MovementAttribs else None
                        except: 
                            File = None
                            Folder = MovementAttribs["folder"]
                            Prefix = MovementAttribs["prefix"]
                        PrevX = PrevY = 0
                        if "PrevX" in MovementAttribs: PrevX = int(MovementAttribs["PrevX"])
                        if "PrevY" in MovementAttribs: PrevY = int(MovementAttribs["PrevY"])
                        PrefMethod = True if "PrefMethod" in MovementAttribs and MovementAttribs["PrefMethod"] == "1" else False
                        Frames = None
                        if "Frames" in MovementAttribs: Frames = int(MovementAttribs["Frames"]) + 1
                        Movements[AnisAtrribs["id"]][MovementAttribs["id"]] = [MovementObject(self.app, ScenesAnisPos[AnisAtrribs["id"]], Folder, Prefix, File, float(MovementAttribs["speed"]), False, Scene.attrib["id"], AnisAtrribs["id"], MovementAttribs["id"], PrevX, PrevY, True, PrefMethod, Frames), MovementAttribs["id"]]
            List = []
            for Ani in Anis:
                List.append([AniObject(self.app, Movements[Ani[0]], Ani[2], ScenesAnisPos[Ani[0]], Ani[0], Ani[1]), Ani[1], ScenesAnisPos[Ani[0]], True, Phases[Ani[0]], Ani[0], "Animation"])
                self.AnisDict[Ani[0]] = List[-1]

    def ProcessingProgressBars(self):
        self.ProgressBars = {}
        for Scene in self.Scenes.values():
            ProgressBars = Scene.findall("PROGRESSBAR")
            if ProgressBars != []:
                for ProgressBarObject in ProgressBars:
                    ProgressBarAttrib = ProgressBarObject.attrib
                    self.ProgressBars[ProgressBarAttrib["id"]] = (ProgressBar(self, ProgressBarAttrib["FgImage"], ProgressBarAttrib["Value"]))

    def CreateButtons(self):
        for Scene in self.Scenes.values():
            Buttons = Scene.findall("BUTTON")
            if Buttons != []:
                for ButtonObj in Buttons:
                    ButtonAttrib = ButtonObj.attrib
                    TexturePass = ButtonAttrib["tex"]
                    TextureHover = ButtonAttrib["tex_hover"]
                    TexturePress = ButtonAttrib["tex_press"]
                    Cursor = ButtonAttrib["cursor"]
                    if TexturePass == "": raise ValueError("Texture pass myst exist")
                    if TextureHover == "": TextureHover = TexturePass
                    if TexturePress == "": TexturePress = TexturePass
                    SoundH = ButtonAttrib["soundH"]
                    SoundP = ButtonAttrib["soundP"]
                    SoundI = ""
                    if "soundI" in ButtonAttrib: SoundI = ButtonAttrib["soundI"]
                    try: TextureDisabled = ButtonAttrib["tex_disable"]
                    except: TextureDisabled = None
                    self.Buttons[ButtonAttrib["id"]] = Button(TexturePass, TextureHover, TexturePress, self, SoundH, SoundP, Cursor, TextureDisabled, SoundI=SoundI)

    def ProcessingImages(self, Images):
        if len(Images) == 0: return []
        else: 
            VisibleList = {}
            ScenesImagesPos = {}
            for Scene in self.Scenes.values():
                for Image in Scene.findall("PICTURE"):
                    ImageAtrribs = Image.attrib
                    ScenesImagesPos[ImageAtrribs["id"]] = pg.math.Vector3(int(ImageAtrribs["x"]), int(ImageAtrribs["y"]), int(ImageAtrribs["z"]))
                    try: 
                        if int(ImageAtrribs["flags"]) == 1: VisibleList[ImageAtrribs["id"]] = True
                        if int(ImageAtrribs["flags"]) == 0: VisibleList[ImageAtrribs["id"]] = False
                    except: VisibleList[ImageAtrribs["id"]] = True
            Result = {}
            for Image in Images:
                try: 
                    if Image[3] == "Csr": 
                        self.CursorImages[Image[0]] = Image[2]
                except IndexError: Result[Image[0]] = [Image[2], Image[1], ScenesImagesPos[Image[0]], VisibleList[Image[0]], Image[0], "Image"]
            return Result
        
    def DrawImages(self):
        Images = []
        if self.Images != Images:
            for Image in self.Images.values():
                Images.append(Image)
        for Ani in self.AnisDict.values():
            Images.append(Ani)
        for Text in self.Texts.values():
            Images.append(Text)
        for Id, TextFieldObject in self.TextFields.items():
            Images.append((TextFieldObject, TextFieldObject.Scene, TextFieldObject.Pos, Id, "TextField"))
        for Grid in self.GridObjects.values():
            Images.append(Grid)
        if self.CurrentScene in self.ScenesPutPrev and self.DrawPutPrev: self.app.s.blit(self.app.PutPrev, (0, 0))
        if Images != []:
            Images = sorted(Images, key=lambda obj: obj[2].z, reverse=True)
            for Image in Images:
                DrawWithOffset = True if Image[-2] in self.DrawWithOffestIds else False
                OffsetImages = self.Offset if DrawWithOffset else vec2()
                Visible = True
                RenderText = False
                if Image[-1] == "Image": Visible = Image[-3]
                if Image[-1] == "GridObject": Visible = Image[-3]
                if Image[-4] == "Text": RenderText = True
                elif Image[-1] == "Animation": Visible = Image[-4]
                if Visible:
                    if not Image[1] == self.CurrentScene or (Image[-1] == "Animation" and Image[0].CursorM != None):
                        try:
                            if Image[-1] == "Animation" and self.CurrentScene in self.AddAnis[Image[-2]]: Image[0].draw(OffsetImages)
                            if Image[-1] == "Image" and self.CurrentScene in self.AddImages[Image[-2]]:
                                self.app.s.blit(Image[0], (self.AddImages[Image[-2]][self.CurrentScene].x + OffsetImages.x, self.AddImages[Image[-2]][self.CurrentScene].y + OffsetImages.y))
                        except KeyError: pass
                        if Image[-1] == "Animation" and Image[0].CursorM != None: Image[0].draw(OffsetImages)
                    else:
                        if Image[-1] == "Image": 
                            if not RenderText: self.app.s.blit(Image[0], (Image[2].x - OffsetImages.x, Image[2].y - OffsetImages.y))
                            else: 
                                Align = Image[-5]
                                Offset = vec2(0, 0)
                                if Align == "CENTER":
                                    Offset.x = Image[0].get_width() // 2
                                    Offset.y = Image[0].get_height() // 2
                                if Align == "CENTERX": Offset.x = Image[0].get_width() // 2
                                if Align == "CENTERY": Offset.y = Image[0].get_height() // 2
                                if Align == "RIGHT": Offset.x = Image[0].get_width()
                                if Align == "RIGHTBOTTOM": 
                                    Offset.x = Image[0].get_width()
                                    Offset.y = Image[0].get_height()
                                self.app.s.blit(Image[0], (Image[2].x - Offset.x, Image[2].y - Offset.y))
                        if Image[-1] in ["Animation", "TextField"]: Image[0].draw(OffsetImages)
                        if Image[-1] == "GridObject":
                            for Cords, Value in Image[0].items():
                                if Value != "None":
                                    Col, Row = Cords.split("_")
                                    Col, Row = int(Col), int(Row)
                                    TileSize = Image[-4]
                                    StartPos = vec2(Image[2].x + Row * TileSize, Image[2].y + Col * TileSize)
                                    if Value in Image[-5]:
                                        self.app.s.blit(self.Images[Image[-5][Value]][0], StartPos)
                                    else:
                                        pg.draw.rect(self.app.s, "white", (*StartPos, TileSize, TileSize))
                                        pg.draw.line(self.app.s, "black", StartPos, (StartPos.x, StartPos.y + TileSize))
                                        pg.draw.line(self.app.s, "black", StartPos, (StartPos.x + TileSize, StartPos.y))
                                        pg.draw.line(self.app.s, "black", (StartPos.x + TileSize, StartPos.y), (StartPos.x + TileSize, StartPos.y + TileSize))
                                        pg.draw.line(self.app.s, "black", (StartPos.x, StartPos.y + TileSize), (StartPos.x + TileSize, StartPos.y + TileSize))

class Fonts:
    def __init__(self):
        self.CreaingChars()
        self.Fonts = LoadFonts(self.LoadFontFromTtf, self.LoadFont)

    def CreaingChars(self):
        self.Chars = {}
        try:
            with open("FONTS/FontChars.json") as file:
                Chars = json.load(file)
            for Char in Chars["Chars"]:
                self.Chars[str(Char[0])] = Char[1]
        except FileNotFoundError: pass

    def LoadFontFromTtf(self, Name, Size):
        return {0: "Ttf", 1: pg.font.Font(Name, Size)}

    def LoadFont(self, Name):
        FontFromXml = ReadXmlFile(f"{Name}")
        if FontFromXml.attrib["texture"].split(".")[-1] == "eft": Texture = self.GetSurfFromNl(np.load(f"{FontFromXml.attrib["texture"]}"))
        else: Texture = pg.image.load(f"{FontFromXml.attrib["texture"]}").convert_alpha()
        CharsList = FontFromXml.findall("Char")
        Chars = {0: "File"}
        for Char in CharsList:
            CharAttribs = Char.attrib
            Id = CharAttribs["id"]
            if Id in list(self.Chars.keys()): Id = self.Chars[Id]
            Id = int(Id)
            XAdv = 0
            if "xadvanced" in CharAttribs: XAdv = int(CharAttribs["xadvanced"])
            Chars[chr(Id)] = [Texture.subsurface(int(CharAttribs["x"]), int(CharAttribs["y"]), int(CharAttribs["width"]), int(CharAttribs["height"])), int(CharAttribs["xoffset"]), int(CharAttribs["yoffset"]), XAdv]
        return Chars
    
    def GetSurfFromNl(self, Nl):
        Img = pg.Surface((len(Nl["Image"]), len(Nl["Image"][0])), flags=pg.SRCALPHA)
        pg.surfarray.array_to_surface(Img, Nl["Image"])
        return Img
    
    def WriteFont(self, Font, Text, Color=None, Align=None):
        if self.Fonts[Font][0] == "File":
            W = H = 0
            OffsetX = 0
            OffsetY = 0
            for Letter in Text:
                Img = self.Fonts[Font][Letter]
                W += Img[0].get_width() + Img[1] + Img[3]
                OffsetX = Img[1]
                if Img[2] < 0 and abs(Img[2]) > OffsetY:
                    OffsetY = abs(Img[2])
                if H < Img[0].get_height() + Img[2]: H = Img[0].get_height() + Img[2]
            W -= OffsetX
            Surface = pg.Surface((W, H + OffsetY), flags=pg.SRCALPHA)
            X = 0
            for Letter in Text:
                Img = self.Fonts[Font][Letter]
                if X == 0: X -= Img[1]
                Surface.blit(Img[0], (X + Img[1], Img[2] + OffsetY))
                X += Img[0].get_width() + Img[1] + Img[3]
        elif Color != None:
            Surface = self.Fonts[Font][1].render(Text, 1, Color)
        else:
            raise AttributeError("Color is invalid")
        return (Surface, Align)
    
class Button:
    def __init__(self, image, image2, image3, app, SoundH, SoundP, cursor="CsrNormal", image4=None, SoundI=""):
        self.app = app
        self.image1 = image
        self.image2 = image2
        self.image3 = image3
        self.image4 = image4
        self.image = self.image1
        if self.image2 != "": self.app.Images[self.image2][-3] = False
        if self.image3 != "": self.app.Images[self.image3][-3] = False
        Image = self.app.Images[self.image]
        self.rect = Image[0].get_rect(x=Image[2].x, y=Image[2].y)
        self.MousePressed = False
        self.soundH = SoundH
        self.soundP = SoundP
        self.soundI = SoundI
        self.soundRollPlay = False
        self.soundClickPlay = False
        self.soundInactivePlay = False
        self.Cursor = cursor
        self.Returned = False
        self.Disabled = False
        self.Active = True
    
    def SoundClickPlay(self):
        self.app.Sounds.PlaySound(self.soundP)

    def SoundInactivePlay(self):
        self.app.Sounds.PlaySound(self.soundI)

    def update(self):
        if self.Active:
            self.Returned = False
            if self.Disabled:
                if self.image4 == None: self.Disabled = False
            if not self.Disabled:
                try: self.app.Images[self.image4][-3] = False
                except: pass
            if self.rect.collidepoint(self.app.app.MousePos):
                if not self.Disabled:
                    if not self in self.app.ButtonsCollide: self.app.ButtonsCollide.append(self)
                    if self.soundH != "": 
                        if not self.soundRollPlay: 
                            self.app.Sounds.PlaySound(self.soundH)
                            self.soundRollPlay = True
                    if self.image2 != "": self.image = self.image2
                if pg.mouse.get_pressed()[0]:
                    if not self.Disabled:
                        self.MousePressed = True
                        if self.soundP:     
                            if not self.soundClickPlay: 
                                self.SoundClickPlay()
                                self.soundClickPlay = True
                        if self.image3 != "": self.image = self.image3
                    else: 
                        if self.soundI != "":
                            if not self.soundInactivePlay:
                                self.SoundInactivePlay()
                                self.soundInactivePlay = True
                if not pg.mouse.get_pressed()[0]:
                    self.soundInactivePlay = False
            if not pg.mouse.get_pressed()[0] and self.rect.collidepoint(self.app.app.MousePos) and self.MousePressed:
                if not self.Disabled:
                    self.MousePressed = False
                    self.soundClickPlay = False
                    self.soundInactivePlay = False
                    if self.image2 != "": self.image = self.image2
                    self.Returned = True
            if not self.rect.collidepoint(self.app.app.MousePos):
                if self in self.app.ButtonsCollide: self.app.ButtonsCollide.remove(self)
                self.image = self.image1
                self.MousePressed = False
                self.soundClickPlay = False
                self.soundRollPlay = False
                self.soundInactivePlay = False
            if not self.Disabled:
                if not self.image == self.image1: self.app.Images[self.image1][-3] = False
                else: self.app.Images[self.image1][-3] = True
                if self.image2 != "" and not self.image == self.image2: self.app.Images[self.image2][-3] = False
                else: self.app.Images[self.image2][-3] = True
                if self.image3 != "" and not self.image == self.image3: self.app.Images[self.image3][-3] = False
                else: self.app.Images[self.image3][-3] = True
            else:
                self.app.Images[self.image1][-3] = False
                if self.image2 != "": self.app.Images[self.image2][-3] = False
                if self.image3 != "": self.app.Images[self.image3][-3] = False
                self.app.Images[self.image4][-3] = True
            return self.Returned
            
        else:
            self.app.Images[self.image1][-3] = False
            if self.image2 != "": self.app.Images[self.image2][-3] = False
            if self.image3 != "": self.app.Images[self.image3][-3] = False
            if self.image4 != None: self.app.Images[self.image4][-3] = False
            if self in self.app.ButtonsCollide: self.app.ButtonsCollide.remove(self)
            return False

class AniObject:
    def __init__(self, app, Movements, State, Pos, Id, Scene):
        self.app = app
        self.Movements = Movements
        self.State = State
        self.Pos = vec2(Pos.x, Pos.y)
        self.MovementStop = False
        self.Id = Id
        self.First = True
        self.Poses = {Scene: self.Pos}
        self.AniFunc = None
        self.GetStaticFunc = None
        self.FrameSoundPlay = False
        self.NumberFrameSoundPlay = None
        self.MovementFrameSoundPlay = None
        self.CursorM = None
        self.CommandListRun = False
        self.OldFrame = 0
        self.CurrentMovement = None
        self.Updated = True
        self.Offset = vec2()
        self.UpdateFrame = True

    def update(self):
        if self.First:            
            if self.CursorM == None: 
                self.StandartPos = self.Poses[self.app.Scenes.CurrentScene].copy()  
                self.Poses[self.app.Scenes.CurrentScene] = self.StandartPos.copy()     
            self.Phase = self.app.Scenes.AnisDict[self.Id][-3]
            if self.Id in self.app.Scenes.AddAnis and self.app.Scenes.CurrentScene in self.app.Scenes.AddAnis[self.Id]:
                self.Poses[self.app.Scenes.CurrentScene] = self.app.Scenes.AddAnis[self.Id][self.app.Scenes.CurrentScene]
            self.First = False
        self.MovementStop = False
        if self.CursorM == None: self.Poses[self.app.Scenes.CurrentScene] = self.StandartPos.copy()
        for Movement in self.Movements.values():
            if self.State == Movement[1]:
                if self.OldFrame != int(Movement[0].ImageIndex): 
                    self.CommandListRun = False
                    self.FrameSoundPlay = False
                if self.Phase[self.State] != []:
                    for Phase in self.Phase[self.State]:
                        PhaseAttribs = Phase.attrib
                        if int(PhaseAttribs["id"]) == int(Movement[0].ImageIndex):
                            try: 
                                if not self.CommandListRun:
                                    self.app.Scenes.CommandLists[PhaseAttribs["CommandList"]].run()
                                    Movement[0].Pos = self.StandartPos.copy()
                                    self.CommandListRun = True
                            except: pass
                if self.UpdateFrame:
                    if self.State == Movement[1]:
                        # if self.MovementFrameSoundPlay == Movement and self.NumberFrameSoundPlay != int(Movement[0].ImageIndex): self.FrameSoundPlay = False
                        if self.CursorM == None: Movement[0].play(self.Poses[self.app.Scenes.CurrentScene])
                        else: Movement[0].play(self.app.MousePos)
                        if self.Phase[self.State] != []:
                            for Phase in self.Phase[self.State]:
                                PhaseAttribs = Phase.attrib
                                if int(PhaseAttribs["id"]) == int(Movement[0].ImageIndex):
                                    try: self.Poses[self.app.Scenes.CurrentScene].x += int(PhaseAttribs["x"])
                                    except: pass
                                    try: self.Poses[self.app.Scenes.CurrentScene].y += int(PhaseAttribs["y"])
                                    except: pass
                                    try: 
                                        if not self.FrameSoundPlay: 
                                            self.app.Scenes.Sounds.PlaySound(PhaseAttribs["sound"], "3")
                                            self.NumberFrameSoundPlay = int(PhaseAttribs["id"])
                                            self.AnimationFrameSoundPlay = Movement
                                            self.FrameSoundPlay = True
                                    except: pass
                        self.OldFrame = int(Movement[0].ImageIndex)
                        if Movement[0].MoveEnd() == "End": 
                            self.MovementStop = True
                            self.OldFrame = None
                        self.Updated = True

    def draw(self, Offset):
        if self.Updated:
            for Movement in self.Movements.values():
                if self.State == Movement[1]: 
                    Movement[0].draw(self.CursorM, Offset, self.Offset)
                    self.CurrentMovement = Movement
                    self.UpdateFrame = True
        else:
            if self.CurrentMovement != None: self.CurrentMovement[0].draw(self.CursorM, Offset, self.Offset)
        if self.State == "Standart":
            if self.AniFunc != None and self.CursorM == None: self.AniFunc(self.StandartPos)
            elif self.AniFunc != None: self.AniFunc(self.app.MousePos)

class MovementObject:
    def __init__(self, app, Pos, Folder, Prefix, File, Speed, Flip=False, SceneName=None, AName=None, MName=None, PrevX=0, PrevY=0, Load=True, PrefMethod=False, Frames=None):
        self.app = app
        self.Folder = Folder
        self.Pos = vec2(Pos.x, Pos.y)
        self.Speed = Speed
        self.Images = []
        self.ImageIndex = 0
        self.Temp = 0
        self.Offset = vec2(PrevX, PrevY)
        if Load:
            if File == None or File == 0:
                for Name in range(0, len(os.listdir(self.Folder))):
                    if len(str(Name)) == 1: FileName = f"00{Name}"
                    if len(str(Name)) == 2: FileName = f"0{Name}"
                    if len(str(Name)) == 3: FileName = f"{Name}"
                    img = pg.image.load(f"{self.Folder}/{Prefix}.{FileName}.png").convert_alpha()
                    if Flip: img = pg.transform.flip(img, True, False)
                    self.Images.append(img)
            else:
                if not PrefMethod:
                    Name = AName+MName+"I"
                    Images = Rects[AName][MName]
                    ImagesCopy = Images.copy()
                    del ImagesCopy["ImageRect"]
                    ImagesItems = list(ImagesCopy.items())
                    for i in ImagesItems:
                        ImageAndRectList = Images[i[0]]
                        ImageListArray = ScenesDictFiles[SceneName][Name+str(ImageAndRectList[0])]
                        ImageListSurface = Images["ImageRect"][ImageAndRectList[0]]
                        if ImageListSurface[1] == False: 
                            ImageListSurface[1] = True
                            pg.surfarray.blit_array(ImageListSurface[0], ImageListArray)
                        Image = ImageListSurface[0].subsurface(ImageAndRectList[1], ImageAndRectList[2], ImageAndRectList[3], ImageAndRectList[4])
                        self.Images.append(Image)
                else:
                    for Name in range(0, Frames):
                        if len(str(Name)) == 1: FileName = f"00{Name}"
                        if len(str(Name)) == 2: FileName = f"0{Name}"
                        if len(str(Name)) == 3: FileName = f"{Name}"
                        self.Images.append(GetSurfFromNl(SceneName, f"MV{Prefix}_{FileName}_png"))
        self.State = "Play"

    def MoveEnd(self):
        return self.State

    def play(self, Pos):
        if self.State == "End": 
            self.State = "Play"
            self.ImageIndex = 0
        self.Temp += self.Speed * self.app.dt
        if self.Temp >= 1: 
            self.Temp = 0
            self.ImageIndex += 1
        if self.ImageIndex >= len(self.Images):
            self.State = "End"
            self.ImageIndex -= 1
        self.Pos = Pos

    def draw(self, CursorM, Offset, CursorOffset):
        if CursorM == None: self.app.s.blit(self.Images[int(self.ImageIndex)], self.Pos - Offset + self.Offset)
        else: self.app.CursorSurface.blit(self.Images[int(self.ImageIndex)], self.app.MousePos + CursorOffset + self.Offset)

class Sounds:
    def __init__(self, Effect=True):
        self.MusicVolume = 0.1
        self.MusicVolumeNorm = 0.1
        self.Effect = Effect
        self.SoundVolume = 0.2
        self.Sounds = {}
        self.Channels = {}
        self.CreateChannel()
        self.CreateChannel(3)
        self.SoundsPlay = []

    def update(self):
        if self.Effect:
            for Snd in self.SoundsPlay:
                if not Snd[0].get_busy(): self.SoundsPlay.remove(Snd)
            if len(self.SoundsPlay) > 0 and self.MusicVolume > 0.05:
                self.MusicVolume -= 0.01
            elif not len(self.SoundsPlay) > 0 and self.MusicVolume < self.MusicVolumeNorm:
                self.MusicVolume += 0.01
            pg.mixer.music.set_volume(self.MusicVolume)

    def LoadSound(self, Path, IndexName, File=None):
        if File == None:
            snd = pg.mixer.Sound(Path)
            snd.set_volume(self.SoundVolume)
            self.Sounds[IndexName] = snd
        else:
            snd = pg.sndarray.make_sound(ScenesDictFiles[File+"S"][Path])
            snd.set_volume(self.SoundVolume)
            self.Sounds[IndexName] = snd
    
    def LoadMusic(self, Path):
        pg.mixer.music.load(Path)
        pg.mixer.music.set_volume(self.MusicVolume)
    
    def PlayMusic(self, Start=0, Loop=-1):
        pg.mixer.music.play(loops=Loop, start=Start)

    def PlaySound(self, IndexName, Channel=0):
        if self.SoundVolume > 0:
          self.Channels[str(Channel)].play(self.Sounds[IndexName])
          self.SoundsPlay.append([self.Channels[str(Channel)], self.Sounds[IndexName]])

    def CreateChannel(self, id=0):
        self.Channels[str(id)] = pg.mixer.Channel(id)

    def ChangeVolumeSound(self, Volume):
        for snd in self.Sounds.values(): snd.set_volume(Volume)
        self.SoundVolume = Volume
    
    def ChangeVolumeMusic(self, Volume):
        pg.mixer.music.set_volume(Volume)
        self.MusicVolume = Volume
        self.MusicVolumeNorm = Volume

def LAPMusic(path, app, start=0):
  if not pg.mixer.music.get_busy():
      app.Sounds.LoadMusic(path)
      app.Sounds.PlayMusic(Start=start)

def MStop():
  pg.mixer.music.stop()

def MPause(app):
    app.Scenes.MusicPause = True
    pg.mixer.music.pause()

def MPlay(app):
    app.Scenes.MusicPause = False
    pg.mixer.music.unpause()

class Dialogs:
    def __init__(self, app) -> None:
        self.app = app
        self.CurrentAni = None
        self.AniMovement = None
        self.CurrentDialogId = None
        self.SubTitels = True
        self.Text = ""
        self.Dialogs = {}
        for Scene in self.app.Scenes.values():
            Attribs = Scene.attrib
            DialogController = Scene.find("DIALOGCONTROLLER")
            DialogsAll = None if DialogController == None else DialogController.findall("DIALOGPART")
            self.Dialogs[Attribs["id"]] = DialogsAll
        self.app.Sounds.CreateChannel(1)
        self.DrawDialog = True

    def DialogPlay(self):
        return self.app.Sounds.Channels["1"].get_busy()

    def update(self):
        if self.CurrentDialogId != None and not self.DialogPlay():
            DialogsFromScene = self.Dialogs[self.app.CurrentScene]
            if DialogsFromScene != None:
                for Dialog in DialogsFromScene:
                    DialogAttribs = Dialog.attrib
                    if DialogAttribs["id"] == self.CurrentDialogId:
                        Item = choice(Dialog.findall("ITEM"))
                        ItemAttrib = Item.attrib
                        self.CurrentAni = DialogAttribs["ani"]
                        self.AniMovement = DialogAttribs["mov"]
                        self.app.Sounds.PlaySound(ItemAttrib["snd"], "1")
                        self.CurrentDialogId = None
                        if self.SubTitels: self.Text = ItemAttrib["text"]
                        self.DrawDialog = False if "flags" in DialogAttribs and int(DialogAttribs["flags"]) == 2 else True
        if not self.DialogPlay():
            self.CurrentAni = None
            self.AniMovement = None
            self.CurrentDialogId = None
            self.Text = ""
            self.DrawDialog = True

    def RenderText(self, Text):
        Offset = 0
        WhiteText = self.app.Fonts.WriteFont("FontGreenGLDDS", Text, (255, 255, 255))[0]
        # Shadow = self.app.Fonts.WriteFont("FontGreenGLDDS", Text, (0, 0, 0))[0]
        Surf = pg.Surface((WhiteText.get_width() + Offset, WhiteText.get_height() + Offset), flags=pg.SRCALPHA)
        # Surf.blit(Shadow, (Offset, Offset))
        Surf.blit(WhiteText, (0, 0))
        return Surf

    def draw(self):
        if self.Text != "" and self.DrawDialog:
            TextLine = ""
            Renders = []
            SurfH = 0
            Enter = 5
            for Word in self.Text.split(): 
                Render = self.RenderText(TextLine)
                if Render.get_width() < self.app.app.s.get_width(): 
                    OldTextLine = TextLine
                    if TextLine == "": TextLine += Word
                    else: TextLine += f" {Word}"
                    if not self.RenderText(TextLine).get_width() < self.app.app.s.get_width(): 
                        TextLine = OldTextLine
                        Renders.append(self.RenderText(TextLine))
                        SurfH += Renders[-1].get_height() + Enter
                        TextLine = Word
            if TextLine != "": 
                Renders.append(self.RenderText(TextLine))
                SurfH += Renders[-1].get_height() + Enter
            Surf = pg.Surface((self.app.app.s.get_width(), SurfH), flags=pg.SRCALPHA)
            Surf.fill((128, 128, 128, 128))
            Y = 0
            for Render in reversed(Renders):
                Surf.blit(Render, (0, Surf.get_height() - Render.get_height() - Y))
                Y += Render.get_height() + Enter
            self.app.app.s.blit(Surf, (0, self.app.app.s.get_height() - Surf.get_height()))
            
class ProgressBar:
    def __init__(self, app, FgImage, ValueStandart):
        self.app = app
        self.Images = self.app.Images
        self.Value = int(ValueStandart)
        self.FgImage = FgImage
        self.FgImageWidth = self.Images[self.FgImage][0].get_width()
        self.FgImageOriginal = deepcopy(self.Images[FgImage])

    def ChangeValue(self, Value):
        self.Value = Value

    def update(self):
        self.Images[self.FgImage][0] = self.FgImageOriginal[0].subsurface(0, 0, (self.FgImageWidth / 100) * self.Value, self.FgImageOriginal[0].get_height()).copy()

class Timer:
    def __init__(self, Duration, Func = None, Repeat = False):
        self.Duration = Duration
        self.Func = Func
        self.StartTime = 0
        self.PauseTicks = 0
        self.Active = False
        self.Repeat = Repeat

    def Activate(self):
        self.Active = True
        self.StartTime = pg.time.get_ticks()   

    def Deactivate(self):
        self.Active = False
        self.StartTime = 0
        self.PauseTicks = 0
        if self.Repeat:
            self.Activate()

    def update(self):
        CurrentTime = pg.time.get_ticks()
        if CurrentTime - self.PauseTicks - self.StartTime >= self.Duration:
            if self.Func and self.StartTime != 0:
                self.Func()
            self.Deactivate()

class TextField:
    def __init__(self, app, x, y, w, h, z, limit, font, active, scene):
        self.app = app
        self.Pos = pg.math.Vector3(x, y, z)
        self.Width = w
        self.Height = h
        self.Limit = limit
        self.Font = font
        self.Active = active
        self.Scene = scene
        self.LineVisible = True
        self.LineIndent = 7
        self.Timer = Timer(500, self.TimerFunc, True)
        self.Timer.Activate()
        self.Text = ""
        self.OldText = self.Text

    def TimerFunc(self):
        self.LineVisible = not self.LineVisible

    def update(self):
        self.Timer.update()
        MousePos = self.app.MousePos
        if pg.mouse.get_pressed()[0]:
            if MousePos.x > self.Pos.x and MousePos.x < self.Pos.x + self.Width and MousePos.y > self.Pos.y and MousePos.y < self.Pos.y + self.Height: self.Active = 1
            else: self.Active = 0

    def event(self, event):
        if self.Active == 1:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE:
                    self.Text = self.Text[:-1]
                else:
                    if len(self.Text) <= self.Limit: self.Text += event.unicode
                    
    def draw(self, Offset):
        Color = None
        Font = self.Font
        if "#" in self.Font:
            FontSplitted = self.Font.split("#")
            Font = FontSplitted[0]
            FontSplitted = FontSplitted[1]
            ColorText = FontSplitted.split()
            Color = (int(ColorText[0]), int(ColorText[1]), int(ColorText[2]))
        try:
            self.RenderedText = self.app.Scenes.Fonts.WriteFont(Font, self.Text, Color)[0]
            self.app.s.blit(self.RenderedText, (self.Pos.x, self.Pos.y + self.Height // 2 - self.RenderedText.get_height() // 2) - Offset)
        except KeyError: 
            self.Text = self.OldText
            self.RenderedText = self.app.Scenes.Fonts.WriteFont(Font, self.Text, Color)[0]
            self.app.s.blit(self.RenderedText, (self.Pos.x, self.Pos.y + self.Height // 2 - self.RenderedText.get_height() // 2) - Offset)
        if self.LineVisible and len(self.Text) <= self.Limit and self.Active == 1: pg.draw.line(self.app.s, "white", (self.Pos.x + self.RenderedText.get_width(), self.Pos.y + self.LineIndent) - Offset, (self.Pos.x + self.RenderedText.get_width(), self.Pos.y + self.LineIndent + self.Height - self.LineIndent * 2) - Offset)
        self.OldText = self.Text

class Cursor:
    def __init__(self, app, app2, Offset, Image=None, Move=None):
        self.app = app
        self.app2 = app2
        self.Image = Image
        self.Move = Move
        self.Offset = Offset
        if self.Move != None: app2.AnisDict[self.Move][0].CursorM = True
        if self.Move != None: app2.AnisDict[self.Move][0].Offset = self.Offset

    def update(self):
        self.IInDict = list(self.app2.Cursors.keys())[list(self.app2.Cursors.values()).index(self)]
        if self.Move != None:
            self.app2.AnisDict[self.Move][0].update()
            if self.IInDict == self.app2.CurrentCursor: self.app2.AnisDict[self.Move][-4] = True
            else: self.app2.AnisDict[self.Move][-4] = False

    def draw(self):
        if self.Image != None: self.app.CursorSurface.blit(self.Image, self.app.MousePos - self.Offset)

class Scroller:
    def __init__(self, app, ImageBg, ImagePointer, Value, I, x, y, Offset):
        self.app = app
        self.x = x
        self.y = y
        self.Offset = Offset
        self.Images = self.app.Images
        self.ImageBg = deepcopy(self.Images[ImageBg])
        self.ImageBg[-3] = True
        self.ImagePointer = deepcopy(self.Images[ImagePointer])
        self.ImagePointer[-3] = True
        self.Images[f"ScrImageP{I}"] = self.ImagePointer
        self.Images[f"ScrImageB{I}"] = self.ImageBg
        self.ImageBg[2].y = self.y
        self.ImageBg[2].x = self.x
        self.ImagePointer[2].y = self.y + self.ImageBg[0].get_height() // 2 - self.ImagePointer[0].get_height() // 2 + self.Offset.y
        self.ImagePointer[2].x = self.x
        self.ZeroX = self.ImagePointer[2].x
        self.Value = int(Value)
        self.ChangeValue(self.Value)
        self.Pressed = False
        self.I = I

    def ChangeValue(self, Value):
        self.Value = Value
        self.ImagePointer[2].x = self.ZeroX + (Value * (self.ImageBg[0].get_width() / 100) - self.ImagePointer[0].get_width() // 2)

    def update(self):
        self.Pos = vec2(self.ImagePointer[2].x + self.ImagePointer[0].get_width() // 2, self.ImagePointer[2].y + self.ImagePointer[0].get_height() // 2)
        if self.ImagePointer[0].get_rect(x=self.ImagePointer[2].x, y=self.ImagePointer[2].y).collidepoint(self.app.app.MousePos):
            if pg.mouse.get_pressed()[0] and self.app.ScrollerPressed == None: 
                self.app.ScrollerPressed = self.I
                self.Pressed = True
        if not pg.mouse.get_pressed()[0]: 
            if self.app.ScrollerPressed == self.I: self.app.ScrollerPressed = None
            self.Pressed = False
        if self.Pressed:
            self.ImagePointer[2].x = min(max(self.app.app.MousePos.x - self.ImagePointer[0].get_width() // 2, self.x - self.ImagePointer[0].get_width() // 2 + self.Offset.x), self.ImageBg[0].get_width() + self.x - self.ImagePointer[0].get_width() // 2 - self.Offset.x)
        self.Value = (self.Pos.x - self.x) / (self.ImageBg[0].get_width() / 100)
        if self.Value == 99.99999999999999: self.Value = 100
        return self.Value
    
class CommandList:
    def __init__(self, app, Commands):
        self.app = app
        self.Commands = []
        for CommandFromDict in Commands:
            self.Commands.append(Command(self.app, CommandFromDict))
        self.IndexCommand = 0
    
    def run(self):
        if self not in self.app.NeedRun: self.app.NeedRun.append(self)
        self.Commands[self.IndexCommand].update()
        if self.Commands[self.IndexCommand].End:
            self.Commands[self.IndexCommand].End = False
            self.Commands[self.IndexCommand].SoundPlay = True
            self.IndexCommand += 1
        if self.IndexCommand >= len(self.Commands):
            self.IndexCommand = 0
            if self in self.app.NeedRun: self.app.NeedRun.remove(self)

class Command:
    def __init__(self, app, CommandDict):
        self.app = app
        self.CommandDict = CommandDict
        self.Sounds = self.app.Sounds
        self.Images = self.app.Images
        self.Anis = self.app.AnisDict
        self.SoundPlay = True
        self.SetMovement = True

    def update(self):
        self.End = False
        if self.CommandDict["id"] == "ChangeScene":
            self.app.app.ChangeScene(self.CommandDict["Scene"], literal_eval(self.CommandDict["CreatePutPrev"]))
            self.End = True
        if self.CommandDict["id"] == "PlaySound":
            if self.SoundPlay: 
                self.Sounds.PlaySound(self.CommandDict["SndId"], self.CommandDict["Channel"])
                self.SoundPlay = False
            if self.Sounds.Channels[self.CommandDict["Channel"]].get_busy() == False: 
                self.End = True
        if self.CommandDict["id"] == "HidePicture":
            self.Images[self.CommandDict["PicId"]][-3] = False
            self.End = True
        if self.CommandDict["id"] == "UnHidePicture":
            self.Images[self.CommandDict["PicId"]][-3] = True
            self.End = True
        if self.CommandDict["id"] == "LoadConfig":
            self.app.Configs[f"{self.CommandDict["Sc"]}"] = ReadXmlFile(f"{self.CommandDict["xml"]}")
            self.End = True
        if self.CommandDict["id"] == "StartMovement":
            if self.Anis[self.CommandDict["AniId"]][0].State == self.CommandDict["MovementId"]: self.Anis[self.CommandDict["AniId"]][0].Updated = True
            if self.SetMovement:
                self.Anis[self.CommandDict["AniId"]][0].State = self.CommandDict["MovementId"]
                self.Anis[self.CommandDict["AniId"]][0].Movements[self.Anis[self.CommandDict["AniId"]][0].State][0].ImageIndex = 0
                self.Anis[self.CommandDict["AniId"]][0].Movements[self.Anis[self.CommandDict["AniId"]][0].State][0].Temp = 0
                self.SetMovement = False
            elif self.Anis[self.CommandDict["AniId"]][0].MovementStop: 
                self.SetMovement = True
                self.End = True
                self.Anis[self.CommandDict["AniId"]][0].Updated = False
                self.Anis[self.CommandDict["AniId"]][0].UpdateFrame = False
        if self.CommandDict["id"] == "MoveAni":
            Pos = vec2(int(self.CommandDict["PosX"]), int(self.CommandDict["PosY"]))
            self.Anis[self.CommandDict["AId"]][0].StandartPos = Pos
            self.Anis[self.CommandDict["AId"]][2].x = Pos.x
            self.Anis[self.CommandDict["AId"]][2].y = Pos.y
            self.Anis[self.CommandDict["AId"]][0].Poses[self.app.CurrentScene] = Pos
            self.End = True
        if self.CommandDict["id"] == "Message":
            self.app.app.CurMessage = self.CommandDict["type"]
            self.End = True
        try: 
            if self.CommandDict["Wait"] == "False":
                self.End = True
        except: pass