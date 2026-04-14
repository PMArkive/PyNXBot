# Go to root/test of PyNXBot
import signal, sys, json

sys.path.append("../")

from nxbot import FRLGBot
from rng import LCRNG


def signal_handler(signal, advances):  # CTRL+C handler
    print("Stop request")
    b.close()


def find_sure_catch(seed, delay, advances):
    c = LCRNG(seed)

    for i in range(0, 1500):
        c.next()

    ballShakes = 0

    while ballShakes < 5:
        temp = LCRNG(c.state())

        while temp.state() >> 16 < 16000 and ballShakes < 5:
            ballShakes = ballShakes + 1
            temp.next()

        if ballShakes == 5:
            t = LCRNG(b.getInitialSeed())
            targetSeed = c.state()
            targetAdvances = t.lcrng_distance(targetSeed) - delay

            # if (advances - targetAdvances) % 3 == 0: # Needed for Safari Zone
            print(f"Target: {targetSeed:08X} - {targetAdvances}")
            break
            # else:
                # ballShakes = 0
        else:
            ballShakes = 0

        c.next()


signal.signal(signal.SIGINT, signal_handler)

config = json.load(open("../config.json"))
b = FRLGBot(config["IP"])

r = LCRNG(b.getInitialSeed())
initialSeed = r.initial_state()
currentSeed = b.getCurrentSeed()
advances = r.lcrng_distance(currentSeed)
catchDelay = 0

print()
print(f"Initial Seed: {initialSeed:04X}")
print(f"Current Seed: {currentSeed:08X}")
print(f"Advances: {advances}")
print()

targetAdvances = 0
botFlag = input("Press A at a specific advance? (y/n) ")

if botFlag == "y" or botFlag == "Y":
    botFlag = True
    targetAdvances = int(input("Input the target advance: "))
else:
    botFlag = False

print("\n")

while True:
    initialSeed = b.getInitialSeed()
    currentSeed = b.getCurrentSeed()
    # find_sure_catch(currentSeed, 105, advances)

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

        if b.readCatchCheckFlag() and not catchDelay:
            catchDelay = advances - targetAdvances - b.readCatchBallShakes()
            print(f"Delay: {catchDelay} (Shakes: {b.readCatchBallShakes()})")
            print()
            b.click("HOME")
            find_sure_catch(currentSeed, catchDelay, advances)

    if botFlag and advances == targetAdvances:
        for i in range(3):
            b.click("A")
            b.pause(0.002)

    b.pause(0.002)
