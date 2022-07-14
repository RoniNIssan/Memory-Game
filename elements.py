import random


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
    def get_pile(self):
        if self.category == "animals":
            return self.animals

    def __str__(self):
        return self.get_pile()


class Pile:
    def __init__(self, category, level):
        self.category = category
        self.pile_size = 8
        if level == 2:
            self.pile_size = 14
        self.pile = CardsInCategroy(category).get_pile()

    def game_randomize_pile(self):
        game_randomize_pile = []
        random_list = random.sample(range(0, self.pile_size), int(self.pile_size / 2))
        for index in random_list:
            game_randomize_pile.append(self.pile[index - 1])
        return game_randomize_pile


class Board:
    def __init__(self, level, category):
        self.category = "animals"
        self.level = level
        self.pile = Pile(category, level).game_randomize_pile()
# TODO: change sturcture: pile consists of category, size and a list of cards.
