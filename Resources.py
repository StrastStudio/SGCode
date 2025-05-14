from settings import *
import numpy as np

def GetSurfFromNl(Scene, Key="Image"):
    Nl = ResScenesDictFiles[Scene]
    Img = pg.Surface((len(Nl[Key]), len(Nl[Key][0])), flags=pg.SRCALPHA)
    pg.surfarray.array_to_surface(Img, Nl[Key])
    return Img

# "SC_01": np.load("00000301.nl") - This is for ScenesDictFiles Teamplate 
ResScenesDictFiles = {"SC_COMMON": np.load("00000300.nl"), "SC_COMMONS": np.load("00000300.nls"), "SC_01": np.load("00000301.nl"), "SC_01S": np.load("00000301.nls"),
                      "SC_02": np.load("00000302.nl"), "SC_PAUSE": np.load("00020400.nl"), "SC_SETTINGS": np.load("00020401.nl"), "SC_GAMEOVER": np.load("00020402.nl"),
                      "SC_TITELS": np.load("00020403.nl"), "SC_INTRO": np.load("00020404.nl"), "SC_HELP": np.load("00020405.nl"), "SC_HELPS": np.load("00020405.nls"),
                      "SC_EXIT": np.load("00020406.nl"), "SC_EXITS": np.load("00020406.nls")}
