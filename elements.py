import random
import pygame


class Card:
    def __init__(self, title):
        self.title = title
        self.is_face_up = False

    def __str__(self):
        return self.title


class CardsInCategroy:
    def __init__(self, category):
        self.category = category

        self.animals = [Card("monkey"),
                        Card("bear"),
                        Card("crocodile"),
                        Card("fox"),
                        Card("lion"),
                        Card("shark"),
                        Card("snake"),
                        Card("butterfly"),
                        Card("whale"),
                        Card("cat"),
                        Card("dog"),
                        Card("bee"),
                        Card("spider"),
                        Card("elephant")]
    #         TODO: add more categories
        self.empty = []

    def get_pile(self):
        if self.category == "animals":
            return self.animals
        if self.category == "empty":
            return self.empty

    def __str__(self):
        return self.get_pile()


class Pile:
    def __init__(self, category, pile_size):
        self.category = category
        self.pile_size = pile_size

        self.pile = CardsInCategroy(category).get_pile()
        self.rand_pile = CardsInCategroy("empty").get_pile()

        game_randomize_pile = []
        random_list = random.sample(range(0, self.pile_size), int(self.pile_size / 2))
        for index in random_list:
            game_randomize_pile.append(self.pile[index - 1])
        self.rand_pile = game_randomize_pile

class Level:
    def __init__(self, level):
        self.level = level
        self.LEVEL_LOCATIONS = {}
        self.pile_size = 8
        self.CARD_WIDTH = 117
        self.CARD_HEIGHT = 167

        if self.level == 1:
            self.CARD_WIDTH = 117
            self.CARD_HEIGHT = 167
            self.LEVEL_LOCATIONS = {1: pygame.Rect(64, 76, self.CARD_WIDTH, self.CARD_HEIGHT),
                                    2: pygame.Rect(235, 76, self.CARD_WIDTH, self.CARD_HEIGHT),
                                    3: pygame.Rect(441, 76, self.CARD_WIDTH, self.CARD_HEIGHT),
                                    4: pygame.Rect(629, 76, self.CARD_WIDTH, self.CARD_HEIGHT),
                                    5: pygame.Rect(64, 264, self.CARD_WIDTH, self.CARD_HEIGHT),
                                    6: pygame.Rect(235, 264, self.CARD_WIDTH, self.CARD_HEIGHT),
                                    7: pygame.Rect(441, 264, self.CARD_WIDTH, self.CARD_HEIGHT),
                                    8: pygame.Rect(629, 264, self.CARD_WIDTH, self.CARD_HEIGHT)}
        if self.level == 2:
            self.pile_size = 14
            self.CARD_WIDTH = 96
            self.CARD_HEIGHT = 136
            pass
#         TODO: add params


class Board:
    def __init__(self, level, category):
        self.category = "animals"
        self.level = Level(level)
        self.pile = Pile(category, self.level.pile_size).rand_pile
        self.cards_in_rand_location = self.build_board()

    def build_board(self):
        random.shuffle(self.pile) # suffle all cards

        cards_randomized_location_list = [card for card in self.pile] # build a base shuffled card pile
        random.shuffle(self.pile) # shuffle pile again to change location
        for card in self.pile:
            cards_randomized_location_list.append(card)
        return cards_randomized_location_list


# TODO: change sturcture: pile consists of category, size and a list of cards.
