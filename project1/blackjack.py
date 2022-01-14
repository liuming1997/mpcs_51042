"""
MPCS 51042 Project 1

Ming Liu

How to Play:

The main file should execute itself from the command line, without further inputs. On UNIX systems it has also been marked as executable.
Acceptable commands during a round: hit (gives you another card), stand (ends your turn) - any other argument assumes 'stand'.
Acceptable arguments after a round: y (play again), n (do not play again) - any other argument assumes 'n'.

At the end of each round, the game displays who won, with what score, and asks the human players to collectively make ONE decision as to whether or not to play again.
This program supports just having computer players, too; if that is the case, it asks a human if it should simulate another round.

Note: This program, if you hit 21, stops for you. You can't decide to lose at 21. Primitive idiot-proofing.

AI Types, in further detail:

Standard AI simply looks at the cards in hand, with a threshold for points, which for the dealer is fixed, and for everyone else is randomly generated.
If it has less points than the threshold, it hits; else, it stands.
(Thinker and Prescient AI don't use this threshold value.)

Thinker AI knows the contents of the deck, but not the next card. It also knows all of the face-up cards, and attempts to calculate the probability of 'friendly' cards.
It then compares the probability of not busting to a randomly generated threshold probability between 0.5 and 0.75; if the probability of not busting is higher, it hits.

Gambler AI is like Thinker, but uses expected value of the cards instead of threshold probability.

Prescient AI knows its own hand and the top card off the deck. If it would bust, it stands; else, it hits. Thus, the prescient AI should never bust, but it may stand early.

I thought about making a cheater AI that simply shuffles the deck until it gets the card it wants, but that took too much time.
And as they said in Casino, "cheater's justice". Fortunately for the computer I lack a metaphorical hammer.
"""

#!/usr/bin/env python

import random
import uuid
from abc import ABC, abstractmethod
import sys
import itertools



# Constructs the deck dictionary, which is a list of all the cards and their point values. Aces have two point values, so they get a list.
# No points for elegance here.
masterDeck = {
    "ace_spades" : [1, 11],
    "two_spades": 2,
    "three_spades": 3,
    "four_spades": 4,
    "five_spades": 5,
    "six_spades": 6,
    "seven_spades": 7,
    "eight_spades": 8,
    "nine_spades": 9,
    "ten_spades": 10,
    "jack_spades": 10,
    "queen_spades": 10,
    "king_spades": 10,
    "ace_clubs" : [1, 11],
    "two_clubs": 2,
    "three_clubs": 3,
    "four_clubs": 4,
    "five_clubs": 5,
    "six_clubs": 6,
    "seven_clubs": 7,
    "eight_clubs": 8,
    "nine_clubs": 9,
    "ten_clubs": 10,
    "jack_clubs": 10,
    "queen_clubs": 10,
    "king_clubs": 10,
    "ace_hearts" : [1, 11],
    "two_hearts": 2,
    "three_hearts": 3,
    "four_hearts": 4,
    "five_hearts": 5,
    "six_hearts": 6,
    "seven_hearts": 7,
    "eight_hearts": 8,
    "nine_hearts": 9,
    "ten_hearts": 10,
    "jack_hearts": 10,
    "queen_hearts": 10,
    "king_hearts": 10,
    "ace_diamonds" : [1, 11],
    "two_diamonds": 2,
    "three_diamonds": 3,
    "four_diamonds": 4,
    "five_diamonds": 5,
    "six_diamonds": 6,
    "seven_diamonds": 7,
    "eight_diamonds": 8,
    "nine_diamonds": 9,
    "ten_diamonds": 10,
    "jack_diamonds": 10,
    "queen_diamonds": 10,
    "king_diamonds": 10,
}
"""
masterDeck: dict (global)
A dictionary of all of the point values of the cards.
"""

