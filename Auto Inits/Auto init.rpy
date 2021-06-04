# -*- coding: utf-8 -*-
init python:

    def make_sprite_timed(image):
        return ConditionSwitch(
            "persistent.sprite_time == 'sunset'",
            im.MatrixColor(
                image,
                im.matrix.tint(0.94, 0.82, 1.0) # При свете дня...
            ),
            "persistent.sprite_time == 'night'",
            im.MatrixColor(
                image,
                im.matrix.tint(0.63, 0.78, 0.82) # Во тьме ночной...
            ),
            True, # Но на случаи когда ни туда ни сюда, выходит обычное изображение
            image
        )

    def initialize_mod_media(mod_name):
        """
        Эта функция является авто инитом подходящих в основном для модов
        игры "Everlasting Summer", я настоятельно не рекомендую использовать
        её в конечном билде мода, так как это повышает время прогрузки игры.
        """
        for file in renpy.list_files(): # Что, новомодное объявление файлов хотите? Ну смотрите, даже разьясню что это за бублик
            if mod_name in file: # Проверяет от нашего ли мода этот файл
                file_name = os.path.splitext(os.path.basename(file))[0] # Достаем имя файла

                if file.endswith((".png", ".jpg", ".webp")): # Фильтр на изображения

                    if "sprites" in file and  not "composite" in file: # Если он в директории спрайтов, то по красоте с матрицой добавляет спрайт # За исключением компонентных спрайтов
                        renpy.image( # По факту, так же обьявляет изображение, но реализуемо подругому. Не забудьте использовать bg cg и подобную херотеть в названии папок
                            file_name.replace("_", " "), # имя по которому будем обращаться
                            make_sprite_timed(file)
                        )
                    elif not "gui" in file: # Компоненты меню обьявляются в самом меню # по такой же логике создавать исключения и для других директорий
                        renpy.image(file.split("/")[-2]+" "+file_name,  # Ну а обычные ваши фончики фоточки обьявляются вот так
                            file,
                            )
                elif file.endswith((".wav", ".mp2", ".mp3", ".ogg", ".opus")): # Если хотите потусить под музычку
                    globals()[file_name] = file # Разьяснения нужны?





#####################################################
# Если хочется использовать именно автоинит, и если не было
# использовано специфичных - желательно использовать метод ниже
# так как этот метод будет "обьединятся" с остальными подобными
# тем самым, оно пройдет по списку лишь раз

init -900 python:

    try:
        eval("mods_to_auto_init") # проверяет существование списка
    except:
        mods_to_auto_init = set() # если нету - создает
    mods_to_auto_init.add("MOD_NAME") # Где MOD_NAME - директория в которой лежит мод (желательно тег мода)

    def initialize_all_mods_medias(): # если существует - перепишется

        if not mods_to_auto_init: # В случае если нету списка модов (например эта функция уже завершилась, во избежании повторов - она его стирает)
            return "No more mods to initialize" # функция не срабатывает и возвращает эту надпись

        for file in renpy.list_files(): # Что, новомодное объявление файлов хотите? Ну смотрите, даже разьясню что это за бублик
            for mod_name in mods_to_auto_init:
                if mod_name in file:
                    break
            else:
                mod_name = None
                continue

            file_name = os.path.splitext(os.path.basename(file))[0] # Достаем имя файла

            if file.endswith((".png", ".jpg", ".webp")): # Фильтр на изображения

                if "sprites" in file and  not "composite" in file: # Если он в директории спрайтов, то по красоте с матрицой добавляет спрайт # За исключением компонентных спрайтов
                    renpy.image( # По факту, так же обьявляет изображение, но реализуемо подругому. Не забудьте использовать bg cg и подобную херотеть в названии папок
                        file_name.replace("_", " "), # имя по которому будем обращаться
                        make_sprite_timed(file)
                    )
                elif not "gui" in file: # Компоненты меню обьявляются в самом меню # по такой же логике создавать исключения и для других директорий
                    renpy.image(file.split("/")[-2]+" "+file_name,  # Ну а обычные ваши фончики фоточки обьявляются вот так
                        file,
                        )
            elif file.endswith((".wav", ".mp2", ".mp3", ".ogg", ".opus")): # Если хотите потусить под музычку
                globals()[file_name] = file # добавляет значение в глобалы

        mods_to_auto_init.clear() # во избежании повторного круга

init 900 python:
    initialize_all_mods_medias()
