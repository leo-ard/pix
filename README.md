# Game of 10 (card game)
The game of 10 is a classic [trick-taking card game](https://en.wikipedia.org/wiki/Trick-taking_game) with trump. The [rules of the game of 10](https://wiki.aediroum.ca/wiki/Jeu_du_10) can be summarize as:
- Strongest card (ace) win the trick
- Ace's and 10's are worth 10 points, 5's is worth 5 points
- Winner of the bet phase start the play and choose the trump
- classic trick-taking game
- Team of two players (sharing same pool of points)
- Plays with a deck of 40 cards (normal deck without cards 2, 3, 4 of each suit)

## Relevance to the course
The game could seem hard to modelize from a dynamic programming point of view. The game is a team game with 4 players with incomplete information about the others player's hand.

However, we believe that we can find a dynamic programming modelization that works for this game, for example, by modelizing the hidden state by random variables. To prouve that some kind of modelization exists, we will try to modelize a simpler version of this game without any hidden state, trump card. We will also assume that we play first. 

First, let's have some definitions :
- $D = \\{ 5\heartsuit, 6\heartsuit, ..., K\heartsuit, A\heartsuit, 5\clubsuit, ..., A\clubsuit, ..., A\diamondsuit \\}$ : the deck. This represents all cards that we can have in the game. We have $|D| = 40$.
- $H_i \subset D, |H_i| = 10$, the hand of player $i$. We can see that we have $H_i \cap H_j = \emptyset ~~\forall i, j \in \{0, 1, 2, 3\}, i \neq j$, in other words, no player has the same cards.
- $POINTS(c_0, c_1, c_2, c_3)$ : the points that we get if cards $c_0, c_1, c_2, c_3$ are on the table in this order. We are represented by player 0, so $c_0$ would be our card. Note that the points can be negative if we lose the round. 
- $S(P_i) : 2^D \rightarrow D$ : a strategy. This function takes a set of cards in the hand and returns a playable card. This function may take additional information such as the cards on the table or could just return the highest playable card.
- we define u^i_k as the card played by the i^{th} player at stage k
- We define the state x as the card detained by the four players. The hand are known at the start.

With those definition we can see the following Bellman equation:

$$
\begin{align}
J(H_0, H_1, H_2, H_3) = \max_{u \in H_0} \\{ POINTS(u^0_k, S_{u^0_k}(H_1), S_{u^0_k,u^1_k}(H_2), S_{u^0_k,u^1_k,u^2_k}(H_3)) + J_k(H_0 \setminus \{u^0_k\}, H_1 \setminus \{ S(H_1) \}, H_2\setminus \{S(H_2)\}, P_3\setminus \{S(H_3)\}) \\}
\end{align}
$$

We see that this problem is relevant and we were able to have some kind of modelization. However, this doesn't modelize the game very much as we handwaved a few core concept such as : 
- The hidden state. Other's player hand are not known.
- The fact that we do not play first every round. The winner of the last trick start the next one.
- No trump suit
- Each player doesn't necessarily have the same strategy : different kind of strategy exists. We could explore greedy strategy, always playing the highest or the lowest. However, those might not be the optimal way to play.
- We do not make assumption about the distribution with the result of the bet winner.

We think we can generalize the hidden state as probability. We could see the probability that a player play has a belief that gets updated at each played card. The probability that a card is in a player's deck is shared among other. At the beggining of the game, the cards that are not in our own hand are shared at 33% in others hand.

If a player doesn't follow a suit, the probability that he has a card in the said suit drop to 0. This is a strong assumption as it is part of the game rules. However, we could test "weak" assumption pretending that other players play strategically. For example, they could try to protect a strong card by playing his lowest card if he cannot win the current trick. Assuming this strategy, we could lower the chance that the-said player has a lower card then the one he just played. Those kind of stategy are seen in humain play and seems to be optimal.


## Objective
Recently, the AEDIROUM (the computer science association) launched a contest to create the best bot of 10... explain more about the contest and that the deadline is by the end of this month. We could try to have a nice rating at this contest as part of the objective of this project

- Have a modelization that let's us write a program that can beat us two at this game. As we are experienced player, this would prove the accuracy of the DP.
