from blackjack import Blackjack
import matplotlib.pyplot as plt
import multiprocessing
import colorama
from colorama import Fore

colorama.init(autoreset=True)

GAMES_TO_SIMULATE = 1000
SHOES_TO_SIMULATE = 100

def simulate_game(args):
    startBank = 1000
    playerBank = startBank

    totalBet = 0
    rounds = []
    wins, losses, ties = 0, 0, 0
    bankRun = False

    # Simulate multiple shoes
    for _ in range(SHOES_TO_SIMULATE):
        blackjack = Blackjack(
            decks=8,
            cutCardLocation=4,
            baseBet=5,
            spreadCutOff=-2,
            playerBank=playerBank
        )

        result = blackjack.simulate()

        if result is None:
            bankRun = True
            break
        playerBank = result.bank
        rounds.extend(result.rounds)
        wins += result.wins
        losses += result.losses
        ties += len(result.rounds) - (result.wins + result.losses)

    return {
        "startBank": startBank,
        "endBank": playerBank,
        "rounds": rounds,
        "wins": wins,
        "losses": losses,
        "ties": ties,
        "bankRun": bankRun
    }

def main():
    games = []
    totalBankRuns = 0
    totalHourly = 0
    totalNegHourly = 0
    totalPosHourly = 0
    totalRounds = 0
    totalEndBank = 0

    with multiprocessing.Pool() as pool:
           
        games = pool.map(simulate_game, range(GAMES_TO_SIMULATE))
        totalBankRuns = sum(game["bankRun"] for game in games)

    for idx, game in enumerate(games):
        startBank = game["startBank"]
        playerBank = game["endBank"]
        rounds = game["rounds"]
        wins = game["wins"]
        losses = game["losses"]
        bankRun = game["bankRun"]

        try:
            totalHourly += (playerBank-startBank)/round(len(rounds)/60)
        except ZeroDivisionError:
            totalHourly += 0

        if playerBank-startBank < 0:
            totalNegHourly += 1
        else:
            totalPosHourly += 1

        totalRounds += len(rounds)
        totalEndBank += playerBank

        if False:
            print(f"\n\nGame {idx+1}:")
            print(f"Starting Bank: {startBank}")
            print(f"End Bank: {playerBank}")
            print(f"Wins: {wins}")
            print(f"Losses: {losses}")
            print(f"Winning percentage: {wins/(len(rounds))}")
            print(f"Lossing percentage: {losses/(len(rounds))}")
            print(f"Ties percentage: {ties/(len(rounds))}")

            print(f"Rounds: {len(rounds)}")
            print(f"Hours: {round(len(rounds)/60)}")
            print(f"$ per hour: {(playerBank-startBank)/round(len(rounds)/60)}")

    print(f"\n\n{Fore.BLUE}Total Games:{Fore.RESET} {GAMES_TO_SIMULATE}")
    print(f"{Fore.BLUE}Starting Bank:{Fore.RESET} ${startBank}")
    print(f"{Fore.BLUE}Average Rounds per game:{Fore.RESET} {round(totalRounds/GAMES_TO_SIMULATE, 2)}")
    print(f"{Fore.BLUE}Average End Bank:{Fore.RESET} ${round(totalEndBank/GAMES_TO_SIMULATE, 2)}")
    print(f"{Fore.BLUE}Bank Run Percentage:{Fore.RESET} {round((totalBankRuns/GAMES_TO_SIMULATE)*100, 2)}%")
    print(f"{Fore.BLUE}Average Hourly:{Fore.RESET} ${round(totalHourly/GAMES_TO_SIMULATE, 2)}")
    print(f"{Fore.BLUE}Positive Hourly Percentage:{Fore.RESET} {round((totalPosHourly/GAMES_TO_SIMULATE)*100, 2)}%")
    print(f"{Fore.BLUE}Negative Hourly Percentage:{Fore.RESET} {round((totalNegHourly/GAMES_TO_SIMULATE)*100, 2)}%")

    # Plotting code
    # TODO Rounds show last game, should be something more useful
    plt.plot(rounds)
    plt.title('Blackjack Rounds')
    plt.xlabel('Round Number')
    plt.ylabel('Value')
    plt.show()


if __name__ == "__main__":
    main()