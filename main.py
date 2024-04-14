from random import shuffle
from random import seed
import random
from collections import defaultdict
import sys

#seed(3)

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


def add_cap(a, b):
    return [min(x+y, 1) for x,y in zip(a,b)]

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

    def play_card(self, hand, playable_hand, asked, atout, a, b, c):
        choice = random.choice(hand_to_list(playable_hand))
        return make_hand(choice)

    def update_played(self, played, asked, a):
        pass

def first(hand):
    for i, v in enumerate(hand):
        if v == 1:
            return i
    return -1

class highest_strategy:
    def __init__(self):
        pass

    def play_card(self, hand, playable_hand, asked, atout, a, b, c):
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
            return random_strategy().play_card(hand, playable_hand, asked, atout, a, b, c)

    def update_played(self, played, asked, a):
        pass


        # choice = sorted(hand_to_list(playable_hand), key=lambda x: mask_atout(make_hand(x), asked, atout))[0]
        # return make_hand(choice)

class dp_strategy:

    left = [] 
    turn_kick_in = 0
    current_turn = 0

    def __init__(self, turn_kick_in, heuristic, aggregator):
        self.left = []
        self.turn_kick_in = turn_kick_in
        self.current_turn = 10
        self.heuristic = heuristic
        self.aggregator = aggregator
        

    def play_card(self, hand, playable_hand, asked, atout, winner, played_display, current):

        if not asked:
            asked = all_hand
        
        if not atout:
            atout = all_hand

        if self.current_turn == 10:
            self.left = [hand, remove_card(all_hand, hand), remove_card(all_hand, hand), remove_card(all_hand, hand)]

        card_to_play = make_hand()
        if self.current_turn > self.turn_kick_in:
            card_to_play = random_strategy().play_card(hand, playable_hand, asked, atout, winner, played_display, current)
        else:
            iter_deck = [
                playable_hand,
                all_hand if played_display[(current+1)%4] == "" else make_hand(played_display[(current+1)%4]),
                all_hand if played_display[(current+2)%4] == "" else make_hand(played_display[(current+2)%4]),
                all_hand if played_display[(current+3)%4] == "" else make_hand(played_display[(current+3)%4]),
            ]
            if len(hand_to_list(playable_hand)) == 1:
                card_to_play = make_hand(hand_to_list(playable_hand)[0])
            else:
                depth = 1 if self.current_turn > 3 else 3
            
                #print("foobar", depth, self.current_turn)
                score, action, _ = node2(self.left, (current-winner) % 4, atout, depth, self.current_turn, force=iter_deck, heuristic=self.heuristic, aggregate=self.aggregator)
                card_to_play = make_hand(action)

        self.current_turn -= 1
        return card_to_play
        

    def update_played(self, table, asked, current):
        deck = self.left
        next_deck = [0] * 4
        hand_table = make_hand(*table)
        for i in range(4):
            current_i = (current + i) % 4
            fournis = any(dot(asked, make_hand(table[current_i]))) # S'il a fournit la couleur demandé
            #fournis = True
            if not fournis:
                next_deck[i] = remove_card(deck[i], add_cap(hand_table, asked))
            else:
                next_deck[i] = remove_card(deck[i], hand_table)
        #next_deck[0] = remove_card(self.left[0], make_hand(table[current]))
        self.left = next_deck
        

from itertools import combinations

