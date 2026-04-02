import sys, json

# Go to root of PyNXBot
sys.path.append("../")

from structure import PK3
from nxbot import FRLGBot

config = json.load(open("../config.json"))
b = FRLGBot(config["IP"])

while True:
    empty = True
    box = int(input("Which box would you like to check? "))
    print()

    for ii in range(1, 31):
        pk3 = PK3(b.readBox(box, ii))

        if pk3.isValid() and pk3.pid() != 0:
            print(f"Box: {box} Slot: {ii}")
            print(pk3.toString())
            empty = False

    if empty:
        print("Box is empty\n")

    stop = input("Continue? (y/n) ")

    if stop != "y" and stop != "Y":
        break

b.close()
