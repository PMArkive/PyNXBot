import os

class PKMString(object):
    def __init__(self, lang="en", gen=""):
        currentfolder = os.path.dirname(__file__)

        with open(f"{currentfolder}/text_Abilities_{lang}{gen}.txt", "r", encoding="utf8") as file:
            self.abilities = file.read().splitlines()

        with open(f"{currentfolder}/text_Natures_{lang}.txt", "r", encoding="utf8") as file:
            self.natures = file.read().splitlines()

        with open(f"{currentfolder}/text_Species_{lang}.txt", "r", encoding="utf8") as file:
            self.species = file.read().splitlines()

        with open(f"{currentfolder}/text_Moves_{lang}.txt", "r", encoding="utf8") as file:
            self.moves = file.read().splitlines()

        with open(f"{currentfolder}/text_Items_{lang}{gen}.txt", "r", encoding="utf8") as file:
            self.items = file.read().splitlines()

        with open(f"{currentfolder}/text_Types_{lang}.txt", "r", encoding="utf8") as file:
            self.types = file.read().splitlines()

        with open(f"{currentfolder}/text_Forms_{lang}.txt", "r", encoding="utf16") as file:
             self.forms = file.read().splitlines()

        if lang == "zh" or lang == "en": # for table
            with open(f"{currentfolder}/text_TRTypes_{lang}.txt", "r", encoding="utf8") as file:
                self.trtypes = file.read().splitlines()

            with open(f"{currentfolder}/text_TRMoves_{lang}.txt", "r", encoding="utf8") as file:
                self.trmoves = file.read().splitlines()

        if lang == "zh":
            with open(f"{currentfolder}/text_swsh_40000_{lang}.txt", "r", encoding="utf8") as file:
                self.locations = file.read().splitlines()

            with open(f"{currentfolder}/MoveData.txt", "r", encoding="utf8") as file:
                movedata = file.read().splitlines()

                import re
                self.movetypes = []
                self.movecats = []

                for move in movedata:
                    m = re.search(r"(\d+)\t(\d)", move)
                    self.movetypes.append(self.types[int(m.group(1))])
                    self.movecats.append(int(m.group(2)))
