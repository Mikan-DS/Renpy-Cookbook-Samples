define current_sub_menu = False

define _game_menu_screen = "game_menu"


## Ширина и высота миниатюры, используемой слотом сохранения.
define config.thumbnail_width = 192
define config.thumbnail_height = 108



init:


    transform move_in(left=True):
        yoffset 1080
        xalign (-.5 if left else .5)

        ease .9 yoffset 0 xalign 0.0

    transform move_out(left=True):
        yoffset 0
        xalign 0.0

        ease .9 yoffset 1080 xalign (-.5 if left else .5)

    style magazine_text is button_text:
        color "000"
        outlines [(1, "000")]
        hover_outlines [(1, "FF0")]

        size 38
        font "fonts/PRINTF.ttf"
    style magazine_button_text is magazine_text


    screen navigation(mode=True):

        style_prefix "magazine"

        if main_menu:
            add "gui/menu/main_menu.jpg"
            # if current_sub_menu:
            #     key "K_e" action Show(current_sub_menu, mode="hide")

        else:
            key "game_menu" action Function(renpy.show_screen, current_sub_menu or "game_menu", mode="hide")
        on "show" action Function(renpy.show_layer_at, Transform(blur=9))
        on "hide" action [Function(renpy.show_layer_at, Transform(blur=0)), SetVariable("current_sub_menu", False)]



        frame:
            if mode:
                if mode == "hide" and not main_menu:
                    at move_out(True)
                    if not current_sub_menu:
                        timer 1.01 action Return()
                if current_sub_menu==False:
                    at move_in(True)
                timer 1 action SetVariable("current_sub_menu", None)


            background "gui/menu/left_hand.png"

            xsize 800

            vbox:

                pos 180, 380
                at Transform(rotate=7)

                if main_menu:
                    textbutton "Начать игру" action [SetVariable("current_sub_menu", False), Start()]
                else:
                    textbutton "Вернуться" action Function(renpy.show_screen, current_sub_menu or "game_menu", mode="hide")#Show(current_sub_menu or "game_menu", mode="hide")
                    textbutton "Сохранить" action ShowMenu("save")
                textbutton "Загрузить" action ShowMenu("load")
                textbutton "Настройки" action ShowMenu("preferences")
                if main_menu:
                    textbutton "Выйти" action Quit()
                else:
                    textbutton "Главное меню" action MainMenu()


        transclude
        add "gui/menu/logo.png":
            if current_sub_menu==False:
                at transform:
                    alpha (1.0 if mode == "hide" else 0.0)
                    ease .8 alpha (0.0 if mode == "hide" else 1.0)




    screen main_menu():

        tag menu

        use navigation

    screen game_menu(mode=True):

        tag menu

        on "hide" action If("mode", Show("navigation", mode="hide"))

        # if not mode:
        #     timer 1 action Return()

        use navigation(mode)


    screen sub_menu(title="sub_menu", mode=False):

        style_prefix "magazine"


        use navigation(mode=mode):


            timer 1 action SetVariable("current_sub_menu", title)


            frame:
                if mode == "hide":
                    at move_out(False)
                    timer 1 action Return()
                elif not current_sub_menu:
                    at move_in(False)
                    # $ current_sub_menu =
                background "gui/menu/right_hand.png"

                xsize 900

                frame:

                    xpos 1.0
                    ypos 200

                    background None#Solid("F005")
                    xsize 780

                    # textbutton "nya" xalign 1.0 action Show(title, mode="hide")#Function(renpy.show_screen,title, mode="hide")
                    transclude

    style preferences_button_text is magazine_text:
        color "555"
        selected_color "000"
        selected_underline True

        outlines [(1, "000")]
        hover_outlines [(1, "FF0")]

        size 38
        font "fonts/PRINTF.ttf"
    style preferences_button_text is magazine_button_text
    style preferences_label_text is magazine_text

    style preferences_vbox:

        first_spacing 10
        spacing 2


    style preferences_hbox:

        spacing 60

    style preferences_bar:

        left_bar Frame("gui/menu/base_bar.png", tile=True)
        right_bar Frame(Solid("999"))
        ysize 92
        xsize 1300
        thumb Solid("800", ysize=92, xsize=20)



    screen preferences(*args, **kwargs):

        tag menu

        style_prefix "preferences"


        use sub_menu("preferences", *args, **kwargs):

            vbox:

                label _("Настройки") text_size 50 xalign .1

                null height 40

                hbox:

                    xalign .5

                    vbox:
                        label _("Режим экрана") xoffset -10

                        textbutton _("Оконный") action Preference("display", "window")
                        textbutton _("Полный") action Preference("display", "fullscreen")

                    vbox:
                        label _("Пропуск текста") xoffset -10

                        textbutton _("Всего текста") action Preference("skip", "toggle")
                        textbutton _("После выборов") action Preference("after choices", "toggle")
                        textbutton _("Переходов") action InvertSelected(Preference("transitions", "toggle"))

                null height 40

                hbox:
                    vbox:
                        label _("Скорость текста") xoffset -10
                        frame:
                            background Frame(Solid("000"), 0, 0)
                            padding (0, 0)

                            bar value Preference("text speed"):
                                style "preferences_bar"
                                at Transform(zoom=.3)

                    vbox:
                        label _("Авточтение") xoffset -10
                        frame:
                            background Frame(Solid("000"), 0, 0)
                            padding (0, 0)

                            bar value Preference("auto-forward time"):
                                style "preferences_bar"
                                at Transform(zoom=.3)

                null height 70


                vbox:
                    label _("Громкость музыки") xoffset -10
                    frame:
                        background Frame(Solid("000"), 0, 0)
                        padding (0, 0)

                        bar value Preference("music volume"):
                            style "preferences_bar"
                            at Transform(zoom=.4)

                vbox:
                    label _("Громкость звуков") xoffset -10
                    frame:
                        background Frame(Solid("000"), 0, 0)
                        padding (0, 0)

                        bar value Preference("sound volume"):
                            style "preferences_bar"
                            at Transform(zoom=.4)



# screen file_slots(title, *args, **kwargs):
#
#     tag menu
#
#     style_prefix "preferences"
#
#     default page_name_value = FilePageNameInputValue(pattern=_("{} страница"), auto=_("Автосохранения"), quick=_("Быстрые сохранения"))
#
#
#
#     use sub_menu("preferences", *args, **kwargs):
#
#         label title
#
#
#
#         text page_name_value.get_text() style "page_label"
#
#
#
#         ## Таблица слотов.
#         vbox:
#
#             xalign 0.5
#             yalign 0.5
#
#
#             for y in range(3):
#
#                 hbox:
#
#
#                     for x in range(2):
#
#                         $ slot = (x*y) + 1
#
#                         add FileScreenshot(slot, empty=Frame("gui/menu/slot_background.png"))
#
#
#
#         ## Кнопки для доступа к другим страницам.
#         hbox:
#             style_prefix "page"
#
#             xalign 0.5
#             yalign 1.0
#
#             spacing gui.page_spacing
#
#             textbutton _("<") action FilePagePrevious()
#
#             if config.has_autosave:
#                 textbutton _("{#auto_page}А") action FilePage("auto")
#
#             if config.has_quicksave:
#                 textbutton _("{#quick_page}Б") action FilePage("quick")
#
#             ## range(1, 10) задаёт диапазон значений от 1 до 9.
#             for page in range(1, 10):
#                 textbutton "[page]" action FilePage(page)
#
#             textbutton _(">") action FilePageNext()