ResRects = {
    # "Dog": {
    #     "ASC01DogMove": {
    #         "ImageRect": {1: [pg.Surface((646, 180), flags=pg.SRCALPHA), False]},
    #         1: (1, 0, 0, 336, 180),
    #         2: (1, 336, 0, 310, 163)
    #     }
    # }
    "ASC01ContainerPaper": {
        "MVSC01CPOpen": {
            "ImageRect": {1: [GetSurfFromNl("SC_01", "ASC01ContainerPaperMVSC01CPOpenI1"), True]},
            0: (1, 576, 511, 144, 253),
            1: (1, 576, 257, 144, 254),
            2: (1, 576, 0, 144, 257),
            3: (1, 0, 562, 144, 264),
            4: (1, 144, 561, 144, 270),
            5: (1, 288, 559, 144, 273),
            6: (1, 432, 555, 144, 275),
            7: (1, 432, 278, 144, 277),
            8: (1, 432, 0, 144, 278),
            9: (1, 288, 280, 144, 279),
            10: (1, 288, 0, 144, 280),
            11: (1, 144, 281, 144, 280),
            12: (1, 0, 281, 144, 281),
            13: (1, 144, 0, 144, 281),
            14: (1, 0, 0, 144, 281)
        },
        "MVSC01CPClose": {
            "ImageRect": {1: [GetSurfFromNl("SC_01", "ASC01ContainerPaperMVSC01CPCloseI1"), True]},
            0: (1, 0, 0, 144, 281),
            1: (1, 144, 0, 144, 281),
            2: (1, 288, 0, 144, 281),
            3: (1, 432, 0, 144, 281),
            4: (1, 576, 0, 144, 280),
            5: (1, 576, 280, 144, 280),
            6: (1, 0, 281, 144, 279),
            7: (1, 144, 281, 144, 278),
            8: (1, 144, 559, 144, 277),
            9: (1, 0, 560, 144, 276),
            10: (1, 288, 281, 144, 274),
            11: (1, 288, 555, 144, 270),
            12: (1, 432, 560, 144, 265),
            13: (1, 432, 281, 144, 258),
            14: (1, 576, 560, 144, 254)
        },
    },
    "ASC01ContainerWaste": {
        "MVSC01CWOpen": {
            "ImageRect": {1: [GetSurfFromNl("SC_01", "ASC01ContainerWasteMVSC01CWOpenI1"), True]},
            0: (1, 576, 509, 144, 252),
            1: (1, 576, 256, 144, 253),
            2: (1, 576, 0, 144, 256),
            3: (1, 144, 560, 144, 263),
            4: (1, 0, 560, 144, 269),
            5: (1, 288, 557, 144, 272),
            6: (1, 432, 554, 144, 275),
            7: (1, 432, 278, 144, 276),
            8: (1, 432, 0, 144, 278),
            9: (1, 288, 279, 144, 278),
            10: (1, 288, 0, 144, 279),
            11: (1, 144, 280, 144, 280),
            12: (1, 0, 280, 144, 280),
            13: (1, 144, 0, 144, 280),
            14: (1, 0, 0, 144, 280)
        },
        "MVSC01CWClose": {
            "ImageRect": {1: [GetSurfFromNl("SC_01", "ASC01ContainerWasteMVSC01CWCloseI1"), True]},
            0: (1, 0, 0, 144, 280),
            1: (1, 288, 0, 144, 280),
            2: (1, 144, 0, 144, 280),
            3: (1, 0, 280, 144, 280),
            4: (1, 144, 280, 144, 280),
            5: (1, 288, 280, 144, 279),
            6: (1, 432, 0, 144, 279),
            7: (1, 432, 279, 144, 278),
            8: (1, 432, 557, 144, 277),
            9: (1, 288, 559, 144, 275),
            10: (1, 0, 560, 144, 273),
            11: (1, 144, 560, 144, 269),
            12: (1, 576, 0, 144, 264),
            13: (1, 576, 264, 144, 257),
            14: (1, 576, 521, 144, 253)
        },
    },
    "ASC01ContainerFood": {
        "MVSC01CFOpen": {
            "ImageRect": {1: [GetSurfFromNl("SC_01", "ASC01ContainerFoodMVSC01CFOpenI1"), True]},
            0: (1, 576, 509, 144, 252),
            1: (1, 576, 256, 144, 253),
            2: (1, 576, 0, 144, 256),
            3: (1, 144, 560, 144, 263),
            4: (1, 0, 560, 144, 269),
            5: (1, 288, 557, 144, 272),
            6: (1, 432, 554, 144, 275),
            7: (1, 432, 278, 144, 276),
            8: (1, 432, 0, 144, 278),
            9: (1, 288, 279, 144, 278),
            10: (1, 288, 0, 144, 279),
            11: (1, 144, 280, 144, 280),
            12: (1, 0, 280, 144, 280),
            13: (1, 144, 0, 144, 280),
            14: (1, 0, 0, 144, 280)
        },
        "MVSC01CFClose": {
            "ImageRect": {1: [GetSurfFromNl("SC_01", "ASC01ContainerFoodMVSC01CFCloseI1"), True]},
            0: (1, 0, 0, 144, 280),
            1: (1, 288, 0, 144, 280),
            2: (1, 144, 0, 144, 280),
            3: (1, 0, 280, 144, 280),
            4: (1, 144, 280, 144, 280),
            5: (1, 288, 280, 144, 279),
            6: (1, 432, 0, 144, 279),
            7: (1, 432, 279, 144, 278),
            8: (1, 432, 557, 144, 277),
            9: (1, 288, 559, 144, 275),
            10: (1, 0, 560, 144, 273),
            11: (1, 144, 560, 144, 269),
            12: (1, 576, 0, 144, 264),
            13: (1, 576, 264, 144, 257),
            14: (1, 576, 521, 144, 253)
        },
    },
    "ASC01ContainerIron": {
        "MVSC01CIOpen": {
            "ImageRect": {1: [GetSurfFromNl("SC_01", "ASC01ContainerIronMVSC01CIOpenI1"), True]},
            0: (1, 576, 509, 144, 252),
            1: (1, 576, 256, 144, 253),
            2: (1, 576, 0, 144, 256),
            3: (1, 144, 560, 144, 263),
            4: (1, 0, 560, 144, 269),
            5: (1, 288, 557, 144, 272),
            6: (1, 432, 554, 144, 275),
            7: (1, 432, 278, 144, 276),
            8: (1, 432, 0, 144, 278),
            9: (1, 288, 279, 144, 278),
            10: (1, 288, 0, 144, 279),
            11: (1, 144, 280, 144, 280),
            12: (1, 0, 280, 144, 280),
            13: (1, 144, 0, 144, 280),
            14: (1, 0, 0, 144, 280)
        },
        "MVSC01CIClose": {
            "ImageRect": {1: [GetSurfFromNl("SC_01", "ASC01ContainerIronMVSC01CICloseI1"), True]},
            0: (1, 0, 0, 144, 280),
            1: (1, 288, 0, 144, 280),
            2: (1, 144, 0, 144, 280),
            3: (1, 0, 280, 144, 280),
            4: (1, 144, 280, 144, 280),
            5: (1, 288, 280, 144, 279),
            6: (1, 432, 0, 144, 279),
            7: (1, 432, 279, 144, 278),
            8: (1, 432, 557, 144, 277),
            9: (1, 288, 559, 144, 275),
            10: (1, 0, 560, 144, 273),
            11: (1, 144, 560, 144, 269),
            12: (1, 576, 0, 144, 264),
            13: (1, 576, 264, 144, 257),
            14: (1, 576, 521, 144, 253)
        },
    },
    "ASC01ContainerGlass": {
        "MVSC01CGOpen": {
            "ImageRect": {1: [GetSurfFromNl("SC_01", "ASC01ContainerGlassMVSC01CGOpenI1"), True]},
            0: (1, 576, 509, 144, 252),
            1: (1, 576, 256, 144, 253),
            2: (1, 576, 0, 144, 256),
            3: (1, 144, 560, 144, 263),
            4: (1, 0, 560, 144, 269),
            5: (1, 288, 557, 144, 272),
            6: (1, 432, 554, 144, 275),
            7: (1, 432, 278, 144, 276),
            8: (1, 432, 0, 144, 278),
            9: (1, 288, 279, 144, 278),
            10: (1, 288, 0, 144, 279),
            11: (1, 144, 280, 144, 280),
            12: (1, 0, 280, 144, 280),
            13: (1, 144, 0, 144, 280),
            14: (1, 0, 0, 144, 280)
        },
        "MVSC01CGClose": {
            "ImageRect": {1: [GetSurfFromNl("SC_01", "ASC01ContainerGlassMVSC01CGCloseI1"), True]},
            0: (1, 0, 0, 144, 280),
            1: (1, 288, 0, 144, 280),
            2: (1, 144, 0, 144, 280),
            3: (1, 0, 280, 144, 280),
            4: (1, 144, 280, 144, 280),
            5: (1, 288, 280, 144, 279),
            6: (1, 432, 0, 144, 279),
            7: (1, 432, 279, 144, 278),
            8: (1, 432, 557, 144, 277),
            9: (1, 288, 559, 144, 275),
            10: (1, 0, 560, 144, 273),
            11: (1, 144, 560, 144, 269),
            12: (1, 576, 0, 144, 264),
            13: (1, 576, 264, 144, 257),
            14: (1, 576, 521, 144, 253)
        },
    },
    "ASC01ContainerPlastic": {
        "MVSC01CPlOpen": {
            "ImageRect": {1: [GetSurfFromNl("SC_01", "ASC01ContainerPlasticMVSC01CPlOpenI1"), True]},
            0: (1, 576, 509, 144, 252),
            1: (1, 576, 256, 144, 253),
            2: (1, 576, 0, 144, 256),
            3: (1, 144, 560, 144, 263),
            4: (1, 0, 560, 144, 269),
            5: (1, 288, 557, 144, 272),
            6: (1, 432, 554, 144, 275),
            7: (1, 432, 278, 144, 276),
            8: (1, 432, 0, 144, 278),
            9: (1, 288, 279, 144, 278),
            10: (1, 288, 0, 144, 279),
            11: (1, 144, 280, 144, 280),
            12: (1, 0, 280, 144, 280),
            13: (1, 144, 0, 144, 280),
            14: (1, 0, 0, 144, 280)
        },
        "MVSC01CPlClose": {
            "ImageRect": {1: [GetSurfFromNl("SC_01", "ASC01ContainerPlasticMVSC01CPlCloseI1"), True]},
            0: (1, 0, 0, 144, 280),
            1: (1, 288, 0, 144, 280),
            2: (1, 144, 0, 144, 280),
            3: (1, 0, 280, 144, 280),
            4: (1, 144, 280, 144, 280),
            5: (1, 288, 280, 144, 279),
            6: (1, 432, 0, 144, 279),
            7: (1, 432, 279, 144, 278),
            8: (1, 432, 557, 144, 277),
            9: (1, 288, 559, 144, 275),
            10: (1, 0, 560, 144, 273),
            11: (1, 144, 560, 144, 269),
            12: (1, 576, 0, 144, 264),
            13: (1, 576, 264, 144, 257),
            14: (1, 576, 521, 144, 253)
        },
    },
    "ACsrNormal": {
        "MVCsrNormalDef": {
            "ImageRect": {1: [GetSurfFromNl("SC_COMMON", "ACsrNormalMVCsrNormalDefI1"), True]},
            0: (1, 0, 0, 100, 100),
            1: (1, 100, 0, 100, 100),
            2: (1, 200, 0, 100, 100),
            3: (1, 300, 0, 100, 100),
            4: (1, 400, 0, 100, 100),
            5: (1, 500, 0, 100, 100),
            6: (1, 600, 0, 100, 100),
            7: (1, 700, 0, 100, 100),
            8: (1, 800, 0, 100, 100),
            9: (1, 900, 0, 100, 100),
            10: (1, 0, 100, 100, 100),
            11: (1, 100, 100, 100, 100),
            12: (1, 200, 100, 100, 100),
            13: (1, 300, 100, 100, 100),
            14: (1, 400, 100, 100, 100),
            15: (1, 500, 100, 100, 100),
            16: (1, 600, 100, 100, 100),
            17: (1, 700, 100, 100, 100),
            18: (1, 800, 100, 100, 100),
            19: (1, 900, 100, 100, 100),
            20: (1, 0, 200, 100, 100),
            21: (1, 100, 200, 100, 100),
            22: (1, 200, 200, 100, 100),
            23: (1, 300, 200, 100, 100),
            24: (1, 400, 200, 100, 100),
            25: (1, 500, 200, 100, 100),
            26: (1, 600, 200, 100, 100),
            27: (1, 700, 200, 100, 100),
            28: (1, 800, 200, 100, 100),
            29: (1, 900, 200, 100, 100),
            30: (1, 0, 300, 100, 100),
            31: (1, 100, 300, 100, 100),
            32: (1, 200, 300, 100, 100),
            33: (1, 300, 300, 100, 100),
            34: (1, 400, 300, 100, 100),
            35: (1, 500, 300, 100, 100),
            36: (1, 600, 300, 100, 100),
            37: (1, 700, 300, 100, 100),
            38: (1, 800, 300, 100, 100),
            39: (1, 900, 300, 100, 100),
            40: (1, 0, 400, 100, 100),
            41: (1, 100, 400, 100, 100),
            42: (1, 200, 400, 100, 100),
            43: (1, 300, 400, 100, 100),
            44: (1, 400, 400, 100, 100),
            45: (1, 500, 400, 100, 100),
            46: (1, 600, 400, 100, 100),
            47: (1, 700, 400, 100, 100),
            48: (1, 800, 400, 100, 100),
            49: (1, 900, 400, 100, 100),
            50: (1, 0, 500, 100, 100),
            51: (1, 100, 500, 100, 100),
            52: (1, 200, 500, 100, 100),
            53: (1, 300, 500, 100, 100),
            54: (1, 400, 500, 100, 100),
            55: (1, 500, 500, 100, 100),
            56: (1, 600, 500, 100, 100),
            57: (1, 700, 500, 100, 100),
            58: (1, 800, 500, 100, 100),
            59: (1, 900, 500, 100, 100)
        },
    },
}

