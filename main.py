from random import shuffle
from random import seed
import random
from collections import defaultdict
import sys

seed(3)

# Create a deck of 40 cards that is shuffled
def create_deck():
    deck =  list(range(40))
    shuffle(deck)
    return deck

# Attribute the cards to the players randomly
def attribute_cards(deck):
    H = [[0 for _ in range(40)] for _ in range(4)]

    for i,c in enumerate(deck):
        H[i%4][c] = 1

    return H

# One hot encoding of the cards
#  A one hot encoding is a representation of categorical variables as binary vectors
#   where each value is mapped to a single value in the binary vector.
one_hot = [
  "AH", "KH", "QH", "JH", "10H", "9H", "8H", "7H", "6H", "5H",
  "AD", "KD", "QD", "JD", "10D", "9D", "8D", "7D", "6D", "5D",
  "AC", "KC", "QC", "JC", "10C", "9C", "8C", "7C", "6C", "5C",
  "AS", "KS", "QS", "JS", "10S", "9S", "8S", "7S", "6S", "5S"
]

# Define the suits
hearts =   list(map(lambda x: 1 if x[-1] == "H" else 0, one_hot))
diamonds = list(map(lambda x: 1 if x[-1] == "D" else 0, one_hot))
clubs =    list(map(lambda x: 1 if x[-1] == "C" else 0, one_hot))
spades =   list(map(lambda x: 1 if x[-1] == "S" else 0, one_hot))
all_hand = list(map(lambda _: 1, one_hot))

# Helper function to create a hand from a list of cards
#  it will use the one hot encoding to create the hand
def make_hand(*args):
    hand = [0 for _ in range(40)]
    for a in args:
        hand[one_hot.index(a)] = 1
    return hand

# Dot product of two vectors
# If the vectors are a one hot encoding of a cards, the dot product will give you 
# the intersection of the two sets
def dot(a,b):
    return [x*y for x,y in zip(a,b)]

# Scale a vector by a scalar
def scale(s, a):
    return [x*s for x in a]

# Add two vectors
# If the vectors are a one hot encoding of a cards, the add function will give you
# the union of the two sets
def add(a, b):
    return [x+y for x,y in zip(a,b)]

# add multiple vectors together
def madd(*args):
    if len(args) == 1:
        return args[0]
    else:
        return add(args[0], madd(*args[1:]))

# Precalculate points for each turn
points = add(scale(5, make_hand("5H", "5D", "5C", "5S")), 
             scale(10, make_hand("10H", "10D", "10C", "10S", "AH", "AD", "AC", "AS")))

# Calculate the score of a board
def score(board):
    # Here, points is a vector that contains the point for each card. 
    # It contains 0 most of the place and 5 for the 5 and 10 for the 10 and the aces
    # Dot product + sum = number of points
    return sum(dot(points, board))

# Inverse a hand (1 -> 0, 0 -> 1)
def inv(a):
    return [1 if x == 0 else 0 for x in a]


# Get the suite of the card (as a hand)
def suite(card):
    number = card.index(1)
    if number < 10:
        return hearts 
    elif number < 20:
        return diamonds
    elif number < 30:
        return clubs
    else:
        return spades

# Get n random cards
def random_cards(n):
    c = one_hot[:]
    shuffle(c)
    return make_hand(*c[:n])

# Print the cards in a human readable format
def print_cards(deck):
    print("{", end="")
    for i, d in enumerate(deck):
        if d:
            print(one_hot[i], end=",")
    print("}")

# Get the playable cards in a hand
def playable_cards(hand, asked):
    if not asked:
        return hand

    colored_hand = dot(hand, asked)
    if any(colored_hand):
        return colored_hand 
    else:
        return hand

# Convert a hand to a list of strings (cards)
def hand_to_list(hand):
    val = []
    for i, h in enumerate(hand):
        if h:
            val.append(one_hot[i])
    return val


