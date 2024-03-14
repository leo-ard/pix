# The Game of 10 (card game)
The game of 10 is a classic [trick-taking card game](https://en.wikipedia.org/wiki/Trick-taking_game) with trump. The [rules of the game of 10](https://wiki.aediroum.ca/wiki/Jeu_du_10) can be summarize as:
- Strongest card (ace) win the trick
- Ace's and 10's are worth 10 points, 5's is worth 5 points
- Winner of the bet phase start the play and choose the trump
- classic trick-taking game
- Team of two players (sharing same pool of points)
- Plays with a deck of 40 cards (normal deck without cards 2, 3, 4 of each suit)

## Relevance to the course
The game could seem hard to modelize from a dynamic programming point of view. The game is a team game with 4 players with incomplete information about the others player's hand.

However, we believe that we can find a dynamic programming modelization that works for this game, for example, by modelizing the hidden state by random variables. To prouve that some kind of modelization exists, we will try to modelize a simpler version of this game without any hidden state or trump card. We will also assume that we play first. 

First, let's have some definitions :
- $D = \\{ 5\heartsuit, 6\heartsuit, ..., K\heartsuit, A\heartsuit, 5\clubsuit, ..., A\clubsuit, ..., A\diamondsuit \\}$ : the deck. This represents all cards that we can have in the game. We have $|D| = 40$.
- $H_i \subset D, |H_i| = 10$, the hand of player $i$. We can see that we have $H_i \cap H_j = \emptyset ~~\forall i, j \in \{0, 1, 2, 3\}, i \neq j$, in other words, no player has the same cards.
- $POINTS(c_0, c_1, c_2, c_3)$ : the points that we get if cards $c_0, c_1, c_2, c_3$ are on the table in this order. We are represented by player 0, so $c_0$ would be our card. Note that the points can be negative if we lose the round. 
- We define $u^i_k$ as the card played by the $i^{th}$ player at stage k
- We define the state $x_k$ as the card detained by the four players $(H_0, H_1, H_2, H_3)$. The hands are known at the start.

With those definition we can see the following Bellman equation:

$$
\begin{align}
J_N(H_0, H_1, H_2, H_3) =& 0\\
J_k(H_0, H_1, H_2, H_3) =& \max_{u^0_k \in V(H_0)} \min_{[u^i_k \in V(H_i), i \in \\{0,1,2\\}]} \\{ POINTS(u^0_k, u^1_k, u^2_k, u^3_k) + J_{k+1}(H_0 \setminus \\{u^0_k\\}, H_1 \setminus \\{ u^1_k \\}, H_2\setminus \\{ u^2_k \\}, H_3\setminus \\{ u^3_k \\}) \\}
\end{align}
$$

We see that this problem is relevant and we were able to have some kind of modelization. However, this doesn't modelize the game completely as we handwaved a few core concept. Our goal during the project would be to extend the modelizaiton to include all elements of the game, such as : 
- The hidden state. Other's player hand are not known.
- The fact that we do not play first every round. The winner of the last trick start the next one.
- No trump suit
- Modelize the way players play by incorporing a concept of strategy. We could explore greedy strategy, always playing the highest or the lowest. However, those might not be the optimal way to play.
- We do not make assumption about the distribution with the result of the bet winner.

One idea to modelize the hidden state would be to see the player's hand as a belief that gets updated at each played card. The probability that a card is in a player's deck is shared among other. At the beggining of the game, the cards that are not in our own hand are shared at 33% in others hand.

If a player doesn't follow a suit, the probability that he has a card in the said suit drop to 0. This is a strong assumption as it is part of the game rules. However, we could test "weak" assumption pretending that other players play strategically. For example, they could try to protect a strong card by playing his lowest card if he cannot win the current trick. Assuming this strategy, we could lower the chance that the-said player has a lower card then the one he just played. Those kind of stategy are seen in humain play and seems to be optimal.

## Objective
Recently, the AEDIROUM (the computer science association) launched a contest to create the best bot of 10. Bots submission are going to play random hand thousands of time to statically mesure their performance. The competition submission deadline is at the end of March. An arbitrer that gives correct hand and let bots play against each other is already made by fellow phD Matteo Delabré, so it will be easy to test our bot and play against it. As a milestone of this project, we want to prove feasability and superiority of dynamic programming by winning the competition.

In order, here what we intend to do:
- Modelize the simpler version of the game with hidden state.
- Modelize the complete game with hidden state, trump card, strategy, etc. Without the betting phase.
- Implement it in a programming language.
- Submit it to the AEDIROUM competition.

Our final goal would be to have a bot that can beat us two at this game. As we are experienced player, this would prove the accuracy of the DP.
