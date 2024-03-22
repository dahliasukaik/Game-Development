# dahliasukaik
# CPSC 386-02
# 2023-02-26
# dahliasukaik@csu.fullerton.edu
# @dahliasukaik
#
# M2: Blackjack
#
# This my first project and it's a Blackjack game!
#


"""This module is where most of the rules are executed"""

import pickle

from .cards import Card
from .player import Player


STARTING_BALANCE = 10000
BALANCE_FILE = "balances.pickle"

RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]

VALUES = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 10,
    "Q": 10,
    "K": 10,
    "A": 11,
}


def init_deck():
    """This function makes the deck"""
    deck = []
    for suit in SUITS:
        for rank in RANKS:
            card = Card(rank, suit)
            deck.append(card)
    return deck


def deal_card(deck):
    """This functions deals a card from deck"""
    return deck.pop()


def get_hand_value(hand):
    """This functions returns the value of the card"""
    hand_value = sum([VALUES[card.rank] for card in hand])
    num_aces = sum([1 for card in hand if card.rank == "A"])
    while hand_value > 21 and num_aces > 0:
        hand_value -= 10
        num_aces -= 1
    return hand_value


def show_hand(hand):
    """This function shows the card to the player"""
    for card in hand:
        print(card)


def play_blackjack():
    """This function executes the game for players to play and make choices"""
    print("Welcome to Blackjack!")

    players = []
    try:
        with open(BALANCE_FILE, "rb") as file:
            balances, saved_players, deck = pickle.load(file)
            for saved_player in saved_players:
                if saved_player.name not in [p.name for p in players]:
                    players.append(saved_player)
        if not players:
            raise ValueError("no players loaded from file")
    except (FileNotFoundError, ValueError):
        balances = {}
        deck = init_deck()

    num_players = int(input("How many players? (1-4): "))

    for i in range(num_players):
        while True:
            name = input(f"What is player {i+1}'s name? ")
            if name not in balances:
                player = Player(name)
                players.append(player)
                balances[player.name] = STARTING_BALANCE
                break
            else:
                print("This name is already taken please choose another! ")

    while True:
        with open(BALANCE_FILE, "wb") as file:
            pickle.dump((balances, players, deck), file)

        for player in players:
            player.hand.clear()

            print(player)
            bet = int(input(f"How much would you like to bet?"))
            player.bet(bet)
            player.hand.extend([deal_card(deck), deal_card(deck)])

            print(f"{player.name}, your hand is:")
            show_hand(player.hand)

            while True:
                hand_value = get_hand_value(player.hand)

                if hand_value == 21:
                    print("Blackjack!")
                    player.add_to_balance(bet * 2.5)
                    break

                elif hand_value > 21:
                    print("Bust!")
                    break

                else:

                    print(f"Your hand value is {hand_value}")

                    hit_or_stand = input("Would you like to hit or stand? (h/s): ")
                    if hit_or_stand == "h":
                        player.hand.append(deal_card(deck))

                        print(f"{player.name}, your hand is now:")
                        show_hand(player.hand)

                    else:
                        break

            print(
                f"{player.name}, your final hand value is {get_hand_value(player.hand)}"
            )
        dealer_hand = [deal_card(deck), deal_card(deck)]

        print("Dealer's hand is:")
        print(dealer_hand[0])

        while get_hand_value(dealer_hand) < 17:
            dealer_hand.append(deal_card(deck))

            print("Dealer hits.")
            print(f"Dealer's hand is now:")

            show_hand(dealer_hand)

        dealer_hand_value = get_hand_value(dealer_hand)

        if dealer_hand_value > 21:
            print("Dealer busts!")

            for player in players:
                player.add_to_balance(bet * 2)

        else:
            print(f"Dealer's final hand value is {dealer_hand_value}")
            for player in players:
                player_hand_value = get_hand_value(player.hand)

                if player_hand_value > 21:
                    print(f"{player.name} busts!")

                elif player_hand_value > dealer_hand_value:
                    print(f"{player.name} wins!")
                    player.add_to_balance(bet * 2)

                elif player_hand_value == dealer_hand_value:
                    print(f"{player.name} pushes!")
                    player.add_to_balance(bet)

                else:
                    print(f"{player.name} loses!")

        for player in players:
            print(f"{player.name}, your balance is now ${player.balance}")

        play_again = input("Would you like to play again? (y/n): ")

        if play_again != "y":
            break

    with open(BALANCE_FILE, "wb") as f:
        pickle.dump((balances, players, deck), f)

    print("Thanks for playing!")
