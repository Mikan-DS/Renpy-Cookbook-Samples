# -*- coding: utf-8 -*-
init python:

    def timed_wrap(code):

        return """ConditionSwitch(
            "persistent.sprite_time=='sunset'",
                im.MatrixColor(
{sprite},
                    im.matrix.tint(0.94, 0.82, 1.0)
                    ),
            "persistent.sprite_time=='night'",
                im.MatrixColor(
{sprite},
                    im.matrix.tint(0.63, 0.78, 0.82)
                ),
            True,
{sprite}
)""".format(sprite=code)

    def init_image(name, file, timed=False):

        code = "    image "+name+" = "
        if timed:
            file = timed_wrap('"'+file+'"')

        return code + file


    def init_gen(mod_name):

        sprites = []
        other = []
        audio = []

        for file in renpy.list_files(): # Что, новомодное объявление файлов хотите? Ну смотрите, даже разьясню что это за бублик
            if mod_name in file: # Проверяет от нашего ли мода этот файл
                file_name = os.path.splitext(os.path.basename(file))[0] # Достаем имя файла
                if file.endswith((".png", ".jpg", ".webp")): # Фильтр на изображения
                    if "sprites" in file:
                        if not "composite" in file: # Если он в директории спрайтов, то по красоте с матрицой добавляет спрайт # За исключением компонентных спрайтов
                            sprites.append(
                                init_image(
                                file_name.replace("_", " "), # имя по которому будем обращаться
                                file,
                                True
                                )
                            )
                    elif not "gui" in file: # Компоненты меню обьявляются в самом меню # по такой же логике создавать исключения и для других директорий
                        other.append(init_image(file.split("/")[-2]+" "+file_name,
                            '"'+file+'"',)
                            )
                elif file.endswith((".wav", ".mp2", ".mp3", ".ogg", ".opus")): # Если хотите потусить под музычку
                    globals()[file_name] = file # Разьяснения нужны?
                    audio.append("        "+file_name+' = "'+file+'"')

        code = """# Код был автосгенерирован утилитой от https://github.com/Mikan-DS

init:
"""
        if sprites:
            code+="""
    # Спрайты
"""
            for sprite in sprites:
                print(sprite)
                code+=sprite+"\n"

        if other:

            code+="""


    # Разные изображения
"""

            for oth in other:
                print(oth)
                code+=oth+"\n"

        if audio:
            code+="""


    # Аудио

    python: # выглядит красивее чем $ перед каждой строкой
"""
            for au in audio:
                print(au)
                code+=au+"\n"

        with open("mod_sprites.rpy", "w") as file:
            file.write(code)

        raise Exception("Файл \"mod_sprites.rpy\" в корневой папке игры с обьявлением медия создан! И в целях что бы вы помнили что оставлять инитген в проекте крайне не желательно - игра не запустится пока в ней будет эта функция (она не нужна при запуске других медия)")

    init_gen("MOD_NAME")
