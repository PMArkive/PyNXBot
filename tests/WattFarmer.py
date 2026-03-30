# Watts farmer Bot

import signal, sys, json
from structure import Den
from nxbot import RaidBot

# Go to root/test of PyNXBot
sys.path.append("../")


# CTRL+C handler
def signal_handler(signal, frame):
    print()
    print("Stop request")
    b.close()


signal.signal(signal.SIGINT, signal_handler)

config = json.load(open("../config.json"))
b = RaidBot(config["IP"])

currWatts = b.TrainerSave.Watts()
b.setWatts(currWatts)
print(f"Current Watts: {currWatts}\n")
print("Farming watts...")

while True:
    # R on Luxray "+1" button
    b.click("R")
    b.pause(0.7)

    for ii in range(RaidBot.DENCOUNT):
        if ii > 189:
            den = Den(b.readDen(ii + 32))
        elif ii > 99:
            den = Den(b.readDen(ii + 11))
        else:
            den = Den(b.readDen(ii))

        if den.isActive() and den.isWishingPiece():
            if den.hasWatts():
                b.getWatts(True, 0.5)
                break
            else:
                print("No watts in Den")
                break

    stop = input("Continue farming? (y/n): ")

    if stop == "n" or stop == "N":
        break

print("Watts farming ended")
print()
b.close()
