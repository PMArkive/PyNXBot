# A button Spammer Bot

import signal, sys, json

# Go to root/test of PyNXBot
sys.path.append("../")

from nxbot import Cram_o_Matic

# CTRL+C handler
def signal_handler(signal, frame):
    print()
    print("Stop request")
    b.close()

signal.signal(signal.SIGINT, signal_handler)

config = json.load(open("../config.json"))
b = Cram_o_Matic(config["IP"])

apricorns = input("Are you using Cram-o-Matic machine? (y/n): ")

if apricorns == "y" or apricorns == "Y":
    apricorns = True
else:
    apricorns = False

b.pause(0.5)

while True:
    print("A spamming...\n")

    while True:
        if apricorns:
            if (b.endApricornsCheck(apricorns)) or b.endApricornsCheck():
                break

        b.click("A")
        b.pause(0.5)

    print()
    stop = input("Continue spamming? (y/n): ")

    if stop == "n" or stop == "N":
        break
    else:
        apricorns = input("Are you using Cram-o-Matic machine? (y/n): ")

        if apricorns == "y" or apricorns == "Y":
            apricorns = True
        else:
            apricorns = False

print("A spamming ended")
print()
b.close()
