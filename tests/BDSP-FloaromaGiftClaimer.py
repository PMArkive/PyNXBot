import signal, sys, json

# Go to root/test of PyNXBot
sys.path.append("../")

from rng import XORSHIFT
from nxbot import BDSPBot


# CTRL+C handler
def signal_handler(signal, advances):
    print("Stop request")
    b.close()


signal.signal(signal.SIGINT, signal_handler)

config: dict = json.load(open("../config.json"))
b = BDSPBot(config["IP"])

r = XORSHIFT(b.getSeed())
seed: list = r.state()
advances = 0
print("Initial Seed")
print(
    f"S[0]: {seed[0]:08X}\tS[1]: {seed[1]:08X}\nS[2]: {seed[2]:08X}\tS[3]: {seed[3]:08X}"
)
print()
print(f"Advances: {advances}\n\n")

userInput: str = input("Press A at a specific advance? (y/n) ")

if userInput == "y" or userInput == "Y":
    botFlag = True
    userAdvances: str = input("Input the target advances separated by a space: ")
    targetAdvances: list = sorted(
        [int(i) for i in userAdvances.split(" ") if i.isdigit()]
    )

    # Variables for conversation timeline
    conversationStarted = False
    remainder = divmod(targetAdvances[0], 41)[1]
    startConversation: list = [remainder]

    # Identify when to begin the conversation, every possible starting point is generated to start talking to NPC as soon
    # as pokedex advances stop to prevent fidgets. THIS IS CRITICAL.
    for conversationTarget in startConversation:
        if conversationTarget + 41 < targetAdvances[0] - 500:
            startConversation.append(conversationTarget + 41)

    # Variable to handle progression of conversation
    conversationProgressed = False

    # Dexscrolling Variables
    dexOpened = False
    dexScrolled = False
    trainercardOpened = False
    scrolls = 0
else:
    botFlag = False

print("\n")

while True:
    currSeed = b.getSeed()

    while r.state() != currSeed:
        r.next()
        advances += 1

        if r.state() == currSeed:
            print("Current Seed")
            print(
                f"S[0]: {currSeed[0]:08X}\tS[1]: {currSeed[1]:08X}\nS[2]: {currSeed[2]:08X}\tS[3]: {currSeed[3]:08X}"
            )
            print()
            print(f"Advances: {advances}\n\n")

            if botFlag:
                # Stops pokedex being opened before game loads save file
                if advances > 60:
                    # Avoid advancing too far with Pokedex
                    if advances <= targetAdvances[0] - 1500:
                        # Open Pokedex
                        if not dexOpened:
                            print(f"Opening pokedex to advance...\n\n")
                            b.click("X")
                            b.pause(0.9)
                            b.click("A")
                            b.pause(1.2)
                            b.click("R")
                            b.pause(1.5)
                            dexOpened = True

                        # Scroll Dex
                        if dexOpened:
                            print(f"Pokedex scrolled {scrolls} times\n\n")
                            scrolls += 1
                            b.click("DRIGHT")
                            b.pause(0.1)

                    if advances >= targetAdvances[0] - 1500:
                        if not conversationStarted:
                            # Close Dex
                            if dexOpened:
                                print(f"Closing pokedex...\n\n")
                                b.click("B")
                                b.pause(0.9)
                                b.click("B")
                                b.pause(0.9)
                                dexOpened = False
                                dexScrolled = True

                            # Try to start conversation some multiple of 41 before target, MUST HAPPEN ASAP after pokedex closed
                            if dexScrolled:
                                for conversationTarget in startConversation:
                                    if advances < conversationTarget:
                                        break

                                    if advances == conversationTarget and advances > 30:
                                        b.click("A")
                                        print(
                                            f"Conversation started on advance {conversationTarget}!\n\n"
                                        )
                                        conversationStarted = True

                                    if advances > conversationTarget:
                                        startConversation.remove(conversationTarget)

                        if conversationStarted:
                            # Progress conversation to generation stage
                            if not conversationProgressed:
                                b.pause(1.45)
                                b.click("A")
                                b.pause(1.45)
                                b.click("A")
                                b.pause(1.45)
                                b.click("A")
                                conversationProgressed = True

                            # Try to hit target
                            if conversationProgressed:
                                if len(targetAdvances) > 0:
                                    for currentTarget in targetAdvances:
                                        if advances < currentTarget:
                                            break

                                        if advances == currentTarget:
                                            for i in range(5):
                                                b.click("A")
                                                b.pause(0.2)

                                            print(f"We hit {currentTarget}!\n\n")
                                            b.close()

                                        if advances > currentTarget:
                                            targetAdvances.remove(currentTarget)

            if len(targetAdvances) == 0 or targetAdvances[-1] < advances:
                print("Missed all potential targets.\n")
                b.close()
