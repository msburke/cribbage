import csv
import random

WINNING = 121


def main():
    deck = make_card_list()  # make a deck of cards
    crib = []
    player_1 = 'Matt'  # input('What is your name? ')  # asks for a player's name to use during the game.
    computer = 'Computer'  # sets the computer's name to Computer
    player_hand = draw_hand(deck)  # draws cards for the player's hand
    computer_hand = draw_hand(deck)  # draws cards for the computer's hand
    # show_player_hand(player_1, player_hand)  # shows the player's hand
    build_crib(player_hand, computer_hand, crib)  # clean up the crib building function. Both "players" in one
    community = draw_card(deck)  # draw the community card
    show_player_hand(player_1, player_hand)  # show the player hand
    print('The community card is', community)  # show the community card
    # show_player_hand(computer, computer_hand)
    # show_player_hand('Crib', crib)


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
