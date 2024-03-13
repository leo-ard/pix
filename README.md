# Game of 10 (card game)
The game of 10 is a classic [trick-taking card game](https://en.wikipedia.org/wiki/Trick-taking_game) with trump. The [rules of the game of 10](https://wiki.aediroum.ca/wiki/Jeu_du_10) can be summarize as:
- Strongest card (ace) win the trick
- Ace's and 10's are worth 10 points, 5's is worth 5 points
- Winner of the bet phase start the play and choose the trump
- classic trick-taking game
- Team of two players (sharing same pool of points)
## Relevance to the course
The game could seem hard to modelize from a dynamic programming point of view. Indeed, the game has some hidden state and there are 4 players, which is harder in a game-theory point-of-view.

However, I believe we can find a modelization that works for this game, by modelizing the hidden state by random variables. To prouve that some kind of modelization exists, we will try to modelize a simpler game without any hidden state or trump  and we always play first. 

First, let's have some definitions :
- $D = \{5\heartsuit, 6\heartsuit, ..., K\heartsuit, A\heartsuit, 5\clubsuit, ..., A\clubsuit, ..., A\diamondsuit \}$ : the deck. This represents all cards that we can have in the game. We have $|D| = 40$.
- $P_i \subset D, |P_i| = 10$, the set of card of player $i$. We also have $P_i \cap P_j = \emptyset ~~\forall i, j \in \{0, 1, 2, 3\}, i \neq j$, in other words, no player has the same cards

- $V(c)$ : the value that we get from a card. The value of a card is defined as such : 
$$
\begin{align}
V(5\heartsuit) = V(5\diamondsuit) = V(5\spadesuit) = V(5\clubsuit) =& 5\\
V(10\heartsuit) = V(10\diamondsuit) = V(10\spadesuit) = V(10\clubsuit) =& 10\\
V(A\heartsuit) = V(A\diamondsuit) = V(A\spadesuit) = V(A\clubsuit) =& 10\\
V(\cdot) =& 0 (\text{zero for everything else})
\end{align}
$$
- $POINTS(c_0, c_1, c_2, c_3)$ : the points that we get if cards $c_0, c_1, c_2, c_3$ are on the table in this order. We are represented by player 0, so $c_0$ would be our card. Note that the points can be negative if we lose the round. 
- $S(P_i) : 2^D \rightarrow D$ : a strategy. This function takes a set of cards in the hand and returns a playable card. This function may take additional information such as the cards on the table or could just return the highest playable card.

Now, if we define our state as $P_0, P_1, P_2, P_3$, meaning the cards that each payer has, we can see that our bellman equations become : 

$$
J(P_0, P_1, P_2, P_3) = \max_{u \in P_0} \{ POINTS(u, S(P_1), S(P_2), S(P_3)) + J(P_0\setminus \{u\}, P_1\setminus \{S(P_1)\}, P_2\setminus \{S(P_2)\}, P_3\setminus \{S(P_3)\}) \}
$$



We see that this problem is relevant and we were able to have some kind of modelization. However, this doesn't modelize the game very much as we handwaved a few core concept such as : 
- the hidden state (don't know what people have)
- the fact that we do not play first every round
- no trump card
- Each player doesn't necessarily have the same strategy 

We think we can generalize the hidden state as probability. The probability that a card is in a player's deck is shared among other others. If a player doesn't follow a suit, the probability that he has a card in the said suit drop to 0. This is a strong assumption as it is part of the game rules. However, we could test "weak" assumption pretending that other players has strategic play. For example, they could try to protect a strong card by playing his lowest card if he cannot win the trick.

The modified bellman equation would go as follow: (à modifier)
$$
J(P_0,P_1,P_2,P_3) = \underset{u\in P_0}{max} \{ POINTS(u, S(P_1), S(P_2), S(P_3)) + J(P_0\setminus \{u\}, P_1\setminus \{S(P_1)\}, P_2\setminus \{S(P_2)\}, P_3\setminus \{S(P_3)\}) \}
$$
## Objective
Recently, the AEDIROUM (the computer science association) launched a contest to create the best bot of 10... explain more about the contest and that the deadline is by the end of this month. We could try to have a nice rating at this contest as part of the objective of this project

- Have a modelization that let's us write a program that can beat us two at this game. As we are experienced player, this would prove the accuracy of the DP.