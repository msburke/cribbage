import csv
import random

WINNING = 121


def main():
    deck = make_card_list()  # make a deck of cards
    crib = []  # make an empty crib list
    player_1 = 'Matt'  # input('What is your name? ')  # asks for a player's name to use during the game.
    computer = 'Computer'  # sets the computer's name to Computer
    player_hand = draw_hand(deck)  # draws cards for the player's hand
    computer_hand = draw_hand(deck)  # draws cards for the computer's hand
    crib_holder = determine_first_crib(player_1, computer)  # randomly determine first crib
    build_crib(player_hand, computer_hand, crib)  # clean up the crib building function. Both "players" in one
    community = draw_card(deck)  # draw the community card
    print('---------------------------------')
    print(f'The community card is {community}')  # show the community card
    print('---------------------------------')
    pegging(player_1, player_hand, computer, computer_hand, crib_holder)  # function for the pegging portion of scoring


def determine_first_crib(player, computer):  # randomly determines who gets the first crib
    crib = random.randint(1, 2)  # randomly choose 1 or 2
    if crib == 1:  # if the number is 1
        return player  # player gets the crib
    else:  # if number is 2
        return computer  # computer gets the crib


def pegging(player, player_hand, computer, computer_hand, crib_holder):  # pegging function
    peg_count = 0  # start with pegging score of 0
    player_peg = player_hand.copy()  # make a copy of the player's hand so we can remove things from it
    computer_peg = computer_hand.copy()  # make copy of the computer's hand
    turn = get_next_turn(player, False, computer, False, crib_holder)  # player w/o crib goes first
    while len(player_peg) > 0 or len(computer_peg) > 0:  # as long as there are cards in someone's hand
        while peg_count < 31:
            """
            Somewhere in this loop I need a way to keep track of 'go' values
            Brainstorm:
            player_go = False (set to true if the player returns go)
            computer_go = False (set to true if the computer returns go)
            While both are False, loop keeps going. If both are true, loop resets
            If player or computer flagged True, their turns are skipped until both True
            """
            player_go = False
            computer_go = False
            while not player_go or not computer_go:
                peg_return = play_card(player, player_peg, computer, computer_peg, turn)  # return int or 'go'
                if type(peg_return) == str:  # checks for 'go' returned by player
                    print(f'{turn} says "Go"')  # announces 'go'
                    if turn == player:
                        player_go = True
                    else:
                        computer_go = True
                else:
                    peg_count += peg_return  # if a card was returned, adds value to peg count
                print('--------------------------')
                print(f'Pegging count: {peg_count}')  # print the current peg count
                print('--------------------------')
                turn = get_next_turn(player, player_go, computer, computer_go, turn)  # switch players
        peg_count = 0  # reset pegging count after reaching 31


def play_card(player, player_hand, computer, computer_hand, turn):  # playing cards in pegging sequence
    if turn == player:  # if it's the player's turn
        for num, card in enumerate(player_hand, start=1):  # show numbered list of cards
            print(f'{num}. {card}')
        print()
        play = input(f'{player}, choose a card to play: ')  # ask for card to play
        if is_int(play):  # checks if the player input a value that can be an integer
            play_name = player_hand.pop(int(play) - 1)  # remove card from hand, store name
            value = get_card_value(player, play_name)  # function for getting the value of a card
            return int(value)  # return the integer value of the card
        else:  # if the player inputs a string
            return 'Go'  # returns 'go'
    else:  # TODO make this smarter, as well
        play = random.randint(0, len(computer_hand) - 1)  # randomly draws a card to play from computer's hand
        play_name = computer_hand.pop(play)  # remove card from hand, store name
        value = get_card_value(computer, play_name)  # function for getting the value of a card
        return int(value)


def is_int(val):
    try:
        int(val)
    except ValueError:
        return False
    return True


def get_card_value(player, card):
    with open('deck_of_cards.csv') as f:  # opens the csv file
        cards = csv.DictReader(f)  # reads the csv file as dictionary
        for line in cards:  # for each line of the csv
            name = line['Name']  # assign name to the key for each item in the 'Name' column
            value = line['Value']  # assign value to the key for each item in the 'Value' column
            if name == card:  # looks up the name of the card drawn, returns the associated value
                print(f'{player} played {name} for {value} points')  # displays the player, card, and value
                return value  # returns value to the pegging function


def get_next_turn(player, p_go, computer, c_go, turn):  # function for switching turns
    if p_go and c_go:  # if both player and computer say 'go' this will continue as normal
        if player == turn:  # if it's currently the player's turn
            return computer  # make it the computer's turn
        else:  # otherwise
            return player  # make it the player's turn
    if p_go:  # if the player has said go, return computer regardless
        return computer
    if c_go:  # if the computer has said go, return the player regardless
        return player
    if player == turn:  # if it's currently the player's turn
        return computer  # make it the computer's turn
    else:  # otherwise
        return player  # make it the player's turn


def build_crib(player_hand, computer_hand, crib):
    discard_to_crib(player_hand, crib, False)  # ask player to discard two cards to the crib
    discard_to_crib(computer_hand, crib, True)  # discards two random cards for the computer


def discard_to_crib(hand, crib, ai):  # takes in hand and crib for player/ai to discard 2 cards from hand to crib
    #  TODO make this ai smarter?
    if not ai:  # loop for if the player is human
        for i in range(2):  # player will discard two cards
            for num, card in enumerate(hand, start=1):  # numbers all of the cards
                print(f'{num}. {card}')  # displays the numbers and the corresponding cards
            discard = int(input('Select a card to place in the crib: '))  # prompts for discard
            crib.append(hand.pop(discard-1))  # removes the card from the player's hand and puts it in the crib
    else:  # for if player is computer (AI)
        for i in range(2):  # to discard two cards
            discard = random.randint(1, len(hand))  # pick a number between 1 and the length of the hand list
            crib.append(hand.pop(discard - 1))  # removes the card from the corresponding index and puts it in the crib


def show_player_hand(player, hand):  # takes the name of the player and the list of the cards in their hand
    print(f'{player}, your cards are:')  
    for cards in hand:  # loop through cards in player's hand
        print(' ' + cards)  # print a space to indent and the name of the card


def draw_hand(deck):  # takes the full deck of cards will return a list of 6 random cards
    hand = []  # start with a blank list for the hand
    for i in range(6):  # loops 6 times to draw 6 cards in total
        draw = draw_card(deck)  # draws a random card. See draw_card function for details
        hand.append(draw)  # puts drawn card in hand
    return hand  # returns the hand list to main function


def draw_card(card_list):  # function for drawing a card at random
    random.shuffle(card_list)  # start by shuffling the deck
    draw = card_list.pop(random_card(card_list))  # remove a card at random
    return draw  # return the card drawn from the deck


def random_card(card_list):  # function for picking a number to
    num = random.randint(0, len(card_list) - 1)  # pick an index number for the card generator
    return num  # return the number to the draw function


def make_card_list():  # creates a list of all cards from the csv file
    full_list = []  # start with an empty list
    with open('deck_of_cards.csv') as f:  # opens the csv file
        cards = csv.DictReader(f)  # reads the csv file as dictionary
        for line in cards:  # for each line of the csv
            name = line['Name']  # assign name to the key for each item in the 'Name' column
            full_list.append(name)  # add the names of each card to the list
    return full_list  # return the full list of cards to the main function


if __name__ == '__main__':
    main()
