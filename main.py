# coding=utf-8

# //////////////////
# ФАЙЛ ЗАПУСКА ИГРЫ
# //////////////////

from game import Game


def main():  # Функция вызова игры (главный файл)
    game = StarWars()
    game.run()


class StarWars(Game):
    def __init__(self):
        super(StarWars, self).__init__()


if __name__ == '__main__':
    main()
