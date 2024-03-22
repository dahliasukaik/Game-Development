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


"""This module is where player is created"""


class Player:
    """This class contains functions for the player"""

    def __init__(self, name, balance=10000):
        """This function stores name and other variables"""
        self.name = name
        self.balance = balance
        self.hand = []

    def __str__(self):
        """this returns name and the balance as string"""
        return f"{self.name} (balance: ${self.balance})"

    def bet(self, amount):
        """This function is how players make bets"""
        if amount > self.balance:
            raise ValueError("Not enough balance!")
        self.balance -= amount

    def add_to_balance(self, amount):
        """This functions add money to players balance"""
        self.balance += amount