SCCMNIMG = GetSurfFromNl("SC_COMMON")
SC01IMG = GetSurfFromNl("SC_01")
SC01PS = GetSurfFromNl("SC_01", "ASC01ContainerPaperStatics")
SC01WS = GetSurfFromNl("SC_01", "ASC01ContainerWasteStatics")
SC01FS = GetSurfFromNl("SC_01", "ASC01ContainerFoodStatics")
SC01IS = GetSurfFromNl("SC_01", "ASC01ContainerIronStatics")
SC01GS = GetSurfFromNl("SC_01", "ASC01ContainerGlassStatics")
SC01PLS = GetSurfFromNl("SC_01", "ASC01ContainerPlasticStatics")
SC02IMG = GetSurfFromNl("SC_02")
SCPAUSEIMG = GetSurfFromNl("SC_PAUSE")
SCSETIMG = GetSurfFromNl("SC_SETTINGS")
SCGOIMG = GetSurfFromNl("SC_GAMEOVER")
SCTITIMG = GetSurfFromNl("SC_TITELS")
SCINTROIMG = GetSurfFromNl("SC_INTRO")
# SCHELPIMG = GetSurfFromNl("SC_HELP")
SCEXITIMG = GetSurfFromNl("SC_EXIT")

pg.display.set_icon(SCCMNIMG.subsurface(0, 1080, 256, 256))

