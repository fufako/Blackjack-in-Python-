import random
import time


class Deck:
    def __init__(self):
        self.cards = 4 * [
            2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11,
            2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11,
            2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11,
            2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11,
        ]

        self.len = len(self.cards)

    def reset(self):
        self.cards = 4 * [
            2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11,
            2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11,
            2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11,
            2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11,
        ]

    def print(self):
        return self.cards

    def shuffle(self):
        random.shuffle(self.cards)

    def is_time_to_shuffle(self):
        return len(self.cards) < (self.len/2)

    def time_to_shuffle(self):
        print("Reshuffling...")
        time.sleep(1)
        self.reset()
        self.shuffle()

    def get_a_card(self):
        return self.cards.pop(0)


class Hand:
    def __init__(self):
        self.hand = []

    def reset(self):
        self.hand = []

    def print(self):
        return self.hand

    def draw_a_card(self, deck):
        self.hand.append(deck.get_a_card())

    def hand_score(self):
        self.score = 0
        for card in self.hand:
            self.score += card
            if self.score > 21 and card == 11:
                card = 1
        return self.score


class Player(Hand):
    def __init__(self, money, bet=0):
        super().__init__()
        self.alive = True
        self.profit = 0
        self.money = money
        self.blackjack = False
        self.bet = bet

    def reset(self):
        self.hand = []
        self.alive = True
        self.profit = 0

    def deal_cards(self, deck):
        self.draw_a_card(deck)
        self.draw_a_card(deck)
        print('Player cards: {}'.format(self.print()))
        self.blackjack = self.check_blackjack()

    def check_blackjack(self):
        if self.hand_score == 21:
            return True
        return False

    def add_money(self, money):
        self.money += int(money)

    def remove_money(self, money):
        self.money -= int(money)

    def print_balance(self):
        return 'Your balance is currently: {}$'.format(self.money)

    def bets(self):
        while True:
            self.print_balance()
            bet = input('How much would you like to bet?')
            if not bet.isdecimal():
                continue
            if int(bet) > self.money:
                print('You do not have enough money!')
            else:
                print('Bet placed !')
                self.bet = int(bet)
                self.remove_money(int(bet))
                break

    def gameplay(self, deck):
        while True:
            if self.hand_score() > 21 or self.blackjack:
                self.alive = False
                break
            print('Your sum is {}.'.format(self.hand_score()))
            act = input('Would you like to hit or stand? Type h or s: ')
            if act == 'h' or act == 'H':
                self.draw_a_card(deck)
            if act == 's' or act == "S":
                break

    def results(self, dealer):
        if self.alive and dealer.alive:
            if self.hand_score() > dealer.hand_score():
                print('You win!\n')
                self.profit = 2
            elif self.hand_score() == dealer.hand_score():
                print('Draw!\n')
                self.profit = 1
            else:
                print('You lose!')
        elif not self.alive:
            if self.blackjack:
                print("BLACKJACK!\n")
                self.profit = 2.5
            else:
                print("BUST! You lose!\n")
        else:
            print("DEALER BUSTS. YOU WIN!\n")
            self.profit = 2
        self.settle()

    def settle(self):
        self.add_money(self.profit*self.bet)


class Dealer(Hand):

    def __init__(self):
        super().__init__()
        self.alive = True

    def reset(self):
        self.hand = []
        self.alive = True
        self.profit = 0

    def dealer_print(self):
        return str(self.hand[0]) + ' ?'

    def deal_cards(self, deck):
        self.draw_a_card(deck)
        self.draw_a_card(deck)
        print('Dealer cards: {}'.format(self.dealer_print()))
        self.blackjack = self.check_blackjack()

    def check_blackjack(self):
        if self.hand_score == 21:
            return True
        return False

    def dealer_move(self, deck):
        while True:
            print('Dealer sum is: {}'.format(self.hand_score()))
            if self.hand_score() in range(17, 22):
                return True
            if self.hand_score() > 21:
                self.alive = False
                return False
            if self.hand_score() < 17:
                self.draw_a_card(deck)


def play_again():
    question = input('Would you like to play another round? [y / n]: ')
    if question == 'y':
        return True
    return False


def game():
    player_start_money = 100
    deck = Deck()
    player = Player(player_start_money)
    dealer = Dealer()
    deck.shuffle()
    while True:
        if player.money == 0:
            print('Out of money!')
            break
        if deck.is_time_to_shuffle():
            deck.shuffle()

        print(player.print_balance())
        player.bets()
        dealer.deal_cards(deck)
        player.deal_cards(deck)

        player.gameplay(deck)
        if player.alive:
            dealer.dealer_move(deck)
        player.results(dealer)
        print(player.print_balance())
        if play_again():
            player.reset()
            dealer.reset()
            continue
        else:
            break


if __name__ == "__main__":
    game()
