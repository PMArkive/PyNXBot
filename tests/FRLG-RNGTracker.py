JUMP_DATA = (
    # (mult, add)
    (0x41C64E6D, 0x6073),
    (0xC2A29A69, 0xE97E7B6A),
    (0xEE067F11, 0x31B0DDE4),
    (0xCFDDDF21, 0x67DBB608),
    (0x5F748241, 0xCBA72510),
    (0x8B2E1481, 0x1D29AE20),
    (0x76006901, 0xBA84EC40),
    (0x1711D201, 0x79F01880),
    (0xBE67A401, 0x8793100),
    (0xDDDF4801, 0x6B566200),
    (0x3FFE9001, 0x803CC400),
    (0x90FD2001, 0xA6B98800),
    (0x65FA4001, 0xE6731000),
    (0xDBF48001, 0x30E62000),
    (0xF7E90001, 0xF1CC4000),
    (0xEFD20001, 0x23988000),
    (0xDFA40001, 0x47310000),
    (0xBF480001, 0x8E620000),
    (0x7E900001, 0x1CC40000),
    (0xFD200001, 0x39880000),
    (0xFA400001, 0x73100000),
    (0xF4800001, 0xE6200000),
    (0xE9000001, 0xCC400000),
    (0xD2000001, 0x98800000),
    (0xA4000001, 0x31000000),
    (0x48000001, 0x62000000),
    (0x90000001, 0xC4000000),
    (0x20000001, 0x88000000),
    (0x40000001, 0x10000000),
    (0x80000001, 0x20000000),
    (0x1, 0x40000000),
    (0x1, 0x80000000),
)


def lcrng_distance(state0: int, state1: int) -> int:
    """Efficiently compute the distance from LCRNG state0 -> state1"""
    mask = 1
    dist = 0

    for mult, add in JUMP_DATA:
        if state0 == state1:
            break

        if (state0 ^ state1) & mask:
            state0 = (state0 * mult + add) & 0xFFFFFFFF
            dist += mask

        mask <<= 1

    return dist


# Go to root/test of PyNXBot
import signal
import sys
import json

sys.path.append("../")

from nxbot import FRLGBot

config = json.load(open("../config.json"))
b = FRLGBot(config["IP"])


def signal_handler(signal, advances):  # CTRL+C handler
    print("Stop request")
    b.close()


signal.signal(signal.SIGINT, signal_handler)

initialSeed = b.getInitialSeed()
tempInitialSeed = initialSeed
tempCurrentSeed = initialSeed
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
    tempInitialSeed = b.getInitialSeed()
    currentSeed = b.getCurrentSeed()

    if tempInitialSeed != initialSeed:
        initialSeed = tempInitialSeed
        print("------------------------------------------\n")
        print(f"Initial Seed: {initialSeed:04X}")
        print()

    if tempCurrentSeed != currentSeed:
        print(f"Current Seed: {currentSeed:08X}")
        advances = lcrng_distance(initialSeed, currentSeed)
        print(f"Advances: {advances}")
        print()
        tempCurrentSeed = currentSeed

        if advances == 2558:
            for i in range(5):
                b.click("A")
                b.pause(0.1)

    """if botFlag and advances == targetAdvances:
            for i in range(5):
                b.click("A")
                b.pause(0.2)"""
