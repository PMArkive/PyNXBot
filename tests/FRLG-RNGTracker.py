# Go to root/test of PyNXBot
import signal, sys, json

sys.path.append("../")

from nxbot import FRLGBot
from rng import LCRNG


def signal_handler(signal, advances):  # CTRL+C handler
    print("Stop request")
    b.close()


signal.signal(signal.SIGINT, signal_handler)

config = json.load(open("../config.json"))
b = FRLGBot(config["IP"])

r = LCRNG(b.getInitialSeed())
initialSeed = r.initial_seed()
currentSeed = r.state()
advances = 0

print()
print(f"Initial Seed: {initialSeed:04X}")
print()

"""targetAdvances = 0
botFlag = input("Press A at a specific advance? (y/n) ")
if botFlag == "y" or botFlag == "Y":
    botFlag = True
    targetAdvances = int(input("Input the target advance: "))
else:
    botFlag = False
print("\n")"""

while True:
    initialSeed = b.getInitialSeed()
    currentSeed = b.getCurrentSeed()

    if r.initial_state() != initialSeed:
        r.initial_seed = initialSeed
        r.seed = currentSeed
        advances = 0
        print("------------------------------------------\n")
        print(f"Initial Seed: {initialSeed:04X}")
        print()

    if r.state() != currentSeed:
        advances += r.lcrng_distance(currentSeed)
        print(f"Current Seed: {currentSeed:08X}")
        print(f"Advances: {advances}")
        print()

        if advances == 2558:
            for i in range(5):
                b.click("A")
                b.pause(0.2)

    """if botFlag and advances == targetAdvances:
            for i in range(5):
                b.click("A")
                b.pause(0.2)"""

    b.pause(0.02)
