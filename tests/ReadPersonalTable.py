import sys

# Go to root of PyNXBot
sys.path.append("../")

from lookups import Util, GameVersion


print(
    Util(GameVersion.SWSH).STRINGS.abilities[
        Util(GameVersion.SWSH).PT.getFormeEntry(869, 2).Ability1()
    ]
)
print(
    Util(GameVersion.FRLG).STRINGS.abilities[
        Util(GameVersion.FRLG).PT.getFormeEntry(385, 0).Ability1()
    ]
)