ResStaticImages = {}
# In this block of code load statics!
# ResStaticImages["SRozaIdle"] = pg.image.load("00000650/00028331/00028332.png").convert_alpha() - Example
ResStaticImages["SSC01CPDef"] = SC01PS.subsurface(0, 0, 159, 322)
ResStaticImages["SSC01CPOpen"] = SC01PS.subsurface(0, 322, 159, 322)
ResStaticImages["SSC01CWDef"] = SC01WS.subsurface(0, 0, 159, 322)
ResStaticImages["SSC01CWOpen"] = SC01WS.subsurface(0, 322, 159, 322)
ResStaticImages["SSC01CFDef"] = SC01FS.subsurface(0, 0, 159, 322)
ResStaticImages["SSC01CFOpen"] = SC01FS.subsurface(0, 322, 159, 322)
ResStaticImages["SSC01CIDef"] = SC01IS.subsurface(0, 0, 159, 322)
ResStaticImages["SSC01CIOpen"] = SC01IS.subsurface(0, 322, 159, 322)
ResStaticImages["SSC01CGDef"] = SC01GS.subsurface(0, 0, 159, 322)
ResStaticImages["SSC01CGOpen"] = SC01GS.subsurface(0, 322, 159, 322)
ResStaticImages["SSC01CPlDef"] = SC01PLS.subsurface(0, 0, 159, 322)
ResStaticImages["SSC01CPlOpen"] = SC01PLS.subsurface(0, 322, 159, 322)
ResStaticImages["SCsrNormalDef"] = SCCMNIMG.subsurface(646, 1080, 100, 100)

