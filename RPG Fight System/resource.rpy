# -*- coding: utf-8 -*-
init:
    python:
        def ranper(percentage = .5):
            """
            Принимает в качестве параметра процент(float):
                Пример: 50% - 0.5

            :rtype: bool:
            :param percentage:
            :return: bool:
            """
            return renpy.random.random() < percentage


        class CharacterClass:
            def __init__(self, level = 1, attributes = None, **kwattr):
                """
                Родительский класс для всех классов персонажей.

                Принимает в качестве параметра начальный уровень,
                и словаря с аттрибутами персонажа, недописанные параметры будут указаны по умолчанию.

                    Пример: CharacterClass(1, {"Strench": 3, "Constitution": 10})

                Так же можно указывать аттрибуты по названию:

                    Пример: CharacterClass(1, Strench = 3, Constitution = 10)

                Аттрибуты указанные по ключам - в приоритете.

                :param level:
                :param attributes:
                :param kwattr:
                """
                self.level = level

                self.attributes = {
                    "Strench": 13,
                    "Constitution": 10,
                    "Dexterity": 10,
                    "Health": 100,
                    "Stamina": 100
                }
                if attributes:
                    self.attributes.update(attributes)
                self.attributes.update(**kwattr)

                self.health = self.Health
                self.fatigue = self.Stamina

                # self.last_action = None # В данной версии нет нужды, позже, возможно использования "комбо" техник

            @property
            def Health(self):
                """
                Возвращает статичное колличество здоровья персонажа.
                :return: int:
                """
                return self.attributes["Health"]

            @property
            def Stamina(self):
                """
                Возвращает статичное колличество усталости персонажа.
                :return: int:
                """
                return self.attributes["Stamina"]

            def attack(self):
                """
                Высчитывает колличество урона от персонажа, а так-же
                расчитывает и добавляет шанс на критический удар.

                Возвращает список из двух элементов:
                    (урон, крит) где урон - урон наносимый персонажем с учетом крита, крит - булевое
                    значение обозначающее был ли критический удар.

                :return: tuple:
                """
                critic = 3 if ranper(.3 + self.attributes["Dexterity"] * 0.001) else 1  # Шанс крита

                return (self.attributes["Strench"] * (0.8 + renpy.random.random() * 0.4) * critic,
                        True if critic > 1 else False)

            def defend(self, lvl):
                """
                Высчитывает смог ли персонаж уклонится от атаки.

                Получает в качестве параметра уровень атакующего.

                Возвращает число(int) 0 или 1:
                    где 0 - увернулся, а 1 - нет.

                :param lvl:
                :return: int:
                """
                return 0 if ranper(.1 + (self.level - lvl) * 0.01 + self.attributes["Dexterity"] * 0.001) else 1  # Шанс уворота


        class Enemy:

            def __init__(self, level=1, name="", sprite=None, health=666, strench=4, critic=0.3):
                """
                Родительский класс для всех классов персонажей.

                Принимает в качестве параметра начальный уровень, имя, путь к спрайту или Displayable, Общее здоровье, силу, и шанс на
                критический урон.

                :param level:
                :param name:
                :param sprite:
                :param health:
                :param strench:
                :param critic:
                """
                self.level = level
                self.name = name
                self.sprite = sprite or Null()
                self.health = self.Health = health
                self.Strench = strench
                self.critic = critic

            def attack(self):
                """
                Высчитывает колличество урона от противника, а так-же
                расчитывает и добавляет шанс на критический удар.

                Возвращает список из двух элементов:
                    (урон, крит) где урон - урон наносимый противником с учетом крита, крит - булевое
                    значение обозначающее был ли критический удар.

                :return: tuple:
                """
                critic = 2 if ranper(self.critic) else 1  # Шанс крита
                return (self.Strench * (0.8 + renpy.random.random() * 0.4) * critic,
                        True if critic > 1 else False)

            def defend(self, lvl):
                """
                Высчитывает смог ли противник уклонится от атаки.

                Получает в качестве параметра уровень атакующего.

                Возвращает число(int) 0 или 1:
                    где 0 - увернулся, а 1 - нет.

                :param lvl:
                :return: int:
                """
                return 0 if ranper(.1 + (self.level - lvl) * 0.01) else 1  # Шанс уворота


        class Slime(Enemy):
            def __init__(self, *args):
                """
                Пример под класса противника
                :param args:
                """
                super(Slime, self).__init__()

                self.name = "Слизь"
                self.sprite = "images/Slime.png"  # Должно быть в наборе


        def attack(a, d):
            """

            Функция атаки (общая).

            Высчитывает урон и уклонение, меняя здоровье противнику.
            Создает информационный текст.
            Меняет очередь.
            И вызывает окно "удара".

            В качестве параметров принимает экземляры классов атакующего (a) и
            отбивающего (d)

            :param a:
            :param d:
            """
            global turn

            hp, c = a.attack()
            hp = int(hp)
            m = d.defend(a.level)
            hp *= m

            d.health -= hp

            info = ('' if m else 'промахнулись и ') + "нанесли" + (' критический удар!' if m and c else '') + ": "
            Show("attack_screen", hpunch, a, d, hp, info, m)()

            turn = not turn


        def start_battle():
            """
            Функция для упрощения начала сражения.

            -Меняет очередь что бы игрок бил первым.
            -Запускает основную механику.
            """
            turn = True
            Show("FightInterface")()




    #### Значения по умолчанию
    default player = CharacterClass()
    default enemies = [Slime()]
    default turn = True

    screen player_stats:

        tag stats

        vbox:
            xmaximum 0.98
            align (.5, .1)
            spacing 14
            first_spacing 20

            text "Игрок" xalign .5

            hbox:
                text "Здоровье:         "
                bar value player.health range player.Health xsize 300

            hbox:
                text "Выносливость: "
                bar value player.fatigue range player.Stamina xsize 300


    screen Enemy_Fight(attack=False):

        vbox:
            align (.5, .2)
            spacing 10
            text enemies[0].name xalign .5
            bar value enemies[0].health range enemies[0].Health xsize 270 ysize 20 xalign .5

        add enemies[0].sprite size (300, 300) align (.5,.5)

    screen FightInterface():

        tag Fight

        modal True
        zorder 998

        frame:
            xsize 700
            ysize 500
            align (.5, .4)

            use Enemy_Fight

        frame:
            ysize 350
            xsize 1920
            align (.5, 1.0)

            frame:
                xsize 650
                ysize 350
                xalign .5

                use player_stats

            if not renpy.get_screen("attack_screen"):
                if turn:
                    textbutton "Атака" action Function(attack, player, enemies[0])
                else:
                    timer 1.0 action Function(attack, enemies[0], player)

    screen attack_screen(a, d, hp, info, m, *args):

        modal True
        zorder 999

        if isinstance(a, Enemy):

            add Text("{color=#C33}По вам "+info+str(hp)+"{/color}", slow_cps=80) align (.5, .1)

            if m:
                add Solid("#F443"):
                    at transform:
                        alpha 0.0
                        linear 0.4 alpha 1.0
                        linear 0.2 alpha 0.0

        else:

            add Text("Вы "+info+str(hp), slow_cps=80) align (.5, .25)

            if m:
                add Solid("#F33", xsize=180, ysize=19):

                    at transform:

                        yanchor 0.5
                        pos (0.5, 0.47)
                        xoffset -40
                        alpha 1.0

                        xzoom 0
                        linear 0.4 xzoom 1.0
                        linear 0.4 alpha 0.0

        timer 2.5 action (Hide("attack_screen", dissolve))

label splashscreen: # Что бы игра запускалась сразу в битву

    $start_battle()
    pause
    return
