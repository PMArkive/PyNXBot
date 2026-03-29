from lookups import PKMString
from lookups.GameVersion import GameVersion
import os

class Util():
    def __init__(self, ver=GameVersion.SWSH, gen=""):
        from structure import PersonalTable
        self.STRINGS = PKMString(gen=gen)

        if ver == GameVersion.SWSH:
            self.path = "/../resources/bytes/personal_swsh"
        elif ver == GameVersion.FRLG:
            self.path = "/../resources/bytes/personal_rsefrlg"

        self.PT = PersonalTable(bytearray(open(os.path.dirname(__file__) + self.path, "rb").read()), ver=GameVersion.FRLG)
        self.GenderSymbol = ["♂","♀","-"]

    @staticmethod
    def translate(lang):
        Util.STRINGS = PKMString(lang)

    @staticmethod
    def convertImage(filename):
        import colorsys, numpy
        from PIL import Image
        image = Image.open(filename).convert("RGBA")
        h = image.height
        w = image.width
        pixels = numpy.array(image)
        hsv_array = numpy.empty(shape=(h, w, 5), dtype=float)

        for row in range(h):
            for column in range(w):
                rgb = pixels[row, column]
                hsv = colorsys.rgb_to_hsv(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255)
                hsv_array[row, column, 0] = hsv[0]
                hsv_array[row, column, 1] = hsv[1]
                hsv_array[row, column, 2] = hsv[2]
                hsv_array[row, column, 3] = rgb[3]

        return hsv_array

    @staticmethod
    def generatePallete(hsv_array, size=32):
        # Crop the image
        import numpy
        h , w , d = hsv_array.shape

        if h > size:
            top = (h - size) // 2
            bottom = h - size - top

            if hsv_array[:top, :, 3].any() or hsv_array[-bottom:, :, 3].any():
                print("Image is too large")

            hsv_array = hsv_array[top:-bottom, :, :]
            h = size

        if w > size:
            left = (w - size) // 2
            right = w - size - left

            if hsv_array[:, :left, 3].any() or hsv_array[:, -right:, 3].any():
                print("Image is too large")

            hsv_array = hsv_array[:, left:-right, :]
            w = size

        # Find all colors
        Colorlist = numpy.empty((0, 3), int)

        for r in range(h):
            if not hsv_array[r, :, 3].any():
                continue

            for c in range(w):
                hsv = hsv_array[r, c]

                if hsv[3] == 0:
                    continue

                HVB = Util.convert2HVB(hsv)
                idx = Util.findinlist(HVB, Colorlist)

                if idx < 0:
                    Colorlist = numpy.append(Colorlist, [HVB], axis = 0)
                    hsv_array[r, c, 4] = len(Colorlist) - 1
                else:
                    hsv_array[r, c, 4] = idx

        return Colorlist, hsv_array

    @staticmethod
    def convert2HVB(hsv):
        import math
        H = min(29, math.floor(hsv[0] * 30))
        V = min(14, math.floor(hsv[1] * 15))
        B = min(14, math.floor(hsv[2] * 15))

        return [H, V, B]

    @staticmethod
    def findinlist(element, nplist):
        import numpy

        for ii in range(len(nplist)):
            if numpy.array_equal(nplist[ii], element):
                return ii

        return -1

    GEN_3_SPECIES_MAP = [
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
        21,
        22,
        23,
        24,
        25,
        26,
        27,
        28,
        29,
        30,
        31,
        32,
        33,
        34,
        35,
        36,
        37,
        38,
        39,
        40,
        41,
        42,
        43,
        44,
        45,
        46,
        47,
        48,
        49,
        50,
        51,
        52,
        53,
        54,
        55,
        56,
        57,
        58,
        59,
        60,
        61,
        62,
        63,
        64,
        65,
        66,
        67,
        68,
        69,
        70,
        71,
        72,
        73,
        74,
        75,
        76,
        77,
        78,
        79,
        80,
        81,
        82,
        83,
        84,
        85,
        86,
        87,
        88,
        89,
        90,
        91,
        92,
        93,
        94,
        95,
        96,
        97,
        98,
        99,
        100,
        101,
        102,
        103,
        104,
        105,
        106,
        107,
        108,
        109,
        110,
        111,
        112,
        113,
        114,
        115,
        116,
        117,
        118,
        119,
        120,
        121,
        122,
        123,
        124,
        125,
        126,
        127,
        128,
        129,
        130,
        131,
        132,
        133,
        134,
        135,
        136,
        137,
        138,
        139,
        140,
        141,
        142,
        143,
        144,
        145,
        146,
        147,
        148,
        149,
        150,
        151,
        152,
        153,
        154,
        155,
        156,
        157,
        158,
        159,
        160,
        161,
        162,
        163,
        164,
        165,
        166,
        167,
        168,
        169,
        170,
        171,
        172,
        173,
        174,
        175,
        176,
        177,
        178,
        179,
        180,
        181,
        182,
        183,
        184,
        185,
        186,
        187,
        188,
        189,
        190,
        191,
        192,
        193,
        194,
        195,
        196,
        197,
        198,
        199,
        200,
        201,
        202,
        203,
        204,
        205,
        206,
        207,
        208,
        209,
        210,
        211,
        212,
        213,
        214,
        215,
        216,
        217,
        218,
        219,
        220,
        221,
        222,
        223,
        224,
        225,
        226,
        227,
        228,
        229,
        230,
        231,
        232,
        233,
        234,
        235,
        236,
        237,
        238,
        239,
        240,
        241,
        242,
        243,
        244,
        245,
        246,
        247,
        248,
        249,
        250,
        251,
        387,
        388,
        389,
        390,
        391,
        392,
        393,
        394,
        395,
        396,
        397,
        398,
        399,
        400,
        401,
        402,
        403,
        404,
        405,
        406,
        407,
        408,
        409,
        410,
        411,
        252,
        253,
        254,
        255,
        256,
        257,
        258,
        259,
        260,
        261,
        262,
        263,
        264,
        265,
        266,
        267,
        268,
        269,
        270,
        271,
        272,
        273,
        274,
        275,
        290,
        291,
        292,
        276,
        277,
        285,
        286,
        327,
        278,
        279,
        283,
        284,
        320,
        321,
        300,
        301,
        352,
        343,
        344,
        299,
        324,
        302,
        339,
        340,
        370,
        341,
        342,
        349,
        350,
        318,
        319,
        328,
        329,
        330,
        296,
        297,
        309,
        310,
        322,
        323,
        363,
        364,
        365,
        331,
        332,
        361,
        362,
        337,
        338,
        298,
        325,
        326,
        311,
        312,
        303,
        307,
        308,
        333,
        334,
        360,
        355,
        356,
        315,
        287,
        288,
        289,
        316,
        317,
        357,
        293,
        294,
        295,
        366,
        367,
        368,
        359,
        353,
        354,
        336,
        335,
        369,
        304,
        305,
        306,
        351,
        313,
        314,
        345,
        346,
        347,
        348,
        280,
        281,
        282,
        371,
        372,
        373,
        374,
        375,
        376,
        377,
        378,
        379,
        382,
        383,
        384,
        380,
        381,
        385,
        386,
        358,
    ]
