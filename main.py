import random
import itertools
import math

#Dictionary of Rank Name:Rank Points (for 15 scoring)
cards = {
    "Ace": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "Jack": 10,
    "Queen": 10,
    "King": 10
}

#Card order for run scoring
card_order = {
    "Ace": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "Jack": 11,
    "Queen": 12,
    "King": 13
}
suits = ("Spades", "Clubs", "Hearts", "Diamonds")


def is_run(combo):  #Used for checking if something is a run
    is_run = True  #Assume true
    combo = sorted(combo)  #sort in order
    for i in range(len(combo) - 1):
        if card_order[combo[i + 1].rank] - card_order[
                combo[i].
                rank] != 1:  #Create a moving window of size two through the list
            is_run = False  #If the moving window is not consecutive at any point, it's not a valid run
    return is_run


class Card:  #Card class
    def __init__(self, rank, suit, isStarter=False):
        #Make arguments attributes
        self.suit = suit
        self.rank = rank
        self.isStarter = isStarter

    def __str__(self):

        #The str value is different if the Card is a starter
        if not self.isStarter:
            return self.rank + " of " + self.suit
        else:
            return "STARTER: " + self.rank + " of " + self.suit

    def __eq__(self, other):  #For ordering
        return self.suit == other.suit and self.rank == other.rank

    def __lt__(self, other):  #For ordering as well
        return card_order[self.rank] < card_order[other.rank]
    def make_starter(self):
      self.isStarter = True

class Deck:  #For a future game
    def __init__(self):
        self.cards = [
            Card(rank, suit) for rank in cards.keys() for suit in suits
        ]
        self.shuffle()
    def __getitem__(self, index):
        return self.cards[index]

    def __setitem__(self, index, value):
        self.cards.index = value

    def shuffle(self):
        random.shuffle(self.cards)


class Hand:
    def __init__(self, deck, length):
        #Make hand from deck
        #NOTE: Deck exists for possible future game program
        self.deck = deck
        self.deck.shuffle()
        self.hand = self.deck[0:length]
        #deck = deck[length:]

        #Points = 0, find all combos, set starter card
        self.points = 0
        self.combinations()
        #self.hand[0].isStarter = True
        self.cards = [
            Card(rank, suit) for rank in cards.keys() for suit in suits
        ]
    def set_hand(self,value):
      self.hand = value

    def add(self,value):
      self.hand.append(value)

    def score(self, text=True):
        self.points = 0
        self.combinations()
        self.text = text
        #Run all scoring programs
        self.pair_score()
        self.fifteen_score()
        self.flush_score()
        self.run_score()
        self.nobs_score()
        return self.points
    
    def best_hand_average(self):
      self.make_possible_hands()
      hands_scores = {}
      for card in self.cards:
        if card in self.hand:
          self.cards.remove(card)

      for hand in self.possible_hands:
        currentHandScore = 0
        possibleHand = Hand(self.deck,1)
        for card in self.cards:
          card.make_starter()
          holder = []
          for thing in hand:
            holder.append(thing)
          holder.insert(0,card)
          possibleHand.set_hand([])
          for card in holder:
            possibleHand.hand.append(card)
          currentHandScore += possibleHand.score(False)

        hands_scores[currentHandScore] = hand

      best_hand = hands_scores[max(hands_scores.keys())]
      return best_hand
    
    def make_possible_hands(self):
      self.possible_hands = []
      # Create all non-repeating combinations with itertools
      for combo in itertools.combinations(self.hand, 4):
          combo = list(combo)
          self.possible_hands.append(combo)

    def __getitem__(self, index):
        #Special method for when iterating through list of Cards
        return self.hand[index]

    def __setitem__(self, index,value):
      self.hand[index] = value

    def combinations(self):
        self.combos = []
        # Create all non-repeating combinations with itertools
        for r in range(2, len(self.hand) + 1):
            for combo in itertools.combinations(self.hand, r):
                combo = list(combo)
                self.combos.append(combo)

    def pair_score(self):
        myranks = [card.rank for card in self.hand]  #Get list of all ranks
        for rank in cards.keys():  #Go through each rank
            if myranks.count(
                    rank) == 2:  #If there are two of that rank then pair for 2
                if self.text:
                  print("Pair " + rank + "s for 2")
                self.points += 2
            elif myranks.count(rank) == 3:  #If three, trips for 6
                if self.text:
                  print("Triple " + rank + "s for 6")
                self.points += 6
            elif myranks.count(rank) == 4:  #If four, quads for 12
                if self.text:
                  print("Quad " + rank + "s for 12")
                self.points += 12

    def fifteen_score(self):
        for combo in self.combos:  #Go through combos
            myranks = [cards[card.rank] for card in combo
                       ]  #Find all ranks of cards in the combo
            if sum(myranks) == 15:  #Check the current combo for a sum of 15
                if self.text:
                  print("Fifteen for 2 -> " + self.print_combos(combo))
                self.points += 2

    def flush_score(self):
        mysuits = [card.suit
                   for card in self.hand[1:]]  #Get all suits in the hand
        for suit in suits:  #Go through each suit
            if mysuits.count(suit) == 4 and self.hand[
                    0].suit != suit:  #If the four non-starter cards are a flush, 4 points
                if self.text:
                  print("Flush " + suit + " for 4")
                self.points += 4
            elif mysuits.count(suit) == 5 and self.hand[
                    0].suit == suit:  #If all five are a flush, 5 points
                if self.text:
                  print("Flush " + suit + " for 5")
                self.points += 5

    def run_score(self):
        #This was the hard one

        allValidCombos = []  #Where valid runs will go
        for combo in self.combos:
            newCombo = sorted(combo)  #Sort the combo
            if len(newCombo) > 2 and is_run(
                    newCombo):  #Must be a valid run and at least 3 long
                finalCombo = [
                ]  #Create a list to put the cards in (tuples to lists are a pain)
                for card in newCombo:
                    finalCombo.append(str(card))
                allValidCombos.append(
                    finalCombo)  #Add the final combo to the valid combo list

        #Dealing with how long runs contain shorter ones
        for i in range(
                5
        ):  #This is just brute forcing by doing it 5 times. I couldn't figure it out any other way
            for combo in allValidCombos:
                for smallcombo in allValidCombos:  #Find every pair of combos
                    if len(smallcombo) < len(combo) and all(
                            item in combo for item in smallcombo
                    ):  #If one contains the other, remove the smaller one
                        allValidCombos.remove(smallcombo)

        #Scoring
        for combo in allValidCombos:
            if self.text:
              print("Run for " + str(len(combo)) + " -> " +
                  self.print_combos(combo))
            self.points += len(combo)

    def nobs_score(self):
        #Very simple nobs scoring
        for card in self.hand[1:]:  #Check each card
            if card.rank == "Jack" and card.suit == self.hand[
                    0].suit:  #If the card is a jack and matches the suit of the starter card...
                if self.text:
                  print("Nobs for 1")  #Nobs!
                self.points += 1

    def print_combos(self, combo):
        #Nice formatting for printing combos
        combolist = []
        for card in combo:
            combolist.append(str(card))
        return (' + '.join(combolist))

