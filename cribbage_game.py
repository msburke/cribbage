import csv
import random

WINNING = 121
PEG_MAX = 31


def main():
    player_score = []  # empty list to serve as a place where we can store all points awarded to player
    computer_score = []  # empty list to serve as a place where we can store all points awarded to the computer
    crib = []  # make an empty crib list
    player = 'Matt'  # input('What is your name? ')  # asks for a player's name to use during the game.
    computer = 'Computer'  # sets the computer's name to Computer
    crib_holder = determine_first_crib(player, computer)  # randomly determine first crib
    while True:
        deck = make_card_list()  # make a deck of cards
        player_hand = draw_hand(deck)  # draws cards for the player's hand
        computer_hand = draw_hand(deck)  # draws cards for the computer's hand
        show_scores(player, player_score, computer_score)
        build_crib(player_hand, computer_hand, crib, crib_holder)  # discard from hand to crib
        community = draw_card(deck)  # draw the community card
        show_community_card(community)  # shows the community card
        pegging(player, player_hand, player_score, computer, computer_hand, computer_score, crib_holder)  # pegging
        count_hands(player, player_score, player_hand, computer, computer_score, computer_hand, community, crib_holder, crib)
        crib_holder = get_next_turn(player, False, computer, False, crib_holder)  # swap crib holder for the next turn


def count_hands(player, player_score, player_hand, computer, computer_score, computer_hand, community, crib_holder, crib):
    """
    Count all of the possible points in the player and computer hands
    :param computer: 'Computer'
    :param player: name of the player
    :param player_score: list of player points
    :param player_hand: list of cards in the player's hand
    :param computer_score: list of computer points
    :param computer_hand: list of cards in the computer's hand
    :param community: name of the community card
    :param crib_holder: name of the who has the crib this round
    :param crib: list of cards in the crib
    :return:
    """


def add_scores(points, player, player_score, computer_score, turn):
    """
    add the awarded points to the appropriate player
    :param points: number of points to be awarded
    :param player: name of the player
    :param player_score: player's score list
    :param computer_score: computer's score list
    :param turn: whose turn is it?
    :return: no return, values are appended to score lists
    """
    if turn == player:  # if it is the player's turn
        player_score.append(points)  # give the points to the player
    else:  # if it's the computer's turn
        computer_score.append(points)  # give the points to the computer


def check_peg_points(peg_list, peg_score, player, player_score, computer_score, turn):
    """
    checks all the ways to score points while pegging
    :param peg_list: list of cards that have been played in the pegging round
    :param peg_score: current peg score
    :param player: name of player
    :param player_score: player's score list
    :param computer_score: computer's score list
    :param turn: whose turn is it?
    :return: no return, points will be appended
    """
    check_fifteen(peg_score, player, player_score, computer_score, turn)
    check_thirty_one(peg_score, player, player_score, computer_score, turn)
    check_groups(peg_list, player, player_score, computer_score, turn)
    check_run(peg_list, player, player_score, computer_score, turn)


def check_run(peg_list, player, player_score, computer_score, turn):
    """
    Check for possible runs
    :param peg_list: list of cards played
    :param player: name of player
    :param player_score: list of player points
    :param computer_score: list of computer points
    :param turn: whose turn is it?
    :return: points are announced and appended
    """
    if len(peg_list) >= 3:  # as long as the list is three or longer
        for i in range(len(peg_list), 2, -1):  # try runs in decreasing value
            if run_of_n(peg_list, player, player_score, computer_score, turn, i):  # if a run is successful..
                break  # break out of the loop


def run_of_n(peg_list, player, player_score, computer_score, turn, n):
    """

    :param peg_list: list of cards that have been played
    :param player: name of player
    :param player_score: list of player points
    :param computer_score: list of computer points
    :param turn: whose turn is it?
    :param n: length of run to test for
    :return: True if points are awarded, then points are announced and appended. False if not
    """
    n = int(n)
    last_n = []  # list of the last n cards played
    card_order = []  # order number of the last three cards played
    for i in range(-1, -(n + 1), -1):  # get the last n cards played
        last_n.append(peg_list[i])  # put them in the list above
    for cards in last_n:  # look at the cards in the last n list
        order = int(get_card_order(cards))  # get the order of the cards
        card_order.append(order)  # put them in the list
    if check_consecutive(card_order):  # check to see if the cards are consecutive, award appropriate number of points
        if turn == player:
            print(f'{player} played a run of {n} for {n} points.')
            player_score.append(n)
            return True
        else:
            print(f'Computer played a run of {n} for {n} points.')
            computer_score.append(n)
            return True
    else:
        return False


