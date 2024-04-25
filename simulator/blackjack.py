import random

class Blackjack:
    def __init__(
            self,
            decks=8,
            cutCardLocation=4,
            cards=[2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11],
            players=3,
            playerBank=1000,
            baseBet=5,
            spreads=[
                [2, 2],
                [3, 4],
                [5, 8],
            ],
            spreadCutOff=-2,
            blackjackPayout=2.5
    ):
        self.decks = decks
        self.cutCardLocation = cutCardLocation
        self.cards = cards
        self.players = players
        self.deck = []

        self.playerBank = playerBank
        self.baseBet = baseBet
        self.spreads = sorted(spreads, reverse=True)
        self.spreadCutOff = spreadCutOff
        self.blackjackPayout = blackjackPayout

        self.runningCount = 0
        
    def dealCard(self):
        """Deal a card from the deck and count it."""

        card = self.deck.pop()
        self.countCard(card)
        return card

    def countCard(self, card):
        """Count the card and update the running count."""

        if card in [2, 3, 4, 5, 6]:
            self.runningCount += 1
        elif card in [10, 11]:
            self.runningCount -= 1

    def shuffleDeck(self):
        """Shuffle the deck and reset the running count."""

        # 4x is the base cards in a deck x 4
        self.deck = (self.cards * 4) * self.decks
        random.shuffle(self.deck)

    def calculateScore(hand: list):
        """Calculate the score of a hand. If the hand is a soft hand, return the highest possible score."""

        score = sum(hand)
        if score > 21 and 11 in hand:
            hand[hand.index(11)] = 1
            score = sum(hand)
        return score

    def basicStrategy(self, player_hand, dealer_hand):
        """Return the basic strategy for the player's hand."""
        player_score = Blackjack.calculateScore(player_hand)
        dealer_score = dealer_hand[0]

        soft = 11 in player_hand
        if soft:
            score = sum(player_hand)
            if score > 21:
                soft = False

        # Hard
        if not soft:
            if player_score in [13, 14, 15, 16]:
                if dealer_score < 7:
                    return "stand"
                else:
                    return "hit"
            elif player_score == 12:
                if dealer_score in [4, 5, 6]:
                    return "stand"
                else:
                    return "hit"
            elif player_score == 11:
                return "double"
            elif player_score == 10:
                if dealer_score in [10, 11]:
                    return "hit"
                else:
                    return "double"
            elif player_score == 9:
                if dealer_score in [3, 4, 5, 6]:
                    return "double"
                else:
                    return "hit"
            elif player_score <= 8:
                return "hit"

            return "stand"
            
        # Soft
        else:
            if player_score >= 19:
                if dealer_score in [6]:
                    return "double"
                return "stand"
            elif player_score == 18:
                if dealer_score in [3, 4, 5, 6]:
                    return "double"
                elif dealer_score in [9, 10, 11]:
                    return "hit"
                return "stand"
            elif player_score == 17:
                if dealer_score in [3, 4, 5, 6]:
                    return "double"
                return "hit"
            elif player_score in [15, 16]:
                if dealer_score in [4, 5, 6]:
                    return "double"
                return "hit"
            elif player_score == [13, 14]:
                if dealer_score in [5, 6]:
                    return "double"
                return "hit"
            else:
                return "hit"

    def split(player_hand, dealer_hand):
        """Return whether the player should split their hand."""

        if player_hand[0] == player_hand[1]:
            if player_hand[0] == 11:
                return True

            elif player_hand[0] == 9 and not dealer_hand[0] in [7, 10, 11]:
                return True

            elif player_hand[0] == 8:
                return True
            
            elif player_hand[0] == 7 and dealer_hand[0] < 8:
                return True
            elif player_hand[0] == 6 and dealer_hand[0] < 7:
                return True
            # elif player_hand[0] == 4 and dealer_hand[0] < 7:
            #     return True
            elif player_hand[0] in [2, 3] and dealer_hand[0] < 8:
                return True
            
        return False

    def simulate(self):
        dealerWinnings = 0
        self.runningCount = 0

        self.shuffleDeck()

        rounds = []
        wins = 0
        losses = 0
        runningBet = 0

        while len(self.deck) > (self.cutCardLocation*52):

            player_hands = [[self.dealCard(), self.dealCard()]]
            dealer_hand = [self.dealCard(), self.dealCard()]

            for other in range(self.players):
                self.dealCard()
                self.dealCard()

            trueCount = self.runningCount / (len(self.deck)/52)

            # TODO something is wrong with the count
            # we currently make way more money when the count is negative
            if trueCount <= self.spreadCutOff:
                continue

            bet = self.baseBet
            # Growing bet based off spread and true count
            for item in self.spreads:
                if trueCount >= item[0]:
                    bet = item[1] * self.baseBet
                    break
            
            # Placing bet and removing from bank
            runningBet += bet
            self.playerBank -= bet

            roundLive = True
            currentHand = len(player_hands)
            handSplit = False

            # Check if we have pair and should split
            # We only split once, modify if you want infinite
            if Blackjack.split(player_hands[0], dealer_hand):
                player_hands.append([player_hands[0].pop(), self.dealCard()])
                player_hands[0].append(self.dealCard())

                # Pay bet for splitting
                self.playerBank -= bet

                # TODO letting us do inifite splits if we add it later on
                handSplit = True

            if self.playerBank < 0:
                return None

            # Loop through all hands
            for player_hand in player_hands:
                # 1. If dealer has an ace, offer insurance
                # 2. Dealer check if they have BJ
                # 3. If dealer has BJ, check if player has BJ, games ends instantly, push and/or payout insurance

                # 4. If dealer didn't have BJ, player plays
                # 5. If player has BJ, player wins 3:2
                
                # 6. Play can hit, stand, double, split

                roundLive = True
                insurance = False
                doubled = False

                player_score = Blackjack.calculateScore(player_hand)
                dealer_score = Blackjack.calculateScore(dealer_hand)

                # TODO double check the player gets paid immediately
                # when dealer also had BJ
                if player_score == 21:
                    self.playerBank += bet*self.blackjackPayout
                    wins += 1

                    roundLive = False

                else:
                    if dealer_hand[0] == 11:
                        # Player is offered insurance
                        if trueCount >= 3:
                            self.playerBank -= bet / 2
                            insurance = True

                    if dealer_score == 21:
                        if insurance:
                            self.playerBank += bet

                        losses += 1
                        roundLive = False


                # Playing thru the round with 1 hand
                while roundLive:
                    action = self.basicStrategy(player_hand, dealer_hand)

                    # Stake doesn't allow double after split
                    if handSplit and action == "double":
                        action = "hit"

                    if action == "hit":
                        player_hand.append(self.dealCard())
                        continue

                    elif action == "double":
                        player_hand.append(self.dealCard())

                        doubled = True
                        self.playerBank -= bet

                    player_score = Blackjack.calculateScore(player_hand)

                    if player_score > 21:
                        losses += 1
                        roundLive = False
                        break

                    # if we get here, player is done with getting cards
                    # dealer plays out their hand
                    while dealer_score < 17:
                        dealer_hand.append(self.dealCard())
                        dealer_score = Blackjack.calculateScore(dealer_hand)

                    # Check who won
                    gameConclusion = "push"
                    if dealer_score > 21:
                        gameConclusion = "win"
                    elif dealer_score > player_score:
                        gameConclusion = "loss"
                    elif dealer_score < player_score:
                        gameConclusion = "win"


                    if gameConclusion == "win":
                        if doubled:
                            self.playerBank += bet*2

                        self.playerBank += bet*2
                        wins += 1

                    elif gameConclusion == "push":
                        if doubled:
                            self.playerBank += bet
                        self.playerBank += bet
                    else:
                        losses += 1

                    roundLive = False
                    break


                rounds.append(self.playerBank)

        return self.playerBank, runningBet, rounds, wins, losses