human = 0
computer = 0
while human < 121 and computer < 121:
  deck = Deck()
  hand = Hand(deck, 6)

  #DEBUGGING Create hand - set to best possible hand
  '''eli.hand = [Card("5","Spades",True),Card("Jack","Spades"),Card("5","Diamonds"),Card("5","Hearts"),Card("5","Clubs")]'''

  #Show hand
  print("------------------------------------")
  cardcounter = 0
  for card in hand:
    cardcounter += 1
    print(str(cardcounter) + ". " + str(card))
  print("------------------------------------")
  best_hand = hand.best_hand_average()
  #for card in best_hand:
    #print(card)
  firsti = int(input("First card to throw: "))
  secondi = int(input("Second card to throw: "))
  first = hand[firsti-1]
  second = hand[secondi-1]
  hand.hand.remove(first)
  hand.hand.remove(second)
  best = Hand(deck,4)
  best.hand = best_hand
  
  random.shuffle(hand.cards)
  starter = hand.cards[0]
  starter.isStarter = True

  best.hand.insert(0,starter)
  hand.hand.insert(0,starter)

  hand.combinations()
  best.combinations()
  print("------------------------------------")
  print("----------------YOU-----------------")
  for card in hand:
    print(card)
  print("-")
  print("Total: " + str(hand.score()))
  human += hand.points
  print("------------------------------------")
  print("-------------COMPUTER---------------")
  for card in best:
    print(card)
  print("-")
  print("Total: " + str(best.score()))
  computer += best.points
  print("------------------------------------")
  print("Human: " + str(human))
  print("Computer: " + str(computer))
  print("------------------------------------")
if computer>human:
  print("My processors far exceed your puny mortal brain. I am, and always will be, the champion!")
elif human>computer:
  print("Human wins!")
else:
  print("It is a tie! Let's play again and we will see who truly is the champion.")