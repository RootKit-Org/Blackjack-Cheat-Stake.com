import random

class Blackjack:
    def __init__(self):
        self.decks = 8
        self.cutCardLocation = 4
        self.cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
        self.players = 3
        self.deck = []

        self.playerBank = 1000

        self.runningCount = 0
        
    def dealCard(self):
        card = self.deck.pop()
        self.countCard(card)
        return card

    def countCard(self, card):
        if card in [2, 3, 4, 5, 6]:
            self.runningCount += 1
        elif card in [10, 11]:
            self.runningCount -= 1

    def shuffleDeck(self):
        self.deck = (self.cards * 4) * self.decks
        random.shuffle(self.deck)

    def calculateScore(hand: list):
        score = sum(hand)
        if score > 21 and 11 in hand:
            hand[hand.index(11)] = 1
            score = sum(hand)
        return score

    def basicStrategy(self, player_hand, dealer_hand):
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
                if dealer_score == 11:
                    return "hit"
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
            elif player_hand[0] == 4 and dealer_hand[0] < 7:
                return True
            elif player_hand[0] in [2, 3] and dealer_hand[0] < 8:
                return True
            

        return False

    def simulate(self, playerWinning=0):
        if playerWinning > 0:
            self.playerBank = playerWinning
        dealerWinnings = 0
        self.runningCount = 0

        self.shuffleDeck()

        rounds = []
        wins = 0
        losses = 0
        totalBet = 0


        while len(self.deck) > (self.cutCardLocation*52):

            player_hands = [[self.dealCard(), self.dealCard()]]
            dealer_hand = [self.dealCard(), self.dealCard()]

            for other in range(self.players):
                self.dealCard()
                self.dealCard()

            trueCount = self.runningCount / (len(self.deck)/52)

            if trueCount <= -2:
                continue

            baseBet = 5
            if trueCount >= 5:
                bet = baseBet * 5
            elif trueCount >= 4:
                bet = baseBet * 3
            elif trueCount >= 3:
                bet = baseBet * 3
            if trueCount >= 2:
                bet = baseBet * 2
            elif trueCount >= 1:
                bet = baseBet * 2
            else:
                bet = baseBet
            # bet = baseBet

            self.playerBank -= bet
            totalBet += bet

            roundLive = True
            playerDouble = False

            currentHand = len(player_hands)
            handSplit = False
            for i in range(currentHand):
                if Blackjack.split(player_hands[i], dealer_hand):
                    player_hands.append([player_hands[i].pop(), self.dealCard()])
                    player_hands[i].append(self.dealCard())
                    totalBet += bet
                    self.playerBank -= bet
                    handSplit = True

            if self.playerBank < 0:
                return None

            for player_hand in player_hands:
                roundLive = True
                while roundLive:
                    player_score = Blackjack.calculateScore(player_hand)
                    dealer_score = Blackjack.calculateScore(dealer_hand)

                    if dealer_score == 21:
                        if trueCount >= 3:
                            self.playerBank += bet * .5
                        else:
                            dealerWinnings += bet
                        losses += 1
                        roundLive = False

                    if player_score == 21:
                        # print("Blackjack! You win!")
                        self.playerBank += 2.5 * bet
                        wins += 1
                        roundLive = False
                    elif player_score > 21:
                        # print("Bust! You lose!")
                        dealerWinnings += bet
                        losses += 1
                        roundLive = False
                    else:

                        action = self.basicStrategy(player_hand, dealer_hand)

                        if action == "hit":
                            player_hand.append(self.dealCard())
                            player_score = Blackjack.calculateScore(player_hand)

                        else:
                            if action == "double":
                                player_hand.append(self.dealCard())
                                player_score = Blackjack.calculateScore(player_hand)
                                self.playerBank -= bet
                                totalBet += bet
                                if not handSplit:
                                    self.playerBank -= bet
                                    totalBet += bet
                                else:
                                    action = "hit"

                                if player_score > 21:
                                    # print("Bust! You lose!")
                                    dealerWinnings += bet
                                    losses += 1
                                    roundLive = False

                            while dealer_score < 17:
                                dealer_hand.append(self.dealCard())
                                dealer_score = Blackjack.calculateScore(dealer_hand)
                                # print(f"Dealer's hand: {dealer_hand}")

                            if dealer_score > 21:
                                # print("Dealer busts! You win!")
                                self.playerBank += bet * 2
                                wins += 1
                                roundLive = False
                            elif dealer_score > player_score:
                                # print("Dealer wins!")
                                dealerWinnings += bet
                                losses += 1
                                roundLive = False
                            elif dealer_score < player_score:
                                # print("You win!")
                                if action == "double":
                                    self.playerBank += (bet*2) * 2
                                else:
                                    self.playerBank += bet * 2
                                wins += 1
                                break
                            else:
                                # print("It's a tie!")
                                if action == "double":
                                    self.playerBank += bet * 2
                                else:
                                    self.playerBank += bet
                                roundLive = False

                rounds.append(self.playerBank)

        return self.playerBank, totalBet, rounds, wins, losses
