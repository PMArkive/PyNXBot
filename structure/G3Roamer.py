from structure.ByteStruct import ByteStruct
from lookups import Util, GameVersion

class G3Roamer(ByteStruct):
    def __init__(self, buf, otid):
        self.data = bytearray(buf[:])
        self.OTID = otid

    def iv32(self):
        return self.getuint(0x0) & 0xFF  # Raomes IVs bug (RS/FRLG only)

    def ivs(self):
        iv32 = self.iv32()

        return [
            iv32 & 0x1F,
            (iv32 >> 5) & 0x1F,
            (iv32 >> 10) & 0x1F,
            (iv32 >> 20) & 0x1F,
            (iv32 >> 25) & 0x1F,
            (iv32 >> 15) & 0x1F,
        ]

    def pid(self):
        return self.getuint(0x4)

    def nature(self):
        return self.pid() % 25

    def shinyType(self):
        from structure import PK3

        return PK3.getShinyType(self.OTID, self.pid())

    def species(self):
        return Util(GameVersion.FRLG).GEN_3_SPECIES_MAP[self.getushort(0x8)]

    def hp(self):
        return self.getushort(0xA)

    def level(self):
        return self.getbyte(0xC)

    def status(self):
        return self.getbyte(0xD)

    def is_active(self):
        return self.getbyte(0x13)

    def toString(self):
        if self.is_active():
            shinytype = self.shinyType()
            shinyflag = "" if shinytype == 0 else "⋆  " if shinytype == 1 else "◇  "
            msg = f"PID: {self.pid():X}  " + shinyflag
            msg += f"{Util(GameVersion.FRLG).STRINGS.species[self.species()]}\n"
            msg += f"Nature: {Util(GameVersion.FRLG).STRINGS.natures[self.nature()]}\n"
            msg += f"IVs: {self.ivs()}\n"
            msg += f"Level: {self.level()}\n"
            msg += f"HP: {self.hp()}\n"
            msg += f"Status condition: {Util(GameVersion.FRLG).STRINGS.status[self.status()]}\n"

            return msg
        else:
            return "Roamer is not active"