# AI types.
# Standard follows the dealer, but has varying thresholds for when to hit and stand.
# Thinker attempts to guess the cards in the deck based on the cards it can see, a very primitive card counter. It knows the contents of the deck.
# Gambler just uses expected value of the cards in the deck.
# Prescient knows the next card off the top of the deck, to be found later.
# Note that thinkers don't keep a RUNNING count of cards they've seen, just cards that are visible right now. They're pretty bad.
aiTypes = ["standard", "thinker", "gambler"]
"""
aiTypes: list (global)
A list of the three main AI types. There is a fourth, documentened above as 'prescient', which will show up later.
"""

# Names for computer players.
# Taken from a list of NPCs from my last tabletop campaign / novel writing project.
# Note: There are only so many names in this list; if you have n players where n > len(nameList) you have collisions, which is why each player also gets a UUID.
# Also sometimes you still get collisions anyways, because of random.choice(), which when called once in a for loop, can't sample without replacement.
# But are you ever going to have that many people playing the same game of Blackjack?
# In theory, uuid and name can both collide, but since uuid4 is 128 bits you'll experience the heat death of the universe before a double collision.
nameList = ["Artyom", "Anna", "Vera", "Alisa", "Annika", "Anton", "Roman", "Yulia", "Stanislav",
            "Raye", "Clint", "Elena", "Karl", "Sakura", "Marina", "Boris", "Vasily", "Astra", "Raisa", "Ludmilla",
            "Peter", "Lili", "Natasha", "Kai", "Tsecha", "Edward", "Tycho", "Emma", "Selene", "Clara", "Ciel", "Emilia", "Yasmin"]
"""
nameList: list (global)
List of names for computer players. Note that collisions may occur when picking a name. Names were drawn from a previous tabletop campaign that I ran.
"""

leaderboard = {}

"""
leaderboard: dict (global)
Dictionary of the players, to keep a running score count, of the format [player.uuid : [player.name, player.timesWon]] for each player.
    Due to the rather late-stage implementation of this feature, it may not work.
"""

class Card:
    """
    The Card class stores a few values for each individual card, such as its name, rank, and suit.

    Parameters:
    -----------
    value: int or list
            int if the card is not an ace, list [1, 11] if it is.
        suit: str
            the suit of the card
        rank: str
            the common name of the card (e.g. 'ace', 'two', 'queen', etc.)
    """
    def __init__(self, rank : str, suit : str, value):
        """
        Constructor for a new card:

        Parameters:
        -----------
        value: int or list
            int if the card is not an ace, list [1, 11] if it is.
        suit: str
            the suit of the card
        rank: str
            the common name of the card (e.g. 'ace', 'two', 'queen', etc.)
        
        Returns:
        --------
        This function returns nothing.
        """
        self.rank = rank
        self.suit = suit
        self.value = value

    def pointValue(self):
        """
        Gives you the point value of a card.

        Returns:
        --------
        Either int or list based on the particular card, list if ace.
        """
        return self.value

    def __repr__(self):
        """
        Prints the common name of the card, e.g. "Queen of Hearts".

        Returns:
        --------
        String
        """
        return str(self.rank.capitalize() + " of " + self.suit.capitalize())

class Deck:
    """
    The Deck class is a collection of Cards.
    
    Parameters:
    -----------
    deckList: list(Card)
        The master deck list, holding Cards.
    """
    def __init__(self):
        """
        Constructor; creates an empty list that will be populated by Card objects.

        Returns:
        --------
        This function returns nothing.
        """
        self.deckList = []

    def shuffle(self):
        """
        Sometimes it is necessary to shuffle a deck; this function does so.

        Returns:
        --------
        This function returns nothing.
        """
        random.shuffle(self.deckList)

    def generate(self):
        """
        Populates deckList with 52 cards, one for each card in masterDeck.

        Returns:
        --------
        This function returns nothing.
        """
        for card in masterDeck:
            names = card.split("_")
            self.deckList.append(Card(names[0], names[1], masterDeck.get(card)))
            Deck.shuffle(self)
        return self.deckList

    def addCards(self):
        """
        Adds 52 new cards as needed, calling generate().

        Returns:
        --------
        This function returns nothing.
        """
        self.deckList.append(Deck.generate(self))

    def removeCard(self, card):
        """
        Testing function left over from before, but I didn't have time to go back and remove it.

        Returns:
        --------
        This function returns nothing.
        """
        try:
            self.deckList.remove(Deck.generate(card))
        except:
            pass

    def drawCard(self):
        """
        Draw a card, returns that card, removes that card from the decklist.

        Returns:
        --------
        Returns a Card object from the first element of deckList.
        """
        draw = self.deckList[0]
        self.deckList = self.deckList[1:]
        return draw

    def deckCheck(self):
        """
        Calls addCards() as needed, if deckList is empty because you drew all the cards.

        Returns:
        --------
        This function returns nothing.
        """
        if len(self.deckList) == 0:
            self.addCards()

