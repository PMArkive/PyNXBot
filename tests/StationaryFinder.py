# Connect your Switch to Interet
# Start sys-botbase and ldn_mitm
# Go to System Settings, check your Switch IP and write it inside the "config.json" file
# Save in front of a stationary and leave the game opened
# Modify research filters inside the script according to what is written below
# Run the script

# pk8.getAbilityString() == 1/2/"H"
# Util(GameVersion.SWSH).STRINGS.natures[pk8.nature()] == "Nature"
# pk8.shinyString() == "None"/"Star"/"Square" (!= "None" for both star/square)
# pk8.IVs == spread_name (spread_name = [x,x,x,x,x,x])
# Util(GameVersion.SWSH).GenderSymbol[pk8.gender()] == "♂"/"♀"/"-"

import signal, sys, json
from lookups import Util, GameVersion
from nxbot import SWSHBot
from structure import PK8

# Go to root of PyNXBot
sys.path.append("../")

# CTRL+C handler
def signal_handler(signal, frame):
    print()
    print("Stop request")
    b.close()

signal.signal(signal.SIGINT, signal_handler)

config = json.load(open("../config.json"))
b = SWSHBot(config["IP"])

# Add here the spreads you need
V6 = [31, 31, 31, 31, 31, 31]
A0 = [31, 0, 31, 31, 31, 31]
S0 = [31, 31, 31, 31, 31, 0]
TRA0 = [31, 0, 31, 31, 31, 0]

print("Modes:\n1) Ethernatus\n2)Registeel/Regirock/Regice/Regidrago/Regieleki\n")

mode = int(input("Input the desired mode: (1/2) "))

while True:
    found = False

    if mode == 1:
        b.moveStick("LEFT", x=0, y=32767)
        b.pause(2)
        b.moveStick("LEFT", x=0, y=0)
        print("Skipping cutscene...")
    else:
        print("Starting battle...")

    battle = False
    i = 0

    while battle is not True and i <= 90:
        pk8 = PK8(b.readWild())

        if pk8.isValid() and pk8.ec() != 0:
            battle = True
            print("Battle started! - Checking stats...")
            b.pause(0.5)
            print(pk8.toString())

            if Util(GameVersion.SWSH).STRINGS.natures[pk8.nature()] == "Timid" or pk8.shinyString() != "None":
                found = True

            break

        if mode == 2:
            b.click("A")
        else:
            b.click("B")

        b.pause(0.5)
        i += 1

    if found:
        b.foundActions()
    else:
        b.notfoundActions(i)

    # Game resetting
    print("Resetting...")
    b.quitGame()
    b.enterGame()
    b.skipIntroAnimation()
