# Berry Picker Bot

import signal, sys, json

# Go to root/test of PyNXBot
sys.path.append("../")

from nxbot import BerryBot


# CTRL+C handler
def signal_handler(signal, frame):
    print()
    print("Stop request")
    b.pickBeforeLeaving()
    b.close()


signal.signal(signal.SIGINT, signal_handler)

config = json.load(open("../config.json"))
b = BerryBot(config["IP"])

cycles = input("Do you want a limited number of picking cycles? (y/n): ")

if cycles == "y" or cycles == "Y":
    cycles = int(input("Input the max number of picking cycles: "))
else:
    cycles = sys.maxsize

shakes = int(input("How many shakes per cycle? (input the number): "))

b.pause(0.5)
print()
i = 0

while i < cycles:
    # R on Luxray "+1" button
    b.click("R")
    b.pause(1.2)
    print("Cycle", i + 1)
    b.shakeTree()
    b.continueShaking(shakes - 1)
    b.pickEverything()
    b.pause(0.5)
    print()
    i += 1

print(i, "Cycles completed!")
print()
b.close()
