import csv
import random


def main():
    deck = make_card_list()  # make a deck of cards
    player_1 = input('What is your name? ')
    computer = 'Computer'
    player_hand = draw_hand(player_1, deck)
    show_player_hand(player_1, player_hand)


def show_player_hand(player, hand):
    print(f'{player}, your cards are:')
    for cards in hand:
        print(' ' + cards)


def draw_hand(player, deck):
    hand = []
    for i in range(6):
        draw = draw_card(deck)
        hand.append(draw)
    return hand


def draw_card(card_list):  # function for drawing a card at random
    random.shuffle(card_list)  # start by shuffling the deck
    draw = card_list.pop(random_card(card_list))  # remove a card at random
    return draw  # return the card drawn from the deck


def random_card(card_list):  # function for picking a number to
    num = random.randint(0, len(card_list) - 1)  # pick an index number for the card generator
    return num  # return the number to the draw function


def make_card_list():
    full_list = []
    with open('deck_of_cards.csv') as f:
        cards = csv.DictReader(f)
        for line in cards:
            name = line['Name']
            full_list.append(name)
    return full_list


if __name__ == '__main__':
    main()
