from random import shuffle
from time import sleep
from os import system


class Card():
    suits = ["spades", "diamonds", "hearts", "clubs"]
    values = [None, None, "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]

    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __repr__(self):
        return self.values[self.value] + " of " + self.suits[self.suit]

    def __add__(self, other):
        return [self, other]

class Deck():
    def __init__(self):                           # create a list, fill it with cards, shuffle the list
        self.cards = []
        for i in range(4):
            for j in range(2, 15):
                self.cards.append(Card(j, i))
        shuffle(self.cards)

    def remove_card(self):                        # deal a card
        if len(self.cards) == 0:
            return
        return self.cards.pop()

class Player():
    def __init__(self, name):
        self.name = name
        self.bankroll = 1000
        self.hand = []
        self.hand2 = []
        self.final_hand_val = 0
        self.final_hand2_val = 0
        self.blackjack = False
        self.split = False
        self.double_down = False
        self.went_split = False
        self.went_double = False
        self.display_hand_val = []

    def hand_value_check(self, hand):
        """
        Calculates hand player's hand value. Returns list of values, starting with largest one. Accounts for aces being
        either 1 or 11.
        :param hand: 
        :return: 
        """
        hand_value = 0
        ace = 0
        result = []
        a = 0
        for card in hand:  # calculate value of a hand
            if card.value < 10:
                a = card.value
            elif card.value in range(10, 14):
                a = 10
            elif card.value == 14:  # keep track of Aces that may be counted both as 11 and as 1
                a = 11
                ace += 1
            hand_value += a

        if ace > 0:                      # if hand had aces, return all possible hand values
            for i in range(0, ace + 1):
                result.append(hand_value)
                hand_value -= 10
            self.display_hand_val = result
            return result
        else:
            result.append(hand_value)
            self.display_hand_val = result
            return result

class Dealer():
    def __init__(self):
        self.name = Dealer
        self.bankroll = 1000000
        self.hand = []
        self.blackjack = False
        self.final_hand_value = 0
        self.display_hand_val = []

    def hand_value_check(self, hand):
        """
        Returns value of Dealer's hand. Unlike similar function for player, Dealer's Aces are always accounted for as
        11's, hence final return list will contain only 1 value.
        :param hand: 
        :return: 
        """
        hand_value = 0
        result = []
        a = 0
        for card in hand:                # calculate value of a hand
            if card.value < 10:
                a = card.value
            elif card.value in range(10, 14):
                a = 10
            elif card.value == 14:  # keep track of Aces that may be counted both as 11 and as 1
                a = 11
            hand_value += a

        result.append(hand_value)
        self.display_hand_val = result
        return result

class Bank():
    def __init__(self):
        self.player1_bet = 0
        self.player1_bet2 = 0

    def make_bet(self):
        while True:
            a = input("Enter the bet amount:\n")
            try:
                bet = int(a)
                break
            except:
                print("Invalid bet amount. Try again.")

        bj.player1.bankroll -= bet
        self.player1_bet = bet

class Table():
    def __init__(self):
        self.stage = "start"          # draw different stages of the game
        self.dealer_phase = False

    def draw_table(self, time=0.75):  # draw game state
        system('cls')
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        print(f"Dealer: {bj.dealer.bankroll}$".center(60))
        if self.dealer_phase is True:
            print(f"{', '.join(str(c) for c in bj.dealer.hand)}".center(60))
        elif self.stage == "natural BJ":
            print(f"{bj.dealer.hand[0]}, {bj.dealer.hand[1]}".center(60))
        elif self.stage == "start":
            print(f"{bj.dealer.hand[0]} XX".center(60))
        print("\n")
        if len(bj.dealer.display_hand_val) > 0 and self.dealer_phase is True:
            print(f"{max(bj.dealer.display_hand_val)}\n".center(60))
        else:
            print("\n")
        if self.stage == "split":
            print(f"{bj.bank.player1_bet}".center(30), f"{bj.bank.player1_bet2}\n".center(30))
        else:
            print(f"{bj.bank.player1_bet}$\n".center(60))
        if self.stage == "BJ!":
            print("BLACK JACK!\n".center(60))
        elif len(bj.player1.display_hand_val) > 0:
            if len(bj.player1.display_hand_val) > 1:             # cut 22+ display values only if there are other values to display
                temp = [x for x in bj.player1.display_hand_val if x <= 21]   # if both remaining values > 21, leave smaller one
                if len(temp) == 0:
                    bj.player1.display_hand_val = [min(bj.player1.display_hand_val)]
                else:
                    bj.player1.display_hand_val = [x for x in bj.player1.display_hand_val if x <= 21]
            print(f"{max(bj.player1.display_hand_val)}\n".center(60))
        else:
            print("\n")
        if self.stage == "split":
            print(f"{', '.join(str(c) for c in bj.player1.hand)}".center(30), "||", f"{', '.join(str(c) for c in bj.player1.hand2)}".center(30))
        else:
            print(f"{', '.join(str(c) for c in bj.player1.hand)}".center(60))
        print(f"{bj.player1.name}: {bj.player1.bankroll}$".center(60))
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")

        sleep(time)

class Game():
    def __init__(self):
        name1 = input("Player1 name is: ")
        self.player1 = Player(name1)
        self.dealer = Dealer()
        self.deck = Deck()
        self.bank = Bank()
        self.table = Table()

        print(f"{self.player1.name}, welcome to a game of BlackJack!")

    def reset(self):
        self.deck = Deck()
        self.bank = Bank()
        self.table = Table()
        self.player1.hand = []
        self.player1.hand2 = []
        self.player1.final_hand_val = 0
        self.player1.final_hand2_val = 0
        self.player1.blackjack = False
        self.player1.split = False
        self.player1.double_down = False
        self.player1.went_split = False
        self.player1.went_double = False
        self.dealer.hand = None
        self.dealer.blackjack = False
        self.dealer.final_hand_value = 0

    def play_game(self):
        """
        Main game function.
        :return: 
        """
        self.reset()
        shuffle(bj.deck.cards)  # shuffle cards

        # BETTING PHASE
        bj.bank.make_bet()

        # INITIAL CARD DEALING PHASE
        bj.player1.hand = bj.deck.remove_card()  # Deal cards to player and dealer
        #c1 = Card(10, 1)    debug option -> deal player specific cards
        #c2 = Card(3, 3)
        #bj.player1.hand = [c1, c2]
        bj.dealer.hand = bj.deck.remove_card()
        bj.player1.hand += bj.deck.remove_card()
        bj.dealer.hand += bj.deck.remove_card()

        # PRE PLAYER-CHOICE PHASE
        player_hand_val = bj.player1.hand_value_check(bj.player1.hand)      # check for natural blackjacks
        dealer_hand_val = bj.dealer.hand_value_check(bj.dealer.hand)
        bj.table.draw_table(1)
        for i in player_hand_val:
            if i == 21:
                bj.player1.blackjack = True
                bj.table.stage = "BJ!"
                bj.table.draw_table(1)
            elif i == 9 or i == 10 or i == 11:                                        # check for double down option
                bj.player1.double_down = True

        if bj.player1.hand[0].value == bj.player1.hand[1].value:            # check for split pair option
            bj.player1.split = True

        for i in dealer_hand_val:
            if i == 21:
                bj.dealer.blackjack = True

        if bj.player1.blackjack is True:                                    # pay for natural blackjack outcomes
            bj.table.stage = "natural BJ"
            bj.table.draw_table()
            if bj.dealer.blackjack is False:
                bj.player1.bankroll += bj.bank.player1_bet * 2.5
                bj.dealer.bankroll -= bj.bank.player1_bet * 1.5
                bj.table.draw_table(3)
                return
            else:
                bj.player1.bankroll += bj.bank.player1_bet
                bj.table.draw_table(3)
                return

        # PLAYER CHOICE PHASE

        def ask_user():
            """
            General function for user choice prompt. Checks for valid available player choices (hit/stand available
            always, split and DD are turned by respective flags), asks user for input, keeps asking till input is valid.
            :return: 
            """
            while True:
                if bj.player1.double_down is True and bj.player1.split is True and bj.player1.went_split is False:
                    p_choice = input("Hit, Stand, Double Down or Split?\n")
                    if p_choice != "hit" and p_choice != "stand" and p_choice != "dd" and p_choice != "double" and p_choice != "double down" and p_choice != "split":
                        print("Wrong input.\n")
                        continue
                    else:
                        return p_choice
                elif bj.player1.split is True and bj.player1.went_split is False:                   # various input prompts depending on available player choices
                    p_choice = input("Hit, Stand or Split?\n")
                    if p_choice != "hit" and p_choice != "stand" and p_choice != "split":
                        print("Wrong input.\n")
                        continue
                    else:
                        return p_choice
                elif bj.player1.double_down is True:
                    p_choice = input("Hit, Stand or Double Down?\n")
                    if p_choice != "hit" and p_choice != "stand" and p_choice != "dd" and p_choice != "double" and p_choice != "double down":
                        print("Wrong input.\n")
                        continue
                    else:
                        return p_choice
                else:
                    p_choice = input("Hit or Stand?\n")
                    if p_choice != "hit" and p_choice != "stand":
                        print("Wrong input.\n")
                        continue
                    else:
                        return p_choice

        def double_down(hand=bj.player1.hand):
            """
            Double Down function. Takes into account possible second hand if splitting choice was made. Doubles player's
            bet, deals 1 card to current hand, calculates hand value and assigns it to respective final hand value.
            :param hand: 
            :return: 
            """
            if hand == bj.player1.hand:
                bj.player1.bankroll -= bj.bank.player1_bet
                bj.bank.player1_bet += bj.bank.player1_bet
            else:
                bj.player1.bankroll -= bj.bank.player1_bet2
                bj.bank.player1_bet2 += bj.bank.player1_bet2

            if hand == bj.player1.hand:
                bj.player1.hand.append(bj.deck.remove_card())
                bj.player1.final_hand_val = bj.player1.hand_value_check(bj.player1.hand)
            else:
                bj.player1.hand2.append(bj.deck.remove_card())
                bj.player1.final_hand2_val = bj.player1.hand_value_check(bj.player1.hand2)
            bj.player1.went_double = True

        def hit(hand=bj.player1.hand):
            """
            Simply deals additional card to current hand.
            :param hand: 
            :return: 
            """
            hand.append(bj.deck.remove_card())

        def stand(hand=bj.player1.hand):
            """
            Calculates current hand values, discards ones exceeding 21, then chooses largest of remaining values and
            assigns it to player final hand value
            :param hand: 
            :return: 
            """
            phv = bj.player1.hand_value_check(hand)  # check player hand value
            phv = [x for x in phv if x <= 21]
            if hand == bj.player1.hand:
                if len(phv) > 0:
                    bj.player1.final_hand_val = max(phv)
                else:
                    bj.player1.final_hand_val = "bust"
            else:
                if len(phv) > 0:
                    bj.player1.final_hand2_val = max(phv)
                else:
                    bj.player1.final_hand2_val = "bust"

        def check_for_bust_or_bj(hand=bj.player1.hand):
            """
            Calculates current hand's values, discards ones over 21. If no values remain -> assigns "bust" to final hand
            value. If "21" is among current hand's values -> assigns 21 as final hand value.
            :param hand: 
            :return: 
            """
            phv = bj.player1.hand_value_check(hand)  # check player hand value
            phv = [x for x in phv if x <= 21]  # remove all hand values that exceed 21
            if len(phv) == 0:  # if no values under 21 are available -> bust
                if hand == bj.player1.hand:
                    bj.player1.final_hand_val = "bust"
                    return
                else:
                    bj.player1.final_hand2_val = "bust"
                    return
            elif 21 in phv:  # if 21 is among values -> blackjack
                if hand == bj.player1.hand:
                    bj.player1.final_hand_val = 21
                    return
                else:
                    bj.player1.final_hand2_val = 21
                    return

        global p_choice
        p_choice = ask_user()

        if p_choice == "split":            # branch out hands if split was available and chosen by player
            bj.player1.hand2.append(bj.player1.hand.pop())    #create second hand for player1
            bj.player1.hand.append(bj.player1.hand.pop())
            bj.player1.bankroll -= bj.bank.player1_bet        #make a bet on a second hand
            bj.bank.player1_bet2 = bj.bank.player1_bet

            bj.table.stage = "split"
            bj.table.draw_table(0.33)

            split_aces = False
            bj.player1.went_split = True
            bj.player1.double_down = False            # turn off possible DD flag from initial draw, check for DD again
            if player_hand_val[0] / 2 == 11:          # check for split-Aces corner case (deal only 1 card to each ace,
                bj.player1.double_down = True         # if that card is 10, pay only 1x bet, not 1.5)
                split_aces = True
            elif player_hand_val[0] / 2 == 9 or player_hand_val[0] / 2 == 10:
                bj.player1.double_down = True

            if split_aces is True:                    #special case for splitting aces
                for i in range(0,2):                  #run once for each card
                    while True:
                        p_choice = input("Do you want to Double Down? yes\\no\n")
                        if p_choice != "yes" and p_choice != "no":
                            print("Wrong input.\n")
                            continue
                        else:
                            break

                    if p_choice == "yes" and i == 0:                 # when player chose to split aces and double down
                        double_down()
                        bj.table.draw_table(0.5)
                    elif p_choice == "yes" and i == 1:
                        double_down(bj.player1.hand2)                # <------- end PCP with final_hand_value(_\2) unchecked results
                        bj.table.draw_table(0.5)
                    elif i == 0:                                       # deal one card for first ace
                        hit()
                        bj.player1.final_hand_val = bj.player1.hand_value_check(bj.player1.hand)
                        bj.table.draw_table(0.5)
                    elif i == 1:                                     # and one for second ace
                        hit(bj.player1.hand2)
                        bj.player1.final_hand2_val = bj.player1.hand_value_check(bj.player1.hand2)      # <------- end PCP with final_hand_value(_\2) unchecked results
                        bj.table.draw_table(0.5)
            else:                                             # general case - 2 loops for each of 2 non-Ace split hands
                for i in range(0, 2):
                    p_choice = ask_user()

                    if i == 0 and p_choice == "dd" or p_choice == "double down" or p_choice == "double":
                        double_down()
                        bj.player1.went_double = False           # Turn down DD flag for possible DD on second hand
                        bj.table.draw_table(0.5)
                    elif i == 1 and p_choice == "dd" or p_choice == "double down" or p_choice == "double":
                        double_down(bj.player1.hand2)
                        bj.table.draw_table(0.5)        # <------- end PCP with final_hand_value(_\2) unchecked results
                    else:
                        ask_counter = 0
                        while True:
                            if ask_counter > 0:
                                p_choice = ask_user()

                            if i == 0 and p_choice == "hit":
                                hit()
                                check_for_bust_or_bj()
                                if bj.player1.final_hand_val == 21 or bj.player1.final_hand_val == "bust":
                                    bj.table.draw_table(0.5)
                                    break
                                else:
                                    ask_counter += 1
                                    bj.table.draw_table(0.5)
                                    continue
                            elif i == 0 and p_choice == "stand":
                                stand()
                                bj.table.draw_table(0.33)
                                break
                            elif i == 1 and p_choice == "hit":
                                hit(bj.player1.hand2)
                                check_for_bust_or_bj(bj.player1.hand2)
                                if bj.player1.final_hand2_val == 21 or bj.player1.final_hand2_val == "bust":
                                    bj.table.draw_table(0.5)
                                    break                             # <------- end PCP with final_hand_value(_\2) unchecked results
                                else:
                                    ask_counter += 1
                                    bj.table.draw_table(0.5)
                                    continue
                            elif i == 1 and p_choice == "stand":
                                stand(bj.player1.hand2)
                                bj.table.draw_table(0.33)
                                break                                     # <------- end PCP with final_hand_value(_\2) unchecked results

        elif p_choice == "dd" or p_choice == "double" or p_choice == "double down":
            double_down()                                         # <------- end PCP with final_hand_value(_\2) unchecked results
            bj.table.draw_table(0.5)
        else:
            counter = 0                                           # entering this branch with a valid p_choice
            while True:                                           # counter allows us to do it only starting from the second run of the loop
                if counter > 0:
                    bj.player1.split = False
                    bj.player1.double_down = False
                    p_choice = ask_user()
                if p_choice == "hit":
                    hit()
                    check_for_bust_or_bj()
                    counter += 1
                    if bj.player1.final_hand_val == 21 or bj.player1.final_hand_val == "bust":
                        bj.table.draw_table(1)
                        break                                     # <------- end PCP with final_hand_value(_\2) unchecked results
                    else:
                        bj.table.draw_table(0.8)
                        continue
                elif p_choice == "stand":
                    stand()
                    bj.table.draw_table(0.8)
                    break                                          # <------- end PCP with final_hand_value(_\2) unchecked results

        # normalize final hand values to single "int"s
        if bj.player1.final_hand_val == "bust" and bj.player1.final_hand2_val == "bust" and bj.player1.went_split is True:
            bj.dealer.bankroll += bj.bank.player1_bet
            bj.dealer.bankroll += bj.bank.player1_bet2
            return
        elif bj.player1.went_split is False and bj.player1.final_hand_val == "bust":
            bj.dealer.bankroll += bj.bank.player1_bet
            return
        else:
            if type(bj.player1.final_hand_val) == list:
                bj.player1.final_hand_val = max(bj.player1.final_hand_val)
            if type(bj.player1.final_hand2_val) == list:
                bj.player1.final_hand2_val = max(bj.player1.final_hand2_val)

        # DEALER PHASE

        bj.table.dealer_phase = True
        bj.table.draw_table()          # Dealer reveals face-down card

        while True:
            if dealer_hand_val[0] < 17:                       # If hand val is less than 17, dealer keeps drawing cards
                bj.dealer.hand.append(bj.deck.remove_card())
                dealer_hand_val = bj.dealer.hand_value_check(bj.dealer.hand)
                bj.table.draw_table(0.4)
                continue
            else:                                             # If hand val is 17 or more, dealer stops drawing
                if dealer_hand_val[0] > 21:
                    bj.dealer.final_hand_value = 0            # dealer goes bust
                    bj.table.draw_table(1)
                    break
                else:
                    bj.dealer.final_hand_value = dealer_hand_val[0]
                    bj.table.draw_table(1)
                    break

        # SHOWDOWN
        # Payment's for player's first hand
        if bj.player1.final_hand_val == "bust":
            bj.dealer.bankroll += bj.bank.player1_bet
        else:
            if bj.dealer.final_hand_value == bj.player1.final_hand_val:
                bj.player1.bankroll += bj.bank.player1_bet
            elif bj.dealer.final_hand_value > bj.player1.final_hand_val:
                bj.dealer.bankroll += bj.bank.player1_bet
            elif bj.dealer.final_hand_value < bj.player1.final_hand_val:
                bj.dealer.bankroll -= bj.bank.player1_bet
                bj.player1.bankroll += bj.bank.player1_bet * 2

        # Payments for player's second hand
        if bj.player1.final_hand2_val == "bust":
            bj.dealer.bankroll += bj.bank.player1_bet2
        else:
            if bj.dealer.final_hand_value == bj.player1.final_hand2_val:
                bj.player1.bankroll += bj.bank.player1_bet2
            elif bj.dealer.final_hand_value > bj.player1.final_hand2_val:
                bj.dealer.bankroll += bj.bank.player1_bet2
            elif bj.dealer.final_hand_value < bj.player1.final_hand2_val:
                bj.dealer.bankroll -= bj.bank.player1_bet2
                bj.player1.bankroll += bj.bank.player1_bet2 * 2
        bj.table.draw_table(0.33)


bj = Game()

while True:
    bj.play_game()
# while True:
#     answer = input("Play another hand? Y/N\n")
#     if answer != "Y" and answer != "y" and answer != "N" and answer != "n":
#         print("Wrong input, try again")
#     elif answer == "y" or "Y":
#         bj.play_game()
#         continue
#     else:
#         break

