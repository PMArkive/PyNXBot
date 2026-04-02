import sys, json

# Go to root of PyNXBot
sys.path.append("../")

from nxbot import FRLGBot
from structure import G3Roamer

config = json.load(open("../config.json"))
b = FRLGBot(config["IP"])

while True:
    roamer3 = G3Roamer(b.readRoamerBlock(), b.TrainerSave.OTID())
    print(roamer3.toString())
    stop = input("Check again? (y/n): ")
    print()

    if stop == "n" or stop == "N":
        b.close()