# deck for the game
# generate a deck
deck = Deck()
deck.generate()
"""
Deck: Deck
Generates the main deck that will be used in the game.
"""

# count the number of human players
peopleCount = 0
"""
peopleCount: int
Counts the human players.
"""

# list of face up cards, used later
publicInfo = []
"""
publicInfo: list
List of Card objects that will be used for the computer AI.
"""

class Player(ABC):
    """
    The basic, abstract Player class. HumanPlayer and ComputerPlayer inherit from it.
    """
    def __init__(self) -> None:
        """
        Dummy constructor.

        Returns:
        --------
        This function returns nothing.
        """
        super().__init__()
    
    @abstractmethod
    def action(self):
        """
        Dummy function, to be used later.

        Returns:
        --------
        This function returns nothing.
        """
        pass
    @abstractmethod
    def hit(self):
        """
        Dummy function, to be used later.

        Returns:
        --------
        This function returns nothing.
        """
        pass
    @abstractmethod
    def stand(self):
        """
        Dummy function, to be used later.

        Returns:
        --------
        This function returns nothing.
        """
        pass
    @abstractmethod
    def reset(self):
        """
        Dummy function, to be used later.

        Returns:
        --------
        This function returns nothing.
        """
        pass

class HumanPlayer(Player):
    """
    The HumanPlayer class, inheriting from Player. Used for human players.
    """
    def __init__(self):
        """
        uuid: uuid
            A unique identifier for each player.
        isHuman: bool
            True if human player, False otherwise.
        name: str
            Name of the player.
        points: list
            List of all possible point values of the player's cards.
        won: bool
            True if 21 points, False otherwise.
        lost: bool
            True if > 21 points, False otherwise.
        done: bool
            True if the player elects to stand, False other wise.
        hand: list
            List of Card objects in the player's hand.
        timesWon: int
            Number of times the player has won.
        final: int
            Final value of the player's hand, if not busted.
        bust: int
            Value of the player's hand, if busted.

        Returns:
        --------
        This function returns nothing.
        """
        global peopleCount
        global leaderboard
        peopleCount += 1
        self.uuid = uuid.uuid4()
        self.isHuman = True
        self.name = input("Player " + str(peopleCount) + ", please input your name: ")
        leaderboard[str(self.uuid)] = [self.name, 0]
        self.points = []
        self.won = False
        self.lost = False
        self.done = False
        self.hand = []
        self.timesWon = 0
        self.final = 0
        self.bust = 0

    def hit(self):
        """
        Adds a card to self.hand.

        Returns:
        --------
        This function returns nothing.
        """
        global deck
        deck.deckCheck()
        newCard = deck.drawCard()
        # calculate the point value of your new hand
        self.hand.append(newCard)
        if type(newCard.value) != list:
            print("\tYou have drawn a " + str(newCard).lower() + " (" + str(newCard.value) + " points).\n")
            newCard.value = [newCard.value]
        else:
            print("\tYou have drawn an " + str(newCard).lower() + " (1 or 11 points).\n")
        print("Your new hand is: ")
        for card in self.hand:
            if type(card.value) == list and card.value == [1, 11]:
                print("\t" + str(card) + " (1 or 11 points)")
            else:
                if len(str(card.value)) > 2:
                    print("\t" + str(card) + " (" + str(card.value)[1:-1] + " points)")
                else:
                    print("\t" + str(card) + " (" + str(card.value) + " points)")
        # calculate every possible combination of point values
        pointPermutations = self.points
        pointCombinations = []
        if len(self.points) == 1:
            for i in newCard.value:
                pointCombinations.append(self.points[0] + i)
        else:
            pointPermutations = [list(zip(permutation, newCard.value)) for permutation in itertools.permutations(self.points, len(newCard.value))]
            for pair in pointPermutations:
            # this is just try/except abuse
                try:
                    pointCombinations.append(int(pair[0] + pair[1]))
                except: 
                    pointCombinations.append(int(pair[0][0] + pair[0][1]))

        # calculate whether or not you busted
        if min(pointCombinations) > 21:
            self.bust = int(max(pointCombinations))
            self.lost = True
        # if the value of your hand is exactly 21, stops for you
        elif 21 in pointCombinations:
            self.won = True
        else:
            # remove all values > 21
            pointCombinations[:] = [x for x in pointCombinations if x < 21]
            if len(pointCombinations) == 1:
                print("\tYour new hand is worth " + str(pointCombinations[0]) + " points.")
            else:
                points = ""
                for i in pointCombinations:
                    points += (str(i) + " or ")
                points = points[:-4]
                print("\tYour new hand is worth " + points + " points.")
        self.points = pointCombinations

    def stand(self):
        """
        Makes the player stand.

        Returns:
        --------
        This function returns nothing.
        """
        self.final = max(self.points)
        self.done = True

    def action(self):
        """
        Main decision-making loop. Calls hit() if the player elects to hit, stand() otherwise, but first calculates if the player has busted.

        Returns:
        --------
        This function returns nothing.
        """
        print("\n")
        if self.won:
            print("Your hand is worth 21 points; automatically standing for you.")
        elif self.lost:
            print("You have busted, with " + str(self.bust) + " points.")
        elif self.done:
            print("You have elected to stand, with " + str(self.final) + " points.")
        else:
            print("\n")
            choice = input("Would you like to hit or stand? ")
            if choice.lower() == "hit":
                HumanPlayer.hit(self)
            else:
                HumanPlayer.stand(self)
            return HumanPlayer.action(self)

    def reset(self):
        """
        Resets the player's attributes for the next round.
        """
        self.points = []
        self.won = False
        self.lost = False
        self.done = False
        self.hand = []