def check_consecutive(cards):
    """
    Function to see if the cards played are consecutive in order to determine runs
    :param cards: list of the order of the cards, should be a list of integers
    :return: True if the cards can be arranged consecutively, False if they can't
    """
    sorted_list = sorted(cards)
    range_list = list(range(min(cards), max(cards)+1))
    if sorted_list == range_list:
        return True
    else:
        return False


def check_groups(peg_list, player, player_score, computer_score, turn):
    """
    Checks to see if there are there are possible pairs, three of a kind, or four of a kind
    :param peg_list: list of cards that have been played during pegging round
    :param player: name of player
    :param player_score: list of player's points
    :param computer_score: list of computer's points
    :param turn: whose turn is it?
    :return: points are appended during play
    """
    if len(peg_list) >= 4:  # if there are 4 or more cards in the hand, check for four of a kind first
        four_of_a_kind(peg_list, player, player_score, computer_score, turn)
    elif len(peg_list) == 3:  # if there are three cards in the hand, check for three of a kind first
        three_of_a_kind(peg_list, player, player_score, computer_score, turn)
    elif len(peg_list) == 2:  # if there are two cards in the hand, check for a pair first
        two_of_a_kind(peg_list, player, player_score, computer_score, turn)


def two_of_a_kind(peg_list, player, player_score, computer_score, turn):
    """
    Checks if the two most recently played cards are the same number or face
    :param peg_list: list of cards played during pegging round
    :param player: name of player
    :param player_score: list of player points
    :param computer_score: list of computer points
    :param turn: whose turn is it
    :return: points are appended during play
    """
    second = get_card_order(peg_list[-1])  # gets the "order" of the last card played. Same cards have same order
    first = get_card_order(peg_list[-2])  # gets "order" of the second to last card played
    if second == first:  # if the two cards are the same order, player/computer gets two points
        print(f'{turn} played a pair for 2 points.')
        if turn == player:
            player_score.append(2)
        else:
            computer_score.append(2)


def three_of_a_kind(peg_list, player, player_score, computer_score, turn):
    """
    Checks if the three most recently played cards are a three of a kind. If not, it'll try for a pair
    :param peg_list: list of previously played cards
    :param player: name of player
    :param player_score: list of player points
    :param computer_score: list of computer points
    :param turn: whose turn is it?
    :return: points will be displayed and appended
    """
    third = get_card_order(peg_list[-1])
    second = get_card_order(peg_list[-2])  # these three variables get the 'order' of three most recently played cards
    first = get_card_order(peg_list[-3])
    if third == second == first:  # if all three cards are the same, award 6 points
        print(f'{turn} played three of a kind for 6 points.')
        if turn == player:
            player_score.append(6)
        else:
            computer_score.append(6)
    elif third == second:  # if only the most recently played are the same, go to the two of a kind (pair) function
        two_of_a_kind(peg_list, player, player_score, computer_score, turn)


def four_of_a_kind(peg_list, player, player_score, computer_score, turn):
    """
    Test for four of a kind. If not applicable, tries for three, then pair
    :param peg_list: list of cards played
    :param player: name of player
    :param player_score: list of player points
    :param computer_score: list of computer points
    :param turn: whose turn is it
    :return: points will be displayed and appended
    """
    fourth = get_card_order(peg_list[-1])
    third = get_card_order(peg_list[-2])  # these functions will get the order
    second = get_card_order(peg_list[-3])  # of the four most recent cards
    first = get_card_order(peg_list[-4])
    if fourth == third == second == first:  # if all 4 are the same, reward 12 points
        print(f'{turn} played four of a kind for 12 points.')
        if turn == player:
            player_score.append(12)
        else:
            computer_score.append(12)
    elif fourth == third == second:  # if only last three are the same, go to three of a kind function
        three_of_a_kind(peg_list, player, player_score, computer_score, turn)
    elif fourth == third:  # if only last two are the same, go to pair function
        two_of_a_kind(peg_list, player, player_score, computer_score, turn)