def distribute(left):
    cards = hand_to_list(left)
    return combinations(cards, len(cards)//3)
    
def win_round(cards, asked, atout):
    cards = [make_hand(x) for x in cards] 
    best = 0
    for i, c in enumerate(cards):
        if higher(c, cards[best], asked, atout):
            best = i

    return best

def as_number(hand):
    return sum([x*2**i for i, x in enumerate(hand)])

memoi_dict = defaultdict( 
        lambda: defaultdict(
            lambda: defaultdict( 
                lambda : defaultdict(
                    lambda : defaultdict(int)
                    ))))

memoi_dict2 = defaultdict(lambda : False)

valll = 0

def get_memoi(deck, start_player):
    global memoi_dict2
    key = (*list(map(as_number, deck)), start_player)

    return memoi_dict2[key]#memoi_dict[as_number(deck[0])][as_number(deck[1])][as_number(deck[2])][as_number(deck[3])][start_player]

def set_memoi(deck, start_player, value):
    global memoi_dict2
    key = (*list(map(as_number, deck)), start_player)
    memoi_dict2[key] = value
    #memoi_dict[as_number(deck[0])][as_number(deck[1])][as_number(deck[2])][as_number(deck[3])][start_player] = value


memoi_hit = 0
def iter_without(card, deck, n):
    return hand_to_list(remove_card(deck[n], card))

# Pruning par pignonier
def pignonier_valid(next_deck, card_per_player):
    # par pignonier, si une couleur est demandé et qu'il ne fournit pas, alors 
    #  il doit avoir plus de cartes d'une autre couleur que de tour restant dans la partie

    combined = make_hand()
    for i in range(4):
        combined = add_cap(combined, next_deck[i])
        if next_deck[i].count(1) < card_per_player-1: 
            return False

    for i in range(3):
        comb = add_cap(next_deck[1 + i%3], next_deck[1 + (i+1)%3])
        if comb.count(1) < 2 * (card_per_player - 1):
            return False

    if combined.count(1) < 4 * (card_per_player - 1):
        return False

    return True

import math
def prob(n, table, deck, player, asked):
    c = make_hand(table[player])
    b = deck[player].count(1)
    if any(dot(c, asked)):
        return math.comb(b-1, n-1) / (math.comb(b, n) * n)
    else:
        k = dot(deck[player], asked).count(1)
        return math.comb(b-k, n) / (math.comb(b, n) * n)

compteur = 0

def utility(v):
    if v < 0:
        return v * 2
    else:
        return v

# number of cards in hand
def hand_heuristic(deck, start_player, atout):
    return score(deck[0])

def gen_future_heuristic(ratio):
    def future_heuristic(deck, start_player, atout):
        return score(add_cap(add_cap(add_cap(deck[0], deck[1]), deck[2]), deck[3])) * ratio
    
    return future_heuristic

def best_card_win_heuristique(H, start_player, atout):

    suit_points = [ 0 for _ in range(4) ]
    for i in range(4):
        if any( hand[0+10*i] for hand in H ) : suit_points[i] += 5
        if any( hand[5+10*i] for hand in H ) : suit_points[i] += 10
        if any( hand[9+10*i] for hand in H ) : suit_points[i] += 10

    us_point = 0
    them_point = 0
    i = 0
    while i < 40: 
        cards = (H[0][i], H[1][i], H[2][i], H[3][i])
        suit = i//10


        presence_of_best = any(cards)

        #we have the strongest card of the suit
        if cards[0] : 
            us_point += suit_points[suit]

        #somebody else has it
        elif presence_of_best:
            n = sum(cards) #nubmer of player "sharing" the card

            # teamate has it
            if cards[2]:
                us_point   =+ 1/n * suit_points[suit]
                them_point =+ (1-(1/n)) * suit_points[suit]

            # ennemy has it
            else:
                them_point =+ suit_points[suit]

        
        #if we saw a best card, go to next suit
        if presence_of_best: 
            i+=10
        else:
            i+=1
    return us_point - them_point



import statistics
def node2(
    deck, 
    start_player, 
    atout, 
    count_to_heuristic, 
    card_per_player, 
    force=[all_hand] * 4, 
    heuristic=gen_future_heuristic(0.4),
    aggregate=statistics.mean
    ):
    if count_to_heuristic == 0:
        return (heuristic(deck, start_player, atout), [], [])

    global memoi_hit, compteur
    compteur +=1 
    v = get_memoi(deck, start_player)
    if v: 
        memoi_hit+=1
        #if memoi_hit % 1000 == 0:
        #    print("Memoi hit", memoi_hit)
        #print(len(ddeck[0]), start_player)
        return v

    iter_deck = [dot(deck[i], force[i]) for i in range(4)]


    ddeck = list(map(hand_to_list, iter_deck))
    #card_per_player = len(ddeck[0])
    #if card_per_player == 0:
    #    return (0, [], [])

    c = 0
    U = []
    for u in ddeck[0]:
        possibilities = []
        #probas = []
        #value = 0
        #meta_prob = 0
        #total_mean = 0
        #total_elem = 0
        #print("start")

        for p2 in iter_without(make_hand(u), iter_deck, 1):
            for p3 in iter_without(make_hand(u, p2), iter_deck, 2):
                for p4 in iter_without(make_hand(u, p2, p3), iter_deck, 3):
                    table = [u, p2, p3, p4]
                    #print(table)
                    hand_table = make_hand(*table)

                    asked = suite(make_hand(table[start_player]))
                    next_deck = [0] * 4
                    for i in range(1, 4):
                        fournis = any(dot(asked, make_hand(table[i]))) # S'il a fournit la couleur demandé
                        fournis = True
                        if not fournis:
                            next_deck[i] = remove_card(deck[i], add_cap(hand_table, asked))
                        else:
                            next_deck[i] = remove_card(deck[i], hand_table)
                    next_deck[0] = remove_card(deck[0], hand_table)

                    #proba = 1
                    #for p in range(1, 4):
                    #    proba *= prob(card_per_player, table, deck, p, asked)

                    #print(table, proba)

                    #meta_prob += proba
                    if not pignonier_valid(next_deck, card_per_player - 1):
                        continue
                    
                    
                    winner = win_round(table, asked, atout)
                    #winner = (start_player + relative_winner) % 4
                    
                    s = score(hand_table)
                    current_score = s if winner%2 == 0 else -s
                    
                    #total_elem += 1
                    if card_per_player-1 == 1:
                        #value += current_score * proba
                        possibilities.append(current_score)
                        #total_mean += utility(current_score)
                    else:
                        (future_score, action, future_table) = node2(next_deck, winner, atout, count_to_heuristic - 1, card_per_player-1, heuristic=heuristic, aggregate=aggregate)
                        #value += (current_score + future_score) * proba
                        possibilities.append(current_score + future_score)
                        #total_mean += utility(current_score + future_score)

                    c += 1
        #print(meta_prob)
        #print("meta", meta_prob)
        #exit(1)
        #if meta_prob != 0 or meta_prob != 1:
        #    pass
        #U.append((value, u, []))
        if possibilities != []:
            U.append((aggregate(possibilities), u, []))
        else:
            pass
        #if possibilities != []:
        #    U.append(min(possibilities, key=lambda x: x[0]))

    # This can happend if we enter an invalid state
    if U == []:
        print("invalid")
        print(force)
        print(deck)
        print(iter_deck)
        return (0, ["INVALID"], [])

    action_to_take = max(U, key=lambda x: x[0])

    set_memoi(deck, start_player, action_to_take)
    return action_to_take



#d = create_deck()
#board = attribute_cards(d)
# u = ["AS", "AC", "AH", "AD"]
# unknown = ["JC", "10C", "8H", "7D", "5C", "JH", "8C", "5D", "QC", "QD", "QH", "QS"]
# #u = board[0]
# #unknown = add_cap(add_cap(board[1], board[2]), board[3])
# 
# p1 = make_hand(*u)
# p2 = make_hand(*unknown)
# p3 = make_hand(*unknown)
# p4 = make_hand(*unknown)
# 
# print(node2([p1, p2, p3, p4], 0, hearts, 2))
# print(compteur)
#p1 = make_hand("10C", "9H")
##unknown = ["JC", "10H", "8H", "7H", "5C", "AS", "QH", "8D", "5D"]
#p2 = make_hand("JC", "10H", "8H", "7H", "5C", "AS")
#p3 = make_hand("JC", "10H", "8H", "7H", "5C", "AS")
#p4 = make_hand("JC", "10H", "8H", "7H", "5C", "AS")

#p1 = make_hand("AH", "10H")
#p2 = make_hand("QH", "JH", "9H", "8H", "7H", "6H")
#p3 = make_hand("QH", "JH", "9H", "8H", "7H", "6H")
#p4 = make_hand("QH", "JH", "9H", "8H", "7H", "6H")



        

    
    
    



        # def node(hand, left,  turn_count, atout):
        #     global x, valll
        #     memoi = x[as_number(hand)][as_number(left)]
        #     if memoi:
        #         return memoi
        # 
        #     valll += 1
        # 
        #     lhand = hand_to_list(hand)
        #     lleft = hand_to_list(left)
        # 
        #     if lhand == [] or score(left) == 0:
        #         return (0, [], [])
        # 
        #     hand_values = []
        #     for u in lhand:
        #         combination_values = []
        #         for d in combinations(lleft, 3): # distribution node
        #             value_of_hand = 0
        #             move = 0
        #             dd = 0
        #             for p2 in range(len(d)):
        #                 p1 = (p2+1) % 3
        #                 p3 = (p2+2) % 3
        #                 card_played = [u, d[p1], d[p2], d[p3]]
        # 
        #                 temp = score(make_hand(*card_played))
        #                 win = win_round(card_played, suite(make_hand(u)), atout)
        #                 current_hand_value = temp if win%2 == 0 else -temp
        # 
        #                 next_hand = remove_card(hand, make_hand(u))
        #                 next_left = remove_card(left, make_hand(*d))
        #                 node_value, move, dd = node(next_hand, next_left, win, atout)
        #                 value_of_hand += current_hand_value + node_value
        #             
        #             combination_values.append((value_of_hand / 3, move, [d] + dd))
        # 
        #         min_value = min(combination_values, key=lambda x : x[0])
        #         hand_values.append((min_value[0], [u] + move, min_value[2]))
        # 
        #     val = max(hand_values, key=lambda x: x[0])
        #     x[as_number(hand)][as_number(left)] = val
        #     return val

#from time import sleep
#while True:
#u = ["10C", "9H", "JH", "AD"]
#unknown = ["JC", "10H", "8H", "7H", "5C", "AS", "AH", "8D", "5D","QS", "QD", "QH"]
#u = ["10C", "9H", "AH"]
#unknown = ["JC", "10H", "8H", "7H", "5C", "AS", "QH", "8D", "5D"]
#print(node(make_hand(*u), make_hand(*unknown), 0, hearts))
#print(valll)

#exit(0)


            

            

        

            

            
            

        


# class dp_strategy:
#     left = []
#     tree = []
# 
#     def __init__(self):
#         self.left = make_hand()
# 
#     def play_card(self, hand, playable_hand, asked, atout):
#         
# 
# 
#         pass
# 
#     def update_played(self, played):
#         self.left = remove_card(self.left, played)



    

# Play a game
def game(verbose=True, strategies = [random_strategy(),  random_strategy(), random_strategy(), random_strategy()]):

    # Create a deck and attribute the cards to the players
    deck = create_deck()
    board = attribute_cards(deck)

    scores = [0, 0, 0, 0] # Vector containing the score of each player
    #strategies = [random_strategy(), highest_strategy()]
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
            card = strategies[current].play_card(hand, playable_hand, asked, atout, winner, played_display, current)

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
            played_display[current] = hand_to_list(card)[0]

            # Update the played cards and the highest card
            if higher(card, highest_card, asked, atout):
                highest_card = card
                new_winner = current
            
        # Update the winner and the score
        winner = new_winner
        #current_score = score(played)
        scores[winner] += score(played)
        for j in range(4):
            strategies[j].update_played(played_display, asked, j)
        if verbose: print_round(i+1, winner, played_display)
    #print_score(scores)
    return scores

def min_utility(values):
    return min(map(utility, values))

def gen_cutoff_agregator(cutoff):

    def cutoff_aggregator(lst):
        sorted_lst = sorted(lst)
        index = int(len(lst) * cutoff)
        return sorted_lst[index]

    return cutoff_aggregator



#v = True
v = False
import sys

if v:
    score = game(verbose=True, 
               strategies=[
                   dp_strategy(5, rollout_heuristique, statistics.mean),
                   random_strategy(), 
                   dp_strategy(5, rollout_heuristique, statistics.mean), 
                   random_strategy()
               ])
    print_score(score)
else:
    #total_score = [0, 0, 0, 0]
    #atteinged = 10
    for heuristic in [
        ("future (0.4)", gen_future_heuristic(0.4)), 
        ("future (0.6)", gen_future_heuristic(0.6)),
        ("best_card_win", best_card_win_heuristique), 
        # ("hand point", hand_heuristic)
    ]:
        for aggregator in [
            #("mean + utility", min_utility),
            ("cutoff 25%", gen_cutoff_agregator(.25)),
            ("mean", statistics.mean),
            ("min", min),
            ("cutoff 45%", gen_cutoff_agregator(.45))
        ]:
            for kick_in in [
                ("5", 5),
                ("10", 10)
            ]:
                for other in [
                    ("random bot", random_strategy()),
                    # ("highest bot", highest_strategy())
                ]:
                    for starting in [
                        (f"DP vs {other[0]}", True),
                        (f"{other[0]} vs DP", False)
                    ]:
                        print(f"{starting[0]} -- heuristic={heuristic[0]}, aggregator={aggregator[0]}, kick_in={kick_in[0]}", end="")
                        sys.stdout.flush()
                        gen_dp = lambda: dp_strategy(kick_in[1], heuristic[1], aggregator[1])

                        total_score = [0, 0, 0, 0]
                        for i in range(100):
                            if i % 10 == 0:
                                print(".", end="")
                                sys.stdout.flush()

                            strategies_start = [
                                gen_dp(), 
                                other[1], 
                                gen_dp(), 
                                other[1]
                            ]

                            strategies_second = [
                                other[1],
                                gen_dp(), 
                                other[1], 
                                gen_dp() 
                            ]
                            game_score = game(verbose=False, strategies= strategies_start if starting[1] else strategies_second)
                            total_score = add(game_score, total_score)
                        
                        print_score(total_score)
                        sys.stdout.flush()