class ComputerPlayer(Player):
    """
    The ComputerPlayer class, for all computer players.
    """
    def __init__(self, name="notDealer", threshold=0, aitype="standard"):
        """
        uuid: uuid
            A unique identifier for each player.
        isHuman: bool
            True if human player, False otherwise.
        name: str
            Name of the player.
        points: list
            List of all possible point values of the player's cards.
        won: bool
            True if 21 points, False otherwise.
        lost: bool
            True if > 21 points, False otherwise.
        done: bool
            True if the player elects to stand, False other wise.
        hand: list
            List of Card objects in the player's hand.
        timesWon: int
            Number of times the player has won.
        final: int
            Final value of the player's hand, if not busted.
        bust: int
            Value of the player's hand, if busted.
        aiType: str
            String literal of the computer's AI type.

        Returns:
        --------
        This function returns nothing.
        """
        self.uuid = uuid.uuid4()
        self.isHuman = False
        self.points = []
        self.won = False
        self.lost = False
        self.done = False
        self.hand = []
        self.timesWon = 0
        self.final = 0
        self.bust = 0
        # for the dealer only
        if name == "Dealer" and threshold == 17:
            self.name = name
            self.threshold = int(threshold)
            self.aitype = aitype
        else:
            self.name = random.choice(nameList)
            leaderboard[str(self.uuid)] = [self.name, 0]
            self.threshold = random.randint(14,18)
            # in the tabletop campaign, these characters could cast magic, so here they get to see the next card off the top of the deck
            if self.name in ["Vera", "Lili", "Emma", "Selene", "Clara", "Ciel"]:
                self.aitype = "prescient"
            # if not, just pick one at random between standard and thinker
            else:
                self.aitype = random.choice(aiTypes)

    def hit(self):
        """
        Adds a card to self.hand.

        Returns:
        --------
        This function returns nothing.
        """
        global deck
        deck.deckCheck()
        newCard = deck.drawCard()
        # calculate the point value of the new hand
        self.hand.append(newCard)
        if type(newCard.value) != list:
            print("\n" + self.name + " has drawn a " + str(newCard).lower() + " (" + str(newCard.value) + " points).\n")
            newCard.value = [newCard.value]
        else:
            print("\n" + self.name + " has drawn an " + str(newCard).lower() + " (1 or 11 points).\n")
        print("Their new hand is: ")
        if self.name != "Dealer":
            for card in self.hand:
                if type(card.value) == list:
                    print("\t" + str(card) + " (1 or 11 points)")
                else:
                    print("\t" + str(card) + " (" + str(card.value) + " points)")
        elif self.name == "Dealer":
            for i in range(len(self.hand)):
                if i == 1:
                    print("\t[hidden card]")
                else:
                    if type(self.hand[i].value) == list and self.hand[i].value == [1, 11]:
                        print("\t" + str(self.hand[0]) + " (1 or 11 points)")
                    else:
                        print("\t" + str(self.hand[0]) + " (" + str(self.hand[0].value) + " points)")
        # calculate every possible combination of point values
        pointPermutations = self.points
        pointCombinations = []
        if len(self.points) == 1:
            for i in newCard.value:
                pointCombinations.append(self.points[0] + i)
        else:
            pointPermutations = [list(zip(permutation, newCard.value)) for permutation in itertools.permutations(self.points, len(newCard.value))]
            for pair in pointPermutations:
            # this is just try/except abuse
                try:
                    pointCombinations.append(int(pair[0] + pair[1]))
                except: 
                    pointCombinations.append(int(pair[0][0] + pair[0][1]))
        # calculate whether or not the computer busted
        if min(pointCombinations) > 21:
            self.bust = int(max(pointCombinations))
            self.lost = True
        # if the value of the hand is exactly 21, stop
        elif 21 in pointCombinations:
            self.won = True
        else:
            # remove all values > 21
            pointCombinations[:] = [x for x in pointCombinations if x < 21]
        self.points = pointCombinations

    def stand(self):
        """
        Makes the computer stand.

        Returns:
        --------
        This function returns nothing.
        """
        self.final = max(self.points)
        self.done = True

    def think(self):
        """
        The main decisionmaking process for the computer.
        Calls hit() and stand() as needed.

        Returns:
        --------
        This function returns nothing.
        """
        global deck
        global publicInfo
        if self.points == 21:
            self.won = True
        else:
            if self.aitype == "standard":
                while max(self.points) < self.threshold and self.done == False and self.lost == False:
                    ComputerPlayer.hit(self)
                ComputerPlayer.stand(self)
            elif self.aitype == "thinker":
                stackedDeck = deck
                knowledge = publicInfo
                knowledge.append(self.hand[1])
                # generate a random "probability of success": if the cards in the deck have more than a certain percentage of success, hit
                thresholdProbability = random.uniform(0.5, 0.75)
                for card in knowledge:
                    stackedDeck.removeCard(card)
                sampleSpace = len(stackedDeck.deckList)
                probabilitySpace = []
                for card in stackedDeck.deckList:
                    # treat ace as 1 for simplicity
                    if card.pointValue() == [1, 11]:
                        value = 1
                    else:
                        value = card.pointValue()
                    if max(self.points) + value <= 21:
                        probabilitySpace.append(card)
                    else:
                        continue
                if len(probabilitySpace) / sampleSpace > thresholdProbability:
                    ComputerPlayer.hit(self)
                else:
                    ComputerPlayer.stand(self)
            elif self.aitype == "gambler":
                # like the thinker, but uses expected values instead
                stackedDeck = deck
                knowledge = publicInfo
                knowledge.append(self.hand[1])
                for card in knowledge:
                    stackedDeck.removeCard(card)
                probabilitySpace = []
                for card in stackedDeck.deckList:
                    # treat ace as 1 for simplicity
                    if card.pointValue() == [1, 11]:
                        value = 1
                    else:
                        value = card.pointValue()
                    probabilitySpace.append(value)
                if probabilitySpace / len(probabilitySpace) + min(self.points) <= 21:
                    ComputerPlayer.hit(self)
                else:
                    ComputerPlayer.stand(self)
            else:
                holeCard = deck.deckList[0]
                if holeCard == "ace":
                    if max(self.points) + 1 <= 21 or max(self.points) + 11 <= 21:
                        ComputerPlayer.hit(self)
                    else:
                        ComputerPlayer.stand(self)
                else:
                    if int(holeCard.value) + max(self.points) <= 21:
                        ComputerPlayer.hit(self)
                    else:
                        ComputerPlayer.stand(self)

    def action(self):
        """
        Handles the computer's actions.

        Returns:
        --------
        This function returns nothing.
        """
        if self.lost:
            print(self.name + " has busted.")
        elif self.done:
            print(self.name + " has elected to stand.")
        else:
            self.think()
            return ComputerPlayer.action(self)

    def reset(self):
        """
        Resets the computer's attributes for the next round.

        Returns:
        --------
        This function returns nothing.
        """
        self.points = []
        self.won = False
        self.lost = False
        self.done = False
        self.hand = []
        self.final = 0
        self.bust = 0