def check_fifteen(peg_score, player, player_score, computer_score, turn):
    """
    Checks to see if the player/computer got 15 points on pegging
    :param peg_score: current peg score
    :param player: name of player
    :param player_score: list of player's points
    :param computer_score: list of computer's points
    :param turn: whose turn is it?
    :return: no return, values are appended
    """
    if peg_score == 15:  # checks to see if peg score is 15
        print(f'{turn} scores 2 points for 15.')  # announces the player who got 15
        if turn == player:  # if it was the player's turn
            player_score.append(2)  # give the player 2 points
        else:  # if it was the computer's turn
            computer_score.append(2)  # give the computer 2 points


def check_thirty_one(peg_score, player, player_score, computer_score, turn):
    """
    Checks to see if the player/computer got 31 points on pegging
    :param peg_score: current peg score
    :param player: name of player
    :param player_score: list of player's points
    :param computer_score: list of computer's points
    :param turn: whose turn is it?
    :return: no return, values are appended
    """
    if peg_score == 31:  # checks to see if peg score is 31
        print(f'{turn} scores 2 points for 31.')  # announces player who got 31
        if turn == player:  # if it was the player's turn
            player_score.append(2)  # award player 2 points
        else:  # if it was the computer's turn
            computer_score.append(2)  # give the computer two points


def show_scores(player, player_list, computer_list):
    """
    Hack way of keeping track of scores since lists are mutable. The lists keep track of all points awarded, then this
    function will tabulate them for display
    :param player: name of the player
    :param player_list: list of all points awarded to the player
    :param computer_list: list of all points awarded to the computer
    :return: no return, but the function will display scores and quit the game when someone wins
    """
    player_score = int(score_from_list(player_list))  # call function to get score for player
    computer_score = int(score_from_list(computer_list))  # call function to get score for computer
    print(f"{player}'s score: {player_score}.")  # display the player's name and score
    print(f"Computer's score: {computer_score}.")  # display the computer's score
    check_for_win(player, player_score, computer_score)  # check of there's a winner


def check_for_win(player, player_score, computer_score):
    """
    Compares player and computer scores to the value needed to win (Default: 121). Ends game if there's a winner
    :param player: name of the player
    :param player_score: player's score (int)
    :param computer_score: computer's score (int)
    :return: return None of there are no winners. Ends game if there is.
    """
    if player_score >= WINNING:  # compare player's score to winning score
        print(f'Game over! {player} wins!')  # if the player has won, declare winner!
        quit()  # quit the game
    elif computer_score >= WINNING:  # compare computer's score to winning score
        print('Game over, Computer wins!')  # if the player has won, declare winner!
        quit()  # quit the game
    else:  # if nobody has won
        return None  # return nothing


def score_from_list(lst):
    """
    Takes in the list values and returns an integer score
    :param lst: List of points awarded to player/computer
    :return: calculated score
    """
    score = 0  # start with a score of zero
    for points in lst:  # go through every item in the list
        score += points  # add the item to the score
    return score  # return the score


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


def pegging(player, player_hand, player_score, computer, computer_hand, computer_score, crib_holder):
    """
    This is the pegging function. Players will alternate playing cards up to 31 points until both players run out
    of cards. Point values shown in score functions.
    :param player: Player's name
    :param player_score: list of points awarded to the player
    :param player_hand: List containing the cards in the player's hand
    :param computer: 'Computer'
    :param computer_hand: List containing the cards in the computer's hand
    :param computer_score: list of points awarded to the computer
    :param crib_holder: Who has the crib (player or computer)
    :return: none
    TODO: This needs some serious cleaning. Woof
    """
    player_peg = player_hand.copy()  # make a copy of the player's hand so we can remove things from it
    computer_peg = computer_hand.copy()  # make copy of the computer's hand
    turn = get_next_turn(player, False, computer, False, crib_holder)  # player w/o crib goes first
    while len(player_peg) > 0 or len(computer_peg) > 0:  # as long as there are cards in someone's hand
        peg_count = 0  # start with pegging score of 0
        peg_list = []  # list of cards that have been played. Used for determining pairs, runs, etc.
        player_go = False  # flag for whether the player has said 'go'
        computer_go = False  # flag for whether the computer has said 'go'
        while not player_go or not computer_go:  # continue as long as at least one player hasn't said 'go'
            peg_return = play_card(player, player_peg, computer, computer_peg, turn, peg_list, peg_count)  # int or 'go'
            if type(peg_return) == str:  # checks for 'go' returned by player
                print(f'{turn} says "Go"')  # announces 'go'
                if turn == player:  # if the player returns go
                    player_go = True  # mark go flag for player
                else:  # if the computer says go
                    computer_go = True  # mark go flag for computer
            else:
                peg_count += peg_return  # if a card was returned, adds value to peg count
                check_peg_points(peg_list, peg_count, player, player_score, computer_score, turn)
            if peg_count == PEG_MAX:  # if the pegging count reaches 31
                peg_count = 0  # reset the pegging count
                peg_list = []  # clears the peg list for the next round
                player_go = False  # reset player go to False
                computer_go = False  # reset computer go to False
            show_peg_count(peg_count)
            show_scores(player, player_score, computer_score)
            show_pile(peg_list)
            turn = get_next_turn(player, player_go, computer, computer_go, turn)  # switch players
            if len(player_peg) == 0:  # if the player is out of cards
                player_go = True  # automatically say 'go'
            if len(computer_peg) == 0:  # if the computer is out of cards
                computer_go = True  # automatically say 'go'


