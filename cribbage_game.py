import csv
import random

WINNING = 121
PEG_MAX = 31


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
    show_community_card(community)
    pegging(player_1, player_hand, computer, computer_hand, crib_holder)  # function for the pegging portion of scoring


def show_community_card(community):
    print('---------------------------------')
    print(f'The community card is {community}')  # show the community card
    print('---------------------------------')


def determine_first_crib(player, computer):  # randomly determines who gets the first crib
    """
    :param player: Player's name
    :param computer: 'Computer'
    :return: whomever gets the first crib based on random number generation
    """
    crib = random.randint(1, 2)  # randomly choose 1 or 2
    if crib == 1:  # if the number is 1
        return player  # player gets the crib
    else:  # if number is 2
        return computer  # computer gets the crib


def pegging(player, player_hand, computer, computer_hand, crib_holder):  # pegging function
    """
    :param player: Player's name
    :param player_hand: List containing the cards in the player's hand
    :param computer: 'Computer'
    :param computer_hand: List containing the cards in the computer's hand
    :param crib_holder: Who has the crib (player or computer)
    :return: none

    TODO: This needs some serious cleaning. Woof
    """
    peg_count = 0  # start with pegging score of 0
    player_peg = player_hand.copy()  # make a copy of the player's hand so we can remove things from it
    computer_peg = computer_hand.copy()  # make copy of the computer's hand
    turn = get_next_turn(player, False, computer, False, crib_holder)  # player w/o crib goes first
    while len(player_peg) > 0 or len(computer_peg) > 0:  # as long as there are cards in someone's hand
        player_go = False  # flag for whether the player has said 'go'
        computer_go = False  # flag for whether the computer has said 'go'
        while not player_go or not computer_go:  # continue as long as at least one player hasn't said 'go'
            peg_return = play_card(player, player_peg, computer, computer_peg, turn, peg_count)  # return int or 'go'
            if type(peg_return) == str:  # checks for 'go' returned by player
                print(f'{turn} says "Go"')  # announces 'go'
                if turn == player:  # if the player returns go
                    player_go = True  # mark go flag for player
                else:  # if the computer says go
                    computer_go = True  # mark go flag for computer
            else:
                peg_count += peg_return  # if a card was returned, adds value to peg count
            if peg_count == PEG_MAX:  # if the pegging count reaches 31
                print(f'{turn} gets 31 for two points.')  # award two points to the player who hit 31
                peg_count = 0  # reset the pegging count
            show_peg_count(peg_count)
            turn = get_next_turn(player, player_go, computer, computer_go, turn)  # switch players
            if len(player_peg) == 0:  # if the player is out of cards
                player_go = True  # automatically say 'go'
            if len(computer_peg) == 0:  # if the computer is out of cards
                computer_go = True  # automatically say 'go'
        peg_count = 0  # reset pegging count if both players say go


def show_peg_count(peg_count):
    print('--------------------------')
    print(f'    Pegging count: {peg_count}')  # print the current peg count
    print('--------------------------')


def play_card(player, player_hand, computer, computer_hand, turn, peg):  # playing cards in pegging sequence
    """
    This is the sequence for playing a card. Different sections for Player vs. AI
    :param player: Name of player
    :param player_hand: list of cards in player's hand
    :param computer: 'Computer'
    :param computer_hand: list of cards in computer's hand
    :param turn: whose turn is it?
    :param peg: current pegging score
    :return: value of card played, or string 'go'

    TODO: validation for player card. Clean it up a bit.
    """
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
    else:
        # open spreadsheet, cycle through hand, if card can be played, play it. If no cards can be played, say go
        with open('deck_of_cards.csv') as f:  # opens the csv file
            deck = csv.DictReader(f)  # stack of cards from csv is called deck
            for card in computer_hand:  # look through each card in the hand
                for cards in deck:  # look at deck spreadsheet
                    name = cards['Name']
                    value = cards['Value']
                    if card == name:  # find the card in the name column of the spreadsheet
                        if int(value) + peg <= PEG_MAX:  # if the value of the card can be added to peg count
                            play_name = computer_hand.pop(computer_hand.index(card))  # remove card from hand
                            value = get_card_value(computer, play_name)  # play the card
                            return int(value)  # return the value
            return 'Go'  # if no cards can be played, say 'go'