class Game:
    """
    The Game class, which handles the entire game.
    """
    def __init__(self, humanCount=1, cpuCount=1):
        """
        Constructor for the Game class.

        Parameters:
        -----------
        humanCount: int
            How many human players should there be?
        cpuCount: int
            How many computer players should there be?

        playerList: list
            List of all players, human and computer.
        playAgain: bool
            Used later to ask the player for rematching.

        Returns:
        --------
        This function returns nothing.
        """
        # note: this will work with any number of humanCount and cpuCount
        self.playerList = []
        self.playAgain = False
        self.humanCount = humanCount
        self.cpuCount = cpuCount

        # used an ASCII text generator, because who wants to figure this out by hand
        print("   ____          _               ____  _  ___  _  _  ____      ____  _            _     _            _    ")
        print("  / ___|__ _ ___(_)_ __   ___   | ___|/ |/ _ \| || ||___ \ _  | __ )| | __ _  ___| | __(_) __ _  ___| | __")
        print(" | |   / _` / __| | '_ \ / _ \  |___ \| | | | | || |_ __) (_) |  _ \| |/ _` |/ __| |/ /| |/ _` |/ __| |/ /")
        print(" | |__| (_| \__ \ | | | | (_) |  ___) | | |_| |__   _/ __/ _  | |_) | | (_| | (__|   < | | (_| | (__|   < ")
        print("  \____\__,_|___/_|_| |_|\___/  |____/|_|\___/   |_||_____(_) |____/|_|\__,_|\___|_|\_\/ |\__,_|\___|_|\_\\")
        print("                                                                                     |__/       ")

        for _ in range(self.humanCount):
            self.playerList.append(HumanPlayer())
        for _ in range(self.cpuCount):
            self.playerList.append(ComputerPlayer())

        # shuffle the list of players
        random.shuffle(self.playerList)

        print("\nHere are your participants, in turn order: ")
        for person in self.playerList:
            persontype = "Computer"
            if person.isHuman == True:
                persontype = "Human"
            print("\t" + person.name + " (" + persontype + ") \n\t\tUID: " + str(person.uuid))
        print("\t...and the dealer, who hits 16 and stands 17.")
        print("\n")

        # create the Dealer (which is just a special case of ComputerPlayer), so that it is always last
        self.playerList.append(ComputerPlayer(name="Dealer", threshold=17, aitype="standard"))

    def publicInfo(self):
        """
        Configures the publicly known deck information, used by the AI later on.

        Returns:
        --------
        This function returns nothing.
        """
        global publicInfo
        for player in self.playerList:
            if player.name != "Dealer":
                publicInfo.append(player.hand[0])
                publicInfo.append(player.hand[1])
            else:
                publicInfo.append(player.hand[0])

    def play(self):
        """
        Deals out two cards to each player, and then also handles wrapping up.

        Returns:
        --------
        This function returns nothing.
        """
        global deck
        for player in self.playerList:
            # deal each player a face-up card (there's no variable for face-up or face-down, it's just always the first card)
            player.hand.append(deck.drawCard())
            # deal each player a face-down card
            player.hand.append(deck.drawCard())
            # deck check
            deck.deckCheck()
        # get the list of face-up cards
        Game.publicInfo(self)
        # now play the turns
        for player in self.playerList:
            Game.turn(self, player)
        Game.wrapUp(self)    

    def turn(self, player):
        """
        Controls each player's turn.

        Parameters:
        -----------
        player: Player

        Returns:
        --------
        This function returns nothing.
        """
        global deck
        print("\n" + player.name + "'s turn: ")
        # do human player things
        if player.isHuman:
            # print the player's name, and the contents of their current hand
            print("\t" + player.name + ", your hand is: ")
            for card in player.hand:
                if type(card.value) == list:
                    print("\t\t" + str(card) + " (1 or 11 points)")
                else:
                    print("\t\t" + str(card) + " (" + str(card.value) + " points)")
            # print the player's hand value
            sum = 0
            alternate = 0
            # tracking aces
            doubleAce = 0
            for card in player.hand:
                if type(card.value) == list:
                    sum += card.value[0]
                    alternate += card.value[1]
                    doubleAce += 1
                else:
                    sum += card.value
                    alternate += card.value
            if sum != alternate:
                print("\tYour hand is worth " + str(sum) + " or " + str(alternate) + " points.\n")
            elif doubleAce == 2:
                # set sum and alternate, if you have double aces
                sum = 2
                alternate = 12
                print("\tYour hand is worth 2 or 12 points.")
            else:
                print("\tYour hand is worth " + str(sum) + " points.\n")
            if sum == alternate:
                player.points = [sum]
            else:
                player.points = [sum, alternate]

            # auto stands if 21
            if sum == 21 or alternate == 21:
                player.won = True
                print("\tBlackjack! No further action needed.")
            else:
                print("\tHere are the other players' cards you can see: ")
                for participant in self.playerList:
                    # it would be pretty silly to tell you your own cards
                    if participant.name != player.name:
                        if participant.name != "Dealer":
                            print("\t" + participant.name + ":")
                            for i in range(len(participant.hand)):
                                if type(participant.hand[i].value) == list and participant.hand[i].value == [1, 11]:
                                    print("\t\t" + str(participant.hand[i]) + " (1 or 11 points)")
                                else:
                                    if len(str(participant.hand[i].value)) > 2:
                                        print("\t\t" + str(participant.hand[i]) + " (" + str(participant.hand[i].value)[1:-1] + " points)")
                                    else:
                                        print("\t\t" + str(participant.hand[i]) + " (" + str(participant.hand[i].value) + " points)")
                        elif participant.name == "Dealer":
                            # dealer goes last anyway
                            print("\tDealer: ")
                            if type(participant.hand[0].value) == list:
                                print("\t\t" + str(participant.hand[0]) + " (1 or 11 points)")
                            else:
                                print("\t\t" + str(participant.hand[0]) + " (" + str(participant.hand[0].value) + " points)")
                print("\n")
            player.action()

        # just computer things
        else:
            print(player.name + "'s hand is: ")
            for card in player.hand:
                if type(card.value) == int:
                    print("\t" + str(card) + " (" + str(card.value) + " points)")
                else:
                    print("\t" + str(card) + " (1 or 11 points)")
            deck.deckCheck()
            sum = 0
            alternate = 0
            # tracking aces
            doubleAce = 0
            for card in player.hand:
                if type(card.value) == list:
                    sum += card.value[0]
                    alternate += card.value[1]
                    doubleAce += 1
                else:
                    sum += card.value
                    alternate += card.value
            if doubleAce == 2:
                # set sum and alternate, if you have double aces
                sum = 2
                alternate = 12
            player.points = [sum, alternate]
            player.action()

    def wrapUp(self):
        """
        Handles wrapping up, including printing out winners, their hands, and scores.
        
        Returns:
        --------
        This function returns nothing.
        """
        global leaderboard
        print("\n")
        scores = []
        winners = []
        scoreSheet = []
        for player in self.playerList:
            data = [player.name, str(player.uuid), player.won, player.lost, player.final, player.bust, player.hand]
            scores.append(data)
            if not player.lost and not player.won:
                scoreSheet.append(player.final)
            elif not player.lost and player.won:
                scoreSheet.append(21)
        if len(scoreSheet) != 0:
            maxWinningScore = max(scoreSheet)
        else:
            maxWinningScore = 0
        for datum in scores:
            if datum[2] == True:
                if datum[0] == "Dealer":
                    print("The dealer scored 21 points.")
                    print("\tHand: " + str(datum[6]))
                    winners.append([datum[0], datum[1]])
                else:
                    print("Player " + datum[0] + " (uuid " + datum[1] + ") scored 21 points.")
                    print("\tHand: " + str(datum[6]))
                    winners.append([datum[0], datum[1]])
            elif datum[3] == True:
                if datum[0] == "Dealer":
                    print("The dealer busted with " + str(datum[5]) + " points.")
                    print("\tHand: " + str(datum[6]))
                else:
                    print("Player " + datum[0] + " (uuid " + datum[1] + ") busted with " + str(datum[5]) + " points.")
                    print("\tHand: " + str(datum[6]))
        for datum in scores:
            if datum[2] == False and datum[3] == False:
                if datum[0] == "Dealer":
                    print("The dealer has earned " + str(datum[4]) + " points.")
                    print("\tHand: " + str(datum[6]))
                else:
                    print("Player " + datum[0] + " (uuid " + datum[1] + ") has earned " + str(datum[4]) + " points.")
                    print("\tHand: " + str(datum[6]))
                if datum[4] == maxWinningScore:
                    winners.append([datum[0], datum[1]])
        print("\n")
        # print the winners
        if len(winners) == 0:
            # in practice, if the dealer busts, everyone wins
            print("Push! No one won this round.")
        elif len(winners) == 1 and winners[0][0] == "Dealer":
            print("The dealer has won.")
        elif len(winners) == 1 and winners[0][0] != "Dealer":
            print(str(winners[0][0]) + " has won.")
            timesWon = leaderboard[winners[0][1]]
            timesWon[1] += 1
            leaderboard[winners[0][1]] = [timesWon[0], timesWon[1]]
        else:
            print("Tie! Your winners are: ")
            for winner in winners:
                if winner[0] != "Dealer":
                    print("\t" + winner[0])
                    leaderboard[winners[0][1]][1] += 1
                elif winner[0] == "Dealer":
                    print("\tAdditionally, the dealer has tied.")
        print("\nCurrent Leaderboard:")
        for i in leaderboard:
            print("\tPlayer: " + str(leaderboard[i][0]) + "\n\t\tID: " + str(i) + "\n\t\tTimes Won: " + str(leaderboard[i][1]))
        Game.again(self)

    def again(self):
        """
        Prompts the player for a rematch.

        Returns:
        --------
        This function returns nothing.
        """
        # this works even if there are no human players
        query = input("\nPlay (or simulate) again (y/n)? ")
        if query.lower() == "y":
            self.playAgain = True
            deck.shuffle()
            for player in self.playerList:
                player.reset()
            Game.play(self)
        else:
            self.playAgain = False

def main():
    # query for human and computer player count
    humanCount = input("Enter the number of human players: ")
    # input sanitation, quits if you try something funny
    try:
        humanCount = int(humanCount)
    except ValueError:
        print("Error: Please enter a valid number of human players.")
        sys.exit()
    cpuCount = input("Enter the number of computer players: ")
    try:
        cpuCount = int(cpuCount)
    except ValueError:
        print("Error: Please enter a valid number of computer players.")
        sys.exit()
    if humanCount == 0 and cpuCount == 0:
        print("Error: You must have at least one human or computer player.")
        sys.exit()
    # you can execute this program with blackjack = Game(a, b) where a and b are integers
    # and then blackjack.play()
    blackjack = Game(humanCount, cpuCount)
    blackjack.play()

if __name__ == "__main__":
    main()