def show_pile(pile):
    """
    Used to show the cards that have been played in pegging so the player doesn't have to look back
    :param pile: Takes in the cards from the pile
    :return: no return, but will print on screen
    """
    print()  # print a blank line to keep things clean
    print('Cards in play:', end=' ')  # prints the line 'Cards in play:' and takes out the line break
    for cards in pile:
        print(cards, end='. ')  # prints all the cards on the same line separated by periods
    print()  # return at the end of the list
    print()  # extra line to keep it clean


def show_peg_count(peg_count):
    print('--------------------------')
    print(f'    Pegging count: {peg_count}')  # print the current peg count
    print('--------------------------')


def play_card(player, player_hand, computer, computer_hand, turn, peg_list, peg):  # playing cards in pegging sequence
    """
    This is the sequence for playing a card. Different sections for Player vs. AI
    :param player: Name of player
    :param player_hand: list of cards in player's hand
    :param computer: 'Computer'
    :param computer_hand: list of cards in computer's hand
    :param turn: whose turn is it?
    :param peg_list: list of cards played in the current round of pegging.
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
            peg_list.append(play_name)  # add the card to the pegging list
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
                            peg_list.append(play_name)  # adds the card to the list of cards played
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
                print(f'{player} played {name} for {value}')  # displays the player, card, and value
                return value  # returns value of card


def get_card_order(card):
    """
    Looks up the name of the card on the csv and returns the order of the card
    :param card: name of car
    :return: order of the card
    """
    with open('deck_of_cards.csv') as f:
        deck = csv.DictReader(f)
        for cards in deck:
            name = cards['Name']
            order = cards['Order']
            if name == card:
                return order


def get_card_suit(card):
    """
    Looks up the name of the card and returns its suit
    :param card: name of the card
    :return: name of the suit
    """
    with open('deck_of_cards.csv') as f:
        deck = csv.DictReader(f)
        for cards in deck:
            name = cards['Name']
            suit = cards['Suit']
            if name == card:
                return suit


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


def build_crib(player_hand, computer_hand, crib, crib_holder):
    """
    Function for discarding cards to the crib
    :param crib_holder: name of player who gets the crib
    :param player_hand: list of cards in the player's hand
    :param computer_hand: list of cards in the computer's hand
    :param crib: empty crib list
    :return: crib list appended in function
    """
    discard_to_crib(player_hand, crib, False, crib_holder)  # ask player to discard two cards to the crib
    discard_to_crib(computer_hand, crib, True, crib_holder)  # discards two random cards for the computer


def discard_to_crib(hand, crib, ai, crib_holder):
    """
    takes in hand and crib for player/ai to discard 2 cards from hand to crib
    :param crib_holder: name of player who gets the crib
    :param hand: list of cards in hand of player or computer
    :param crib: crib list (starts empty)
    :param ai: Is the player a player or computer? False = Player, True = AI
    :return: crib list appended in function
    """
    if not ai:  # loop for if the player is human
        for i in range(2):  # player will discard two cards
            for num, card in enumerate(hand, start=1):  # numbers all of the cards
                print(f'{num}. {card}')  # displays the numbers and the corresponding cards
            discard = int(input(f"Select a card to place in {crib_holder}'s crib: "))  # prompts for discard
            while discard > len(hand) or discard < 1:
                discard = int(input('Choose a valid card: '))
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
