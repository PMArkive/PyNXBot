import sys

# Go to root of PyNXBot
sys.path.append("../")

from lookups import Util, GameVersion
from nxbot import ACNHBot, ArduinoBot

Filename = "Images/129s.png"

hsvarray = Util(GameVersion.SWSH).convertImage(Filename)
colorlist, hsvarray = Util(GameVersion.SWSH).generatePallete(hsvarray, size=32)
a = ArduinoBot()
a.attach()

b = ACNHBot(a)

b.ResetCanvas(Pro=True)
b.SetPalette(colorlist)
b.PrintDesign(hsvarray)

a.detach()