# Remove a card from a hand
def remove_card(hand, card):
    return dot(hand, inv(card))

# Print the board
def print_board(board):
    for i, b in enumerate(board):
        print("Player", i+1, ":")
        print_cards(b)

def mask_atout(card1, asked, atout):
    # It works by masking the cards with the asked suit and the "atout"
    mask = asked
    if atout != asked:
        mask = add(mask, atout)

    return dot(card1, mask)

def get_highest_any_suite(hand):
    lowest_v = 40
    highest_hand = make_hand()

    for suite in [hearts, diamonds, clubs, spades]:
        hand_masked = dot(hand, suite)
        if any(hand_masked):
            v = first(hand_masked) - first(suite)
            if lowest_v > v:
                lowest_v = v
                highest_hand = make_hand(one_hot[first(hand_masked)])

    return highest_hand

# Compare two cards
def higher(card1, card2, asked, atout):
    return mask_atout(card1, asked, atout) > mask_atout(card2, asked, atout)
    
# Print the score of a round
def print_score(scores):
    print(f"{scores[0] + scores[2]} vs {scores[1] + scores[3]} :", end=" ")
    for i, s in enumerate(scores):
        print(f"P{i+1}={s}", end=" ")
    print()

# Print the played cards of a round
def print_round(round, winner, played):
    print(f"Round {round} - ", end="")
    for i, p in enumerate(played):
        to_show = f"P{i+1}={p}"
        if i == winner:
            print(f"*{to_show}*", end=" ")
        else:
            print(to_show, end=" ")
    print()

class random_strategy:
    def __init__(self):
        pass

    def play_card(self, hand, playable_hand, asked, atout):
        choice = random.choice(hand_to_list(playable_hand))
        return make_hand(choice)

    def update_played(self, played):
        pass

def first(hand):
    for i, v in enumerate(hand):
        if v == 1:
            return i
    return -1

class highest_strategy:
    def __init__(self):
        pass

    def play_card(self, hand, playable_hand, asked, atout):
        if not atout: # first to play (in the game)
            return get_highest_any_suite(playable_hand)

        if not asked: # first to play
            atout_masked = dot(atout, playable_hand)
            if any(atout_masked):
                return make_hand(one_hot[first(atout_masked)])
            else:
                return get_highest_any_suite(playable_hand)

        masked = mask_atout(playable_hand, asked, atout)
        index = first(masked)
        if index != -1:
            return make_hand(one_hot[index])
        else:
            return random_strategy().play_card(hand, playable_hand, asked, atout)

    def update_played(self, played):
        pass


        # choice = sorted(hand_to_list(playable_hand), key=lambda x: mask_atout(make_hand(x), asked, atout))[0]
        # return make_hand(choice)

from itertools import combinations

