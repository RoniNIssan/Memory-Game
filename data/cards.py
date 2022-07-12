import random

class Card:
    def __int__(self, title):
        # self.category = category
        self.title = title
        self.is_face_up = False


class Pile_Category():
    def __int__(self):
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

    def get_pile(self, category):
        if category == "animals":
            return self.animals


class Pile():
    def __int__(self, category, size):
        self.size = size
        self.category = category
        self.pile = Pile_Category().get_pile(category)

    def game_randomize_pile(self):
        game_rand_list = []
        random_list = random.sample(range(self.size), self.size / 2)
        for index in random_list:
            game_rand_list.append(self.pile[index - 1])

        return game_rand_list


class Board():
    def __init__(self, level, category):
        self.category = "animals"
        self.level = level
        self.pile = Pile(category, level).game_randomize_pile()


# TODO: change sturcture: pile consists of category, size and a list of cards.