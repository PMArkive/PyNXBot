class LCRNG(object):
    def __init__(self, seed):
        self.initial_seed = seed
        self.seed = seed

    def initial_state(self):
        return self.initial_seed

    def state(self):
        return self.seed

    def next(self, mul=0x41C64E6D, add=0x6073):
        self.seed = (self.seed * mul + add) & 0xFFFFFFFF

        return self.seed

    def lcrng_distance(self, state):
        mask = 1
        dist = 0

        for mult, add in LCRNG.JUMP_DATA:
            if self.seed == state:
                break

            if (self.seed ^ state) & mask:
                self.next(mult, add)
                dist += mask

            mask <<= 1

        return dist

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