def distribute(left):
    cards = hand_to_list(left)
    return combinations(cards, len(cards)//3)
    
def win_round(cards, asked, atout):
    cards = [make_hand(x) for x in cards] 
    best = 0
    for i, c in enumerate(cards[1:]):
        if higher(c, cards[best], asked, atout):
            best = i

    return best

def as_number(hand):
    return sum([x*2**i for i, x in enumerate(hand)])

x = defaultdict(lambda: defaultdict(lambda: False))

def node(hand, left,  turn_count, atout):
    global x
    memoi = x[as_number(hand)][as_number(left)]
    if memoi:
        return memoi

    lhand = hand_to_list(hand)
    lleft = hand_to_list(left)

    if lhand == [] or score(left) == 0:
        return (0, [], [])

    hand_values = []
    for u in lhand:
        combination_values = []
        for d in combinations(lleft, 3): # distribution node
            value_of_hand = 0
            move = 0
            dd = 0
            for p2 in range(len(d)):
                p1 = (p2+1) % 3
                p3 = (p2+2) % 3
                card_played = [u, d[p1], d[p2], d[p3]]

                temp = score(make_hand(*card_played))
                win = win_round(card_played, suite(make_hand(u)), atout)
                current_hand_value = temp if win%2 == 0 else -temp

                next_hand = remove_card(hand, make_hand(u))
                next_left = remove_card(left, make_hand(*d))
                node_value, move, dd = node(next_hand, next_left, win, atout)
                value_of_hand += current_hand_value + node_value
            
            combination_values.append((value_of_hand / 3, move, [d] + dd))

        min_value = min(combination_values, key=lambda x : x[0])
        hand_values.append((min_value[0], [u] + move, min_value[2]))

    val = max(hand_values, key=lambda x: x[0])
    x[as_number(hand)][as_number(left)] = val
    return val

from time import sleep
#while True:
#u = ["10C", "9H", "JH", "AD"]
#unknown = ["JC", "10H", "8H", "7H", "5C", "AS", "AH", "8D", "5D","QS", "QD", "QH"]
u = ["10C", "9H", "AH"]
unknown = ["JC", "10H", "8H", "7H", "5C", "AS", "QH", "8D", "5D"]
print(node(make_hand(*u), make_hand(*unknown), 0, hearts))

exit(0)


            

            

        

            

            
            

        


class dp_strategy:
    left = []
    tree = []

    def __init__(self):
        self.left = make_hand()

    def play_card(self, hand, playable_hand, asked, atout):
        


        pass

    def update_played(self, played):
        self.left = remove_card(self.left, played)



    

# Play a game
def game(verbose=True):

    # Create a deck and attribute the cards to the players
    deck = create_deck()
    board = attribute_cards(deck)

    scores = [0, 0, 0, 0] # Vector containing the score of each player
    #strategies = [highest_strategy(), random_strategy(), highest_strategy(), random_strategy()]
    strategies = [random_strategy(), highest_strategy(), random_strategy(), highest_strategy()]
    winner = 0 # The winner of the round
    
    if verbose: print_board(board)
    atout = False

    for i in range(10):
        asked = False # The asked suit
        played = make_hand() # Played cards
        # Name of the card played by each player. Only used for display purpose
        played_display = ["", "", "", ""] 
        # The currently highest card and winner of the trick
        highest_card = make_hand()
        new_winner = winner

        for j in range(4):
            # Current player to start
            current = (j + winner) % 4

            # Hand of the current player
            hand = board[current]
            # Play a card, remove it from the hand of the player and get the played cards
            playable_hand = playable_cards(hand, asked)
            card = strategies[current].play_card(hand, playable_hand, asked, atout)

            if not any(dot(card, playable_hand)) or card.count(1) != 1 or len(card) != 40:
                print("Player", current+1, "cheated")
                raise Exception("Player cheated", card)
                
            board[current] = remove_card(hand, card)


            if verbose: print("Player", current+1, ":", hand_to_list(card)[0])

            # Modify the currently asked suite
            if not asked:
                asked = suite(card)

            if not atout:
                atout = asked

            # Update the played cards
            played = add(played, card)
            if verbose: played_display[current] = hand_to_list(card)[0]

            # Update the played cards and the highest card
            if higher(card, highest_card, asked, atout):
                highest_card = card
                new_winner = current
            
        # Update the winner and the score
        winner = new_winner
        #current_score = score(played)
        scores[winner] += score(played)
        for i in range(4):
            strategies[i].update_played(played)
        if verbose: print_round(i+1, winner, played_display)
    #print_score(scores)
    return scores

#v = True
v = True

if v:
    score = game()
    print_score(score)
else:
# Compute the score of 100000 games            
#for _ in range(10):
    total_score = [0, 0, 0, 0]
    atteinged = 10
    for i in range(100000):
        if i == atteinged:
            print(f"Computing game {i}")
            sys.stdout.flush()
            atteinged *= 10
        total_score = add(game(verbose=False), total_score)
    print_score(total_score)


