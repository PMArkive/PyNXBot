import sys, json

# Go to root of PyNXBot
sys.path.append("../")

from structure import PK3
from nxbot import FRLGBot

config = json.load(open("../config.json"))
b = FRLGBot(config["IP"])

for ii in range(1, 7):
    print(f"Slot: {ii}")
    pk3 = PK3(b.readParty(ii))

    if pk3.isValid() and pk3.pid() != 0:
        print(pk3.toString())
    else:
        print("Empty")

print()
b.close()
