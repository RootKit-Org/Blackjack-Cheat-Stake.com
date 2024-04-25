from blackjack import Blackjack
import matplotlib.pyplot as plt

def main():
    # Your existing code
    gamesToSimulate = 1
    startBank = 10000
    games = []
    totalBankRuns = 0
    totalHourly = 0
    totalNegHourly = 0
    totalPosHourly = 0
    totalRounds = 0
    totalEndBank = 0

    for game in range(gamesToSimulate):
        player, dealer = startBank, 0
        totalBet = 0
        rounds = []
        wins, losses = 0, 0
        bankRun = False
        for _ in range(10000):
            blackjack = Blackjack(
                decks=8,
                cutCardLocation=4,
                baseBet=10,
                spreadCutOff=-2,
                playerBank=player
            )
            result = blackjack.simulate()
            if result is None:
                bankRun = True
                break
            player = result[0]
            totalBet += result[1]
            rounds.extend(result[2])
            wins += result[3]
            losses += result[4]

        games.append({
            "startBank": startBank,
            "endBank": player,
            "totalBet": totalBet,
            "rounds": rounds,
            "wins": wins,
            "losses": losses,
            "bankRun": bankRun
        })
        if bankRun:
            totalBankRuns += 1

    for idx, game in enumerate(games):
        startBank = game["startBank"]
        player = game["endBank"]
        totalBet = game["totalBet"]
        rounds = game["rounds"]
        wins = game["wins"]
        losses = game["losses"]
        bankRun = game["bankRun"]

        totalHourly += (player-startBank)/round(len(rounds)/60)
        if player-startBank < 0:
            totalNegHourly += 1
        else:
            totalPosHourly += 1

        totalRounds += len(rounds)
        totalEndBank += player

        # print(f"\n\nGame {idx+1}:")
        # print(f"Starting Bank: {startBank}")
        # print(f"End Bank: {player}")
        # print(f"Total Bet: {totalBet}")
        # print(f"Wins: {wins}")
        # print(f"Losses: {losses}")
        print(f"Winning percentage: {wins/(wins+losses)}")

        # print(f"Rounds: {len(rounds)}")
        # print(f"Hours: {round(len(rounds)/60)}")
        # print(f"$ per hour: {(player-startBank)/round(len(rounds)/60)}")

    print(f"\n\nTotal Games: {gamesToSimulate}")
    print(f"Starting Bank: ${startBank}")
    print(f"Average Rounds per game: {round(totalRounds/gamesToSimulate, 2)}")
    print(f"Average End Bank: ${round(totalEndBank/gamesToSimulate, 2)}")
    print(f"Bank Run Percentage: {round((totalBankRuns/gamesToSimulate)*100, 2)}%")
    print(f"Average Hourly: ${round(totalHourly/gamesToSimulate, 2)}")
    print(f"Positive Hourly Percentage: {round((totalPosHourly/gamesToSimulate)*100, 2)}%")
    print(f"Negative Hourly Percentage: {round((totalNegHourly/gamesToSimulate)*100, 2)}%")

    # Plotting code
    plt.plot(rounds)
    plt.title('Blackjack Rounds')
    plt.xlabel('Round Number')
    plt.ylabel('Value')
    plt.show()


if __name__ == "__main__":
    main()