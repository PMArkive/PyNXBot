from structure.ByteStruct import ByteStruct


class MyStatus3(ByteStruct):
    def OTID(self):
        return self.getuint(0xA)

    def TID(self):
        return self.getushort(0xA)

    def SID(self):
        return self.getushort(0xC)

    def TSV(self):
        return (self.TID() ^ self.SID()) >> 4
