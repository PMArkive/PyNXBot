from nxbot import SWSHBot
from structure import Den

class RaidBot(SWSHBot):
    def __init__(self, ip, port=6000):
        SWSHBot.__init__(self, ip, port)
        from structure import EncounterNest8Archive, NestHoleDistributionEncounter8Archive
        buf = bytearray(open("../resources/bytes/local_raid", "rb").read())
        Den.LOCALTABLE = EncounterNest8Archive.GetRootAsEncounterNest8Archive(buf, 0)
        buf = self.readEventBlock_RaidEncounter("Event/Current/")
        Den.EVENTTABLE = NestHoleDistributionEncounter8Archive.GetRootAsNestHoleDistributionEncounter8Archive(buf, 0x20)
        self.resets = 0

    def setTargetDen(self, denId):
        self.denID = denId - 1

    def getDenData(self):
        return Den(self.readDen(self.denID))

    def getWatts(self, wattFarmer=False, speed=0):
        self.click("A")
        self.pause(1.5 - speed)
        self.click("A")
        self.pause(1.2 - speed)

        if wattFarmer:
            self.readWatts()

        self.click("A")
        self.pause(1.2)

        if not wattFarmer:
            self.saveGame()
        else:
            self.click("B")
            self.pause(0.2)
            self.click("B")
            self.pause(0.9)

    def setWatts(self, watts):
        self.Watts = watts

    def readWatts(self):
        from structure import MyStatus8
        newWatts = MyStatus8(self.read(0x45068FE8, 0x3)).currentWatts()
        diffWatts = newWatts - self.Watts
        self.Watts = newWatts
        print(f"Watts: {newWatts} (+{diffWatts})")

    def throwPiece(self):
        # A on den
        self.click("A")
        print("A on den")
        self.pause(0.5)
        self.click("A")
        self.pause(1.3)
        # Throw whishing piece
        self.click("A")
        print("Throw Wishing Piece in den")
        self.pause(1.4)
        # Save
        self.click("A")
        print("Saving...")
        self.pause(1)
        # Home
        self.click("HOME")
        print("HOME clicked")
        self.pause(0.5)