ResCursors = {}
# In this block of code load cursors!
# ResCursors["CsrNormal"] = pg.image.load("00000300/00003001.png").convert_alpha() - Example

ResCursors["CsrNormalWA"] = SCCMNIMG.subsurface(256, 1080, 75, 76)

ResImages = []
# In this block of code load images!
# ResImages.append(["PicSC01Bg", "SC_01", pg.image.load("00000301/00003010.png").convert()]) - Example
ResImages.append(["PicSCCMNFg", "SC_COMMON", SCCMNIMG.subsurface(0, 0, 1920, 1080)])
ResImages.append(["PicSCCMNBtnHelpPass", "SC_COMMON", SCCMNIMG.subsurface(256, 1080, 130, 120)])
ResImages.append(["PicSCCMNBtnHelpHover", "SC_COMMON", SCCMNIMG.subsurface(386, 1080, 130, 120)])
ResImages.append(["PicSCCMNBtnHelpPress", "SC_COMMON", SCCMNIMG.subsurface(516, 1080, 130, 114)])
ResImages.append(["PicSC01Bg", "SC_01", SC01IMG.subsurface(0, 0, 1920, 1080)])
ResImages.append(["PicSC01Fg", "SC_01", SC01IMG.subsurface(1920, 0, 1920, 1080)])
ResImages.append(["PicSC01Light", "SC_01", SC01IMG.subsurface(0, 1080, 1920, 1080)])
ResImages.append(["PicSC01RibbonFg", "SC_01", SC01IMG.subsurface(1920, 1080, 1668, 231)])
ResImages.append(["PicSC01RibbonBg", "SC_01", SC01IMG.subsurface(1920, 1311, 1664, 210)])
ResImages.append(["PicSC01GarbageUI", "SC_01", SC01IMG.subsurface(1920, 1521, 1666, 198)])
ResImages.append(["PicSC01Garbage13", "SC_01", SC01IMG.subsurface(3584, 1311, 152, 197)])
ResImages.append(["PicSC01Garbage6", "SC_01", SC01IMG.subsurface(3588, 1080, 152, 197)])
ResImages.append(["PicSC01Garbage7", "SC_01", SC01IMG.subsurface(3586, 1508, 152, 197)])
ResImages.append(["PicSC01Garbage8", "SC_01", SC01IMG.subsurface(3586, 1705, 152, 197)])
ResImages.append(["PicSC01Garbage9", "SC_01", SC01IMG.subsurface(1920, 1719, 152, 197)])
ResImages.append(["PicSC01Garbage2", "SC_01", SC01IMG.subsurface(2072, 1719, 152, 197)])
ResImages.append(["PicSC01Garbage10", "SC_01", SC01IMG.subsurface(2224, 1719, 152, 197)])
ResImages.append(["PicSC01Garbage4", "SC_01", SC01IMG.subsurface(2376, 1719, 152, 197)])
ResImages.append(["PicSC01Garbage12", "SC_01", SC01IMG.subsurface(2528, 1719, 152, 197)])
ResImages.append(["PicSC01Garbage3", "SC_01", SC01IMG.subsurface(2680, 1719, 152, 197)])
ResImages.append(["PicSC01Garbage14", "SC_01", SC01IMG.subsurface(2832, 1719, 152, 197)])
ResImages.append(["PicSC01Garbage15", "SC_01", SC01IMG.subsurface(2984, 1719, 152, 197)])
ResImages.append(["PicSC01Garbage16", "SC_01", SC01IMG.subsurface(3136, 1719, 152, 197)])
ResImages.append(["PicSC01Garbage17", "SC_01", SC01IMG.subsurface(3288, 1719, 152, 197)])
ResImages.append(["PicSC01Garbage18", "SC_01", SC01IMG.subsurface(3440, 1902, 152, 197)])
ResImages.append(["PicSC01Garbage19", "SC_01", SC01IMG.subsurface(3592, 1902, 152, 197)])
ResImages.append(["PicSC01Garbage1", "SC_01", SC01IMG.subsurface(1920, 1916, 152, 197)])
ResImages.append(["PicSC01Garbage20", "SC_01", SC01IMG.subsurface(2072, 1916, 152, 197)])
ResImages.append(["PicSC01Garbage21", "SC_01", SC01IMG.subsurface(2224, 1916, 152, 197)])
ResImages.append(["PicSC01Garbage5", "SC_01", SC01IMG.subsurface(2376, 1916, 152, 197)])
ResImages.append(["PicSC01Garbage11", "SC_01", SC01IMG.subsurface(2528, 1916, 152, 197)])
ResImages.append(["PicSC02Bg", "SC_02", SC02IMG.subsurface(0, 0, 1920, 1080)])
ResImages.append(["PicSC02BtnSettingsPass", "SC_02", SC02IMG.subsurface(0, 1080, 615, 153)])
ResImages.append(["PicSC02BtnSettingsHover", "SC_02", SC02IMG.subsurface(615, 1080, 615, 153)])
ResImages.append(["PicSC02BtnExitPass", "SC_02", SC02IMG.subsurface(1230, 1080, 405, 152)])
ResImages.append(["PicSC02BtnExitHover", "SC_02", SC02IMG.subsurface(1230, 1232, 405, 152)])
ResImages.append(["PicSC02BtnTitelsPass", "SC_02", SC02IMG.subsurface(0, 1233, 405, 152)])
ResImages.append(["PicSC02BtnTitelsHover", "SC_02", SC02IMG.subsurface(405, 1233, 405, 152)])
ResImages.append(["PicSC02BtnSettingsPress", "SC_02", SC02IMG.subsurface(810, 1384, 615, 142)])
ResImages.append(["PicSC02BtnExitPress", "SC_02", SC02IMG.subsurface(810, 1233, 405, 141)])
ResImages.append(["PicSC02BtnPlayPass", "SC_02", SC02IMG.subsurface(0, 1385, 405, 152)])
ResImages.append(["PicSC02BtnPlayHover", "SC_02", SC02IMG.subsurface(405, 1385, 405, 152)])
ResImages.append(["PicSC02BtnTitelsPress", "SC_02", SC02IMG.subsurface(1425, 1384, 405, 141)])
ResImages.append(["PicSC02BtnPlayPress", "SC_02", SC02IMG.subsurface(1635, 1080, 405, 141)])
ResImages.append(["PicSCPAUSEBg", "SC_PAUSE", SCPAUSEIMG.subsurface(0, 0, 1920, 1080)])
ResImages.append(["PicSCPAUSEBtnContinuePass", "SC_PAUSE", SCPAUSEIMG.subsurface(0, 1080, 743, 153)])
ResImages.append(["PicSCPAUSEBtnContinueHover", "SC_PAUSE", SCPAUSEIMG.subsurface(743, 1080, 743, 153)])
ResImages.append(["PicSCPAUSEBtnContinuePress", "SC_PAUSE", SCPAUSEIMG.subsurface(0, 1233, 743, 142)])
ResImages.append(["PicSCPAUSEBtnSettingsPass", "SC_PAUSE", SCPAUSEIMG.subsurface(0, 1375, 615, 153)])
ResImages.append(["PicSCPAUSEBtnSettingsHover", "SC_PAUSE", SCPAUSEIMG.subsurface(615, 1375, 615, 153)])
ResImages.append(["PicSCPAUSEBtnSettingsPress", "SC_PAUSE", SCPAUSEIMG.subsurface(743, 1233, 615, 142)])
ResImages.append(["PicSCPAUSEBtnMenuPass", "SC_PAUSE", SCPAUSEIMG.subsurface(1230, 1375, 379, 153)])
ResImages.append(["PicSCPAUSEBtnMenuHover", "SC_PAUSE", SCPAUSEIMG.subsurface(1486, 1080, 379, 153)])
ResImages.append(["PicSCPAUSEBtnMenuPress", "SC_PAUSE", SCPAUSEIMG.subsurface(1358, 1233, 379, 142)])
ResImages.append(["PicSCSETBg", "SC_SETTINGS", SCSETIMG.subsurface(0, 0, 1920, 1080)])
ResImages.append(["PicSCSETBtnBackPass", "SC_SETTINGS", SCSETIMG.subsurface(0, 1080, 379, 153)])
ResImages.append(["PicSCSETBtnBackHover", "SC_SETTINGS", SCSETIMG.subsurface(379, 1080, 379, 153)])
ResImages.append(["PicSCSETBtnBackPress", "SC_SETTINGS", SCSETIMG.subsurface(758, 1080, 379, 142)])
ResImages.append(["PicSCSETScrBg", "SC_SETTINGS", SCSETIMG.subsurface(1137, 1080, 511, 80)])
ResImages.append(["PicSCSETScrFg", "SC_SETTINGS", SCSETIMG.subsurface(1648, 1080, 38, 119)])
ResImages.append(["PicSCGOBg", "SC_GAMEOVER", SCGOIMG.subsurface(0, 0, 1920, 1080)])
ResImages.append(["PicSCGOBtnRetryPass", "SC_GAMEOVER", SCGOIMG.subsurface(0, 1080, 404, 153)])
ResImages.append(["PicSCGOBtnRetryHover", "SC_GAMEOVER", SCGOIMG.subsurface(404, 1080, 404, 153)])
ResImages.append(["PicSCGOBtnRetryPress", "SC_GAMEOVER", SCGOIMG.subsurface(808, 1080, 404, 142)])
ResImages.append(["PicSCGOBtnMenuPass", "SC_GAMEOVER", SCGOIMG.subsurface(1212, 1080, 379, 153)])
ResImages.append(["PicSCGOBtnMenuHover", "SC_GAMEOVER", SCGOIMG.subsurface(808, 1222, 379, 153)])
ResImages.append(["PicSCGOBtnMenuPress", "SC_GAMEOVER", SCGOIMG.subsurface(0, 1233, 379, 142)])
ResImages.append(["PicSCTITText", "SC_TITELS", SCTITIMG.subsurface(0, 0, 1109, 1984)])
ResImages.append(["PicSCTITBg", "SC_TITELS", SCTITIMG.subsurface(1109, 0, 1920, 1080)])
ResImages.append(["PicSCTITFg", "SC_TITELS", SCTITIMG.subsurface(1109, 1080, 1920, 1080)])
ResImages.append(["PicSCINTROStrast", "SC_INTRO", SCINTROIMG.subsurface(0, 0, 1920, 1080)])
ResImages.append(["PicSCINTROGameLogo", "SC_INTRO", SCINTROIMG.subsurface(1920, 0, 1920, 1080)])
ResImages.append(["PicSCHELPBg", "SC_HELP", GetSurfFromNl("SC_HELP", "I00204050_png")])
ResImages.append(["PicSCHELPGlow", "SC_HELP", GetSurfFromNl("SC_HELP", "I002040535_png")])
ResImages.append(["PicSCHELPSC02Pic0", "SC_HELP", GetSurfFromNl("SC_HELP", "I002040513_png")])
ResImages.append(["PicSCHELPSC02Pic1", "SC_HELP", GetSurfFromNl("SC_HELP", "I002040514_png")])
ResImages.append(["PicSCHELPSC02Pic2", "SC_HELP", GetSurfFromNl("SC_HELP", "I002040515_png")])
ResImages.append(["PicSCHELPSC02Pic3", "SC_HELP", GetSurfFromNl("SC_HELP", "I002040516_png")])
ResImages.append(["PicSCHELPSCSETPic0", "SC_HELP", GetSurfFromNl("SC_HELP", "I002040517_png")])
ResImages.append(["PicSCHELPSCSETPic1", "SC_HELP", GetSurfFromNl("SC_HELP", "I002040518_png")])
ResImages.append(["PicSCHELPSCSETPic2", "SC_HELP", GetSurfFromNl("SC_HELP", "I002040519_png")])
ResImages.append(["PicSCHELPSC01Pic0", "SC_HELP", GetSurfFromNl("SC_HELP", "I002040520_png")])
ResImages.append(["PicSCHELPSC01Pic1", "SC_HELP", GetSurfFromNl("SC_HELP", "I002040521_png")])
ResImages.append(["PicSCHELPSC01Pic2", "SC_HELP", GetSurfFromNl("SC_HELP", "I002040522_png")])
ResImages.append(["PicSCHELPSCPAUSEPic0", "SC_HELP", GetSurfFromNl("SC_HELP", "I002040523_png")])
ResImages.append(["PicSCHELPSCPAUSEPic1", "SC_HELP", GetSurfFromNl("SC_HELP", "I002040524_png")])
ResImages.append(["PicSCHELPSCPAUSEPic2", "SC_HELP", GetSurfFromNl("SC_HELP", "I002040525_png")])
ResImages.append(["PicSCHELPSCGAMEOVERPic0", "SC_HELP", GetSurfFromNl("SC_HELP", "I002040532_png")])
ResImages.append(["PicSCHELPSCGAMEOVERPic1", "SC_HELP", GetSurfFromNl("SC_HELP", "I002040533_png")])
ResImages.append(["PicSCHELPSCGAMEOVERPic2", "SC_HELP", GetSurfFromNl("SC_HELP", "I002040534_png")])
ResImages.append(["PicSCHELPBtnPlayPass", "SC_HELP", GetSurfFromNl("SC_HELP", "I00204054_png")])
ResImages.append(["PicSCHELPBtnPlayHover", "SC_HELP", GetSurfFromNl("SC_HELP", "I00204055_png")])
ResImages.append(["PicSCHELPBtnPlayPress", "SC_HELP", GetSurfFromNl("SC_HELP", "I00204056_png")])
ResImages.append(["PicSCHELPBtnPlayDisabled", "SC_HELP", GetSurfFromNl("SC_HELP", "I002040527_png")])
ResImages.append(["PicSCHELPBtnStopPass", "SC_HELP", GetSurfFromNl("SC_HELP", "I00204057_png")])
ResImages.append(["PicSCHELPBtnStopHover", "SC_HELP", GetSurfFromNl("SC_HELP", "I00204058_png")])
ResImages.append(["PicSCHELPBtnStopPress", "SC_HELP", GetSurfFromNl("SC_HELP", "I00204059_png")])
ResImages.append(["PicSCHELPBtnNextPass", "SC_HELP", GetSurfFromNl("SC_HELP", "I002040510_png")])
ResImages.append(["PicSCHELPBtnNextHover", "SC_HELP", GetSurfFromNl("SC_HELP", "I002040511_png")])
ResImages.append(["PicSCHELPBtnNextPress", "SC_HELP", GetSurfFromNl("SC_HELP", "I002040512_png")])
ResImages.append(["PicSCHELPBtnNextDisabled", "SC_HELP", GetSurfFromNl("SC_HELP", "I002040528_png")])
ResImages.append(["PicSCHELPBtnBackPass", "SC_HELP", GetSurfFromNl("SC_HELP", "I00204051_png")])
ResImages.append(["PicSCHELPBtnBackHover", "SC_HELP", GetSurfFromNl("SC_HELP", "I00204052_png")])
ResImages.append(["PicSCHELPBtnBackPress", "SC_HELP", GetSurfFromNl("SC_HELP", "I00204053_png")])
ResImages.append(["PicSCHELPBtnBackDisabled", "SC_HELP", GetSurfFromNl("SC_HELP", "I002040526_png")])
ResImages.append(["PicSCHELPBtnCrossPass", "SC_HELP", GetSurfFromNl("SC_HELP", "I002040529_png")])
ResImages.append(["PicSCHELPBtnCrossHover", "SC_HELP", GetSurfFromNl("SC_HELP", "I002040530_png")])
ResImages.append(["PicSCHELPBtnCrossPress", "SC_HELP", GetSurfFromNl("SC_HELP", "I002040531_png")])
ResImages.append(["PicSCEXITBtnYesPress", "SC_EXIT", SCEXITIMG.subsurface(0, 0, 269, 142)])
ResImages.append(["PicSCEXITBtnNoPress", "SC_EXIT", SCEXITIMG.subsurface(269, 0, 269, 142)])
ResImages.append(["PicSCEXITBtnYesPass", "SC_EXIT", SCEXITIMG.subsurface(538, 0, 269, 153)])
ResImages.append(["PicSCEXITBtnYesHover", "SC_EXIT", SCEXITIMG.subsurface(807, 0, 269, 153)])
ResImages.append(["PicSCEXITBtnNoPass", "SC_EXIT", SCEXITIMG.subsurface(1076, 0, 269, 153)])
ResImages.append(["PicSCEXITBtnNoHover", "SC_EXIT", SCEXITIMG.subsurface(1345, 0, 269, 153)])
ResImages.append(["PicSCEXITBg", "SC_EXIT", SCEXITIMG.subsurface(0, 153, 1920, 1080)])


ResAnis = []
# In this block of code load anis!
# ResAnis.append(["ASC01Roza", "SC_01", "MVSC01RozaIdle"]) - Example
ResAnis.append(["ASC01ContainerPaper", "SC_01", "Standart"])
ResAnis.append(["ASC01ContainerWaste", "SC_01", "Standart"])
ResAnis.append(["ASC01ContainerFood", "SC_01", "Standart"])
ResAnis.append(["ASC01ContainerIron", "SC_01", "Standart"])
ResAnis.append(["ASC01ContainerGlass", "SC_01", "Standart"])
ResAnis.append(["ASC01ContainerPlastic", "SC_01", "Standart"])
ResAnis.append(["ACsrNormal", "SC_COMMON", "Standart"])

def LoadFonts(TtfFunc, FileFunc):
    return({"FontOrangeGD": FileFunc("FONTS/FontOrangeGD.xml"), "FontGreenGLDDS": FileFunc("FONTS/FontGreenGLDDS.xml"),
            "FontWhiteNISDS": FileFunc("FONTS/FontWhiteNISDS.xml"), "FontRedNISDS": FileFunc("FONTS/FontRedNISDS.xml")})