from structure.ByteStruct import ByteStruct
from lookups import Util, GameVersion

class PK3(ByteStruct):
    STOREDSIZE = 0x50
    PARTYSIZE = 0x64
    BLOCKSIZE = 0xC

    def __init__(self,buf):
        self.data = bytearray(buf[:])
        if self.isEncrypted():
            self.decrypt()

    def pid(self):
        return self.getuint(0x0)

    def nature(self):
        return self.pid() % 25

    def sidtid(self):
        return self.getuint(0x04)

    def language(self):
        return self.getbyte(0x12)

    def miscflags(self):
        return self.getbyte(0x13)

    def checksum(self):
        return self.getushort(0x1C)

    def species(self):
        return Util(GameVersion.FRLG).GEN_3_SPECIES_MAP[self.getushort(0x20)]

    def helditem(self):
        return self.getushort(0x22)

    def gender(self):
        if Util(GameVersion.FRLG).PT.getGen3GenderThreshold(self.species()) == 0:
            return 0
        elif Util(GameVersion.FRLG).PT.getGen3GenderThreshold(self.species()) == 254:
            return 1
        elif Util(GameVersion.FRLG).PT.getGen3GenderThreshold(self.species()) == 255:
            return 2
        elif self.pid() & 255 >= Util(GameVersion.FRLG).PT.getGen3GenderThreshold(self.species()):
            return 0
        else:
            return 1

    def evs(self):
        return [self.data[0x38],self.data[0x39],self.data[0x3A],self.data[0x3C],self.data[0x3D],self.data[0x3B]]

    def move1(self):
        return self.getushort(0x2C)

    def move2(self):
        return self.getushort(0x2E)

    def move3(self):
        return self.getushort(0x30)

    def move4(self):
        return self.getushort(0x32)

    def ball(self):
        return (self.getushort(0x46) >> 11) & 15

    def iv32(self):
        return self.getuint(0x48)

    def battleStats(self): # Lv,HP,Atk,Def,SpA,SpD,Spe
        return self.getbyte(0x54),self.getushort(0x56),self.getushort(0x5A),self.getushort(0x5C),self.getushort(0x60),self.getushort(0x62),self.getushort(0x5E)

    def isEgg(self):
        return ((self.iv32() >> 30) & 1) == 1

    def abilityNum(self):
        return ((self.iv32() >> 31) & 1)

    def ability(self):
        return Util(GameVersion.FRLG).PT.getGen3Abilities(self.species())[self.abilityNum()]

    def ivs(self):
        iv32 = self.iv32()
        return [iv32 & 0x1F, (iv32 >> 5) & 0x1F, (iv32 >> 10) & 0x1F, (iv32 >> 20) & 0x1F, (iv32 >> 25) & 0x1F, (iv32 >> 15) & 0x1F]

    def calChecksum(self):
        chk = 0
        for i in range(32,PK3.STOREDSIZE,2):
            chk += self.getushort(i)
            chk &= 0xFFFF
        return chk

    @staticmethod
    def getShinyType(otid,pid):
        xor = (otid >> 16) ^ (otid & 0xFFFF) ^ (pid >> 16) ^ (pid & 0xFFFF)
        if xor > 15:
            return 0
        else:
            return 2 if xor == 0 else 1

    def shinyType(self):
        return self.getShinyType(self.sidtid(),self.pid())

    def shinyString(self):
        return 'None' if self.shinyType() == 0 else 'Star' if self.shinyType() == 1 else 'Square'

    def save(self,filename):
        with open(f'{filename}.pk3','wb') as fileOut:
            fileOut.write(self.data)

    def toString(self):
        if self.isValid():
            shinytype = self.shinyType()
            shinyflag = '' if shinytype == 0 else '⋆  ' if shinytype == 1 else '◇  '
            msg = f'PID: {self.pid():X}  ' + shinyflag
            msg += f"{Util(GameVersion.FRLG).STRINGS.species[self.species()]}\n"
            msg += f'Held item: {Util(GameVersion.FRLG,gen="_3rd").STRINGS.items[self.helditem()]}\n'
            msg += f"Nature: {Util(GameVersion.FRLG).STRINGS.natures[self.nature()]}  "
            msg += f"Ability: {Util(GameVersion.FRLG,gen="_3rd").STRINGS.abilities[self.ability()]} ({self.abilityNum()})  "
            msg += f"Gender: {Util(GameVersion.FRLG).GenderSymbol[self.gender()]}\n"
            msg += f"IVs: {self.ivs()}  EVs: {self.evs()}\n"
            msg += f"Moves: {Util(GameVersion.FRLG).STRINGS.moves[self.move1()]} / {Util(GameVersion.FRLG).STRINGS.moves[self.move2()]} / {Util(GameVersion.FRLG).STRINGS.moves[self.move3()]} / {Util(GameVersion.FRLG).STRINGS.moves[self.move4()]}\n"
            return msg
        else:
            return 'Invalid Data'
    
    def isBadEgg(self):
        self.miscflags() & 1 != 0

    def isValid(self):
        return self.checksum() == self.calChecksum() and not self.isBadEgg()

    def isEncrypted(self):
        return self.checksum() != self.calChecksum()

    def decrypt(self):
        pid = self.pid()
        sidtid = self.sidtid()
        seed = pid ^ sidtid
        self.__cryptPKM__(seed)
        self.__shuffle__(pid % 24)

    def __cryptPKM__(self, seed):
        self.__crypt__(seed, 32, PK3.STOREDSIZE)
        if len(self.data) == PK3.PARTYSIZE:
            self.__crypt__(seed, PK3.STOREDSIZE, PK3.PARTYSIZE)

    def __crypt__(self, seed, start, end):
        i = start
        while i < end:
            self.data[i] ^= (seed & 0xFF)
            self.data[i + 1] ^= (seed >> 8) & 0xFF
            self.data[i + 2] ^= (seed >> 16) & 0xFF
            self.data[i + 3] ^= (seed >> 24) & 0xFF
            i += 4

    def __shuffle__(self, sv):
        idx = 4 * sv
        sdata = bytearray(self.data[:])
        for block in range(4):
            ofs = PK3.BLOCKPOSITION[idx + block]
            self.data[32 + PK3.BLOCKSIZE * block : 32 + PK3.BLOCKSIZE * (block + 1)] = sdata[32 + PK3.BLOCKSIZE * ofs : 32 + PK3.BLOCKSIZE * (ofs + 1)]

    def refreshChecksum(self):
        self.setushort(0x1C, self.calChecksum())

    def encrypt(self):
        self.refreshChecksum()
        pid = self.pid()
        sidtid = self.sidtid()
        seed = pid ^ sidtid

        self.__shuffle__(PK3.blockPositionInvert[pid % 24])
        self.__cryptPKM__(seed)
        return self.data

    blockPositionInvert = [
        0, 1, 2, 4, 3, 5, 6, 7, 12, 18, 13, 19, 8, 10, 14, 20, 16, 22, 9, 11, 15, 21, 17, 23,
        0, 1, 2, 4, 3, 5, 6, 7, # duplicates of 0-7 to eliminate modulus
    ]

    BLOCKPOSITION = [
        0, 1, 2, 3,
        0, 1, 3, 2,
        0, 2, 1, 3,
        0, 3, 1, 2,
        0, 2, 3, 1,
        0, 3, 2, 1,
        1, 0, 2, 3,
        1, 0, 3, 2,
        2, 0, 1, 3,
        3, 0, 1, 2,
        2, 0, 3, 1,
        3, 0, 2, 1,
        1, 2, 0, 3,
        1, 3, 0, 2,
        2, 1, 0, 3,
        3, 1, 0, 2,
        2, 3, 0, 1,
        3, 2, 0, 1,
        1, 2, 3, 0,
        1, 3, 2, 0,
        2, 1, 3, 0,
        3, 1, 2, 0,
        2, 3, 1, 0,
        3, 2, 1, 0,

        # duplicates of 0-7 to eliminate modulus
        0, 1, 2, 3,
        0, 1, 3, 2,
        0, 2, 1, 3,
        0, 3, 1, 2,
        0, 2, 3, 1,
        0, 3, 2, 1,
        1, 0, 2, 3,
        1, 0, 3, 2,
    ]
