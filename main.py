from random import shuffle
import random

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

# Play a card from a hand
def play_card(hand, asked=False):
    playable_hand = playable_cards(hand, asked)
    choice = random.choice(hand_to_list(playable_hand))
    new_hand = remove_card(hand, choice)

    return new_hand, make_hand(choice)

# Remove a card from a hand
def remove_card(hand, card):
    return dot(hand, inv(make_hand(card)))

# Print the board
def print_board(board):
    for i, b in enumerate(board):
        print("Player", i+1, ":")
        print_cards(b)

# Compare two cards
def higher(card1, card2, asked):
    # It works by masking the cards with the asked suit and the "atout"
    mask = asked
    if hearts != asked:
        mask = add(mask, hearts)

    # Compare the two vectors. In python, list comparaison will compare element by element
    # until one value is greater than the other.
    return dot(card1, mask) > dot(card2, mask)
    
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
    

# Play a game
def game():

    # Create a deck and attribute the cards to the players
    deck = create_deck()
    board = attribute_cards(deck)

    scores = [0, 0, 0, 0] # Vector containing the score of each player
    winner = 0 # The winner of the round
    
    print_board(board)

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
            board[current], card = play_card(hand, asked)
            print("Player", current+1, ":", hand_to_list(card)[0])

            # Modify the currently asked suite
            if not asked:
                asked = suite(card)

            # Update the played cards
            played = add(played, card)
            played_display[current] = hand_to_list(card)[0]

            # Update the played cards and the highest card
            if higher(card, highest_card, asked):
                highest_card = card
                new_winner = current
            
        # Update the winner and the score
        winner = new_winner
        current_score = score(played)
        scores[winner] += score(played)
        print_round(i+1, winner, played_display)
    #print_score(scores)
    return scores



game()

# Compute the score of 100000 games            
#total_score = [0, 0, 0, 0]
#for _ in range(100000):
#    total_score = add(game(), total_score)
#print_score(total_score)
