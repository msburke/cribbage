import csv
import random

WINNING = 121


def main():
    deck = make_card_list()  # make a deck of cards
    player_1 = input('What is your name? ')  # asks for a player's name to use during the game.
    computer = 'Computer'  # sets the computer's name to Computer
    player_hand = draw_hand(deck)  # draws cards for the player's hand
    show_player_hand(player_1, player_hand)  # shows the player's hand


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
