import sys, json

# Go to root of PyNXBot
sys.path.append("../")

from structure import PK3
from nxbot import FRLGBot

config = json.load(open("../config.json"))
b = FRLGBot(config["IP"])

while True:
    pk3 = PK3(b.readWild())

    if pk3.isValid() and pk3.pid() != 0:
        print(pk3.toString())
    else:
        print("No battle started\n")

    stop = input("Check again? (y/n): ")
    print()

    if stop == "n" or stop == "N":
        b.close()