def is_int(val):
    """
    Determines whether a given value is an int
    :param val: value in question
    :return: True if int, False if other
    """
    try:
        int(val)  # tries to make the returned value into an integer
    except ValueError:  # if it returns an error, it can only be a string
        return False  # return false
    return True  # if it does not return an error, it must be an integer


def get_card_value(player, card):
    """
    Reads the name of the card from a list, gets back the value of the card
    :param player: Name of player
    :param card: Name of card
    :return: value of card
    """
    with open('deck_of_cards.csv') as f:  # opens the csv file
        deck = csv.DictReader(f)  # reads the csv file as dictionary
        for cards in deck:  # for each line of the csv
            name = cards['Name']  # assign name to the key for each item in the 'Name' column
            value = cards['Value']  # assign value to the key for each item in the 'Value' column
            if name == card:  # looks up the name of the card drawn, returns the associated value
                print(f'{player} played {name} for {value} points')  # displays the player, card, and value
                return value  # returns value of card


def get_next_turn(player, p_go, computer, c_go, turn):
    """
    function for switching turns
    :param player: Name of player
    :param p_go: Whether the player has said 'go' Default is False
    :param computer: 'Computer'
    :param c_go: Whether the computer has said 'go' Default is false
    :param turn: whose turn is it?
    :return: next player
    """
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
    """
    Function for discarding cards to the crib
    :param player_hand: list of cards in the player's hand
    :param computer_hand: list of cards in the computer's hand
    :param crib: empty crib list
    :return: crib list appended in function
    """
    discard_to_crib(player_hand, crib, False)  # ask player to discard two cards to the crib
    discard_to_crib(computer_hand, crib, True)  # discards two random cards for the computer


def discard_to_crib(hand, crib, ai):
    """
    takes in hand and crib for player/ai to discard 2 cards from hand to crib
    :param hand: list of cards in hand of player or computer
    :param crib: crib list (starts empty)
    :param ai: Is the player a player or computer? False = Player, True = AI
    :return: crib list appended in function
    """
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
    """
    Generally used for testing and debugging. Enumerated lists used for actual gameplay
    :param player: whose hand is it?
    :param hand: list of cards in the hand
    :return: cards are printed
    """
    print(f'{player}, your cards are:')  
    for cards in hand:  # loop through cards in player's hand
        print('    ' + cards)  # print a space to indent and the name of the card


def draw_hand(deck):
    """
    takes the full deck of cards will return a list of 6 random cards
    :param deck: List of all cards in the deck
    :return: list of 6 cards for the player/computer's hand
    """
    hand = []  # start with a blank list for the hand
    for i in range(6):  # loops 6 times to draw 6 cards in total
        draw = draw_card(deck)  # draws a random card. See draw_card function for details
        hand.append(draw)  # puts drawn card in hand
    return hand  # returns the hand list to main function


def draw_card(card_list):
    """
    function for drawing a card at random
    :param card_list: list of cards from which to draw. Usually full deck
    :return: single card popped from the list
    """
    random.shuffle(card_list)  # start by shuffling the deck
    draw = card_list.pop(random_card(card_list))  # remove a card at random
    return draw  # return the card drawn from the deck


def random_card(card_list):
    """
    pick a random card from within a given list
    :param card_list: List from which a card will be drawn
    :return: index of card to be drawn
    """
    num = random.randint(0, len(card_list) - 1)  # pick an index number for the card generator
    return num  # return the number to the draw function


def make_card_list():
    """
    creates a list of all cards from the csv file
    :return: list of all cards in a deck
    """
    full_list = []  # start with an empty list
    with open('deck_of_cards.csv') as f:  # opens the csv file
        deck = csv.DictReader(f)  # reads the csv file as dictionary
        for cards in deck:  # for each line of the csv
            name = cards['Name']  # assign name to the key for each item in the 'Name' column
            full_list.append(name)  # add the names of each card to the list
    return full_list  # return the full list of cards to the main function


if __name__ == '__main__':
    main()
