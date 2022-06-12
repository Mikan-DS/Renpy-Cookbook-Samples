# Вы можете расположить сценарий своей игры в этом файле.

# Определение персонажей игры.
define e = Character('Эйлин', color="#c8ffc8")

# Вместо использования оператора image можете просто
# складывать все ваши файлы изображений в папку images.
# Например, сцену bg room можно вызвать файлом "bg room.png",
# а eileen happy — "eileen happy.webp", и тогда они появятся в игре.

# Игра начинается здесь:
label start:

    scene image "snow_bg.png"

    show screen snow_falling(100)

    pause

    jump .loop


label .loop:

    window show dissolve
    "Снег падает..."
    "Снежинки"
    window hide dissolve

    pause

    jump .loop
