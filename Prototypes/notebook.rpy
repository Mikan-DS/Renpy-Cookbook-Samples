default persistent.notes = []

default notes = set() # Записки доступные в игре
default last_note = None

python early:

    class OpenNote(Action):

        def __init__(self, note):
            self.note = note
        def __eq__(self, other):
            if isinstance(other, OpenNote):
                return self.note == other.note
            return False
        def get_selected(self):
            if last_note and renpy.get_screen("notes"):
                print(self.note.name,last_note.name == self.note.name)
                return last_note.name == self.note.name
        def __call__(self):

            # renpy.show_screen("notes", note=self.note)
            renpy.run([SetVariable("last_note", self.note), Show("notes", dissolve, note=self.note)])

    class Note:
        def __init__(self, name, text, color): # Просто для хранения блокнотов
            self.name = name
            self.text = [text] if isinstance(text, str) else list(text)
            self.color = color

        def __eq__(self, other):

            if not isinstance(other, Note):
                return False
            return self.name == other.name


    def add_note(text, name=None, color="FF0A"):

        name = name or _("Записка")+"№"+str(len(notes)+1)

        note = Note(name, text, color)

        if not notes:
            last_note = note

        notes.add(note)
        # if persistent.notes == None:
        #     persistent.notes == []
        if note in persistent.notes: # с каких то пор у set перестала работать функция сравнения, потому тут костыль
            persistent.notes.remove(note)
        #
        # # persistent.notes += [note]
        persistent.notes.append(note)
        # # renpy.save_persistent()



init:



    style notebook_text:

        font "fonts/Caveat.ttf"
        size 38

    style notebook_label_text:

        font "fonts/BalsamiqSans.ttf"
        color "666"
        size 60

    style notebook_button_right_text is notebook_text:

        size 30
        bold True
        color "666"#"AAA"

    style notebook_button_left_text is notebook_button_right_text


    transform notebook_button(left=False):

        xoffset 0

        xanchor (0.0 if left else 1.0)
        xpos (1.0 if left else 0.0)

        on idle:
            ease .3 xanchor (0.0 if left else 1.0) xoffset (-80 if left else 80)
        on hover:
            ease .3 xanchor (1.0 if left else 0.0) xoffset (50 if left else -50)
        on start:
            ease .3 xanchor (1.0 if left else 0.0) xoffset (5 if left else -5)



    style notebook_button_left:

        xminimum 140
        yminimum 58

        padding (10, 10, 90, 10)

    style notebook_button_right is test_button_left:

        padding (90, 10, 10, 10)


    screen notebook_navigation(chap=""):

        # add Solid("FFF")

        if main_menu:
            add "gui/main_menu_background.png"

        add "gui/notebook/background.png"

        key "K_q" action Return()
        key "game_menu" action Return()

        on "show" action Function(renpy.show_layer_at, Transform(blur=14))
        on "hide" action Function(renpy.show_layer_at, Transform(blur=0))



        frame:

            # background Frame(Solid("F00")) # Для измерения коробки vbox

            xpos .838

            yanchor 1.0
            ypos .9

            vbox:

                spacing 5

                xanchor 0.0


                # text "!" xalign 0.0 # Для измерения положения слайдеров в финальном положении
                # text "!" xalign 1.0

                for note in (notes if not main_menu else persistent.notes):
                    textbutton note.name background Frame(Solid(note.color)) style "notebook_button_right" action OpenNote(note) at notebook_button(False)


        frame:

            # background Frame(Solid("F00"))


            xpos .16

            ypos .21


            vbox:

                spacing 30

                xanchor 1.0


                # text "!" xalign 0.0
                # text "!" xalign 1.0

                # for i in range(5):
                #     textbutton _("X"*(i*3)) background Frame(Solid("CC39")) style "notebook_button_left" action Start() at notebook_button(True)

                if main_menu:

                    textbutton _("Начать игру") background Frame(Solid("C3FC")) style "notebook_button_left" action Start("chapter_1") at notebook_button(True)

                else:

                    textbutton _("Вернуться") background Frame(Solid("C3FC")) style "notebook_button_left" action Return() at notebook_button(True)


                textbutton _("Настройки") background Frame(Solid("09FC")) style "notebook_button_left" action ShowMenu("preferences") at notebook_button(True)

                textbutton _("Загрузить") background Frame(Solid("2D2C")) style "notebook_button_left" action ShowMenu("load") at notebook_button(True)

                if not main_menu:
                    textbutton _("Сохранить") background Frame(Solid("CC1C")) style "notebook_button_left" action ShowMenu("save") at notebook_button(True)
                    textbutton _("В главное меню") background Frame(Solid("F6CC")) style "notebook_button_left" action MainMenu() at notebook_button(True)


                else:

                    textbutton _("Выход") background Frame(Solid("F6CC")) style "notebook_button_left" action Quit() at notebook_button(True)

        frame:
            background None
            # imagebutton idle "gui/notebook/frame.png" focus_mask True action NullAction() # Старая версия
            imagebutton idle "gui/notebook/foreground.png" focus_mask True action NullAction() # Что бы случайно не активировать заметки


            label chap pos (.19, .2) style "notebook_label"

            transclude





    style notebook_bar is bar:

        ysize 26
        base_bar Frame("gui/notebook/bar.png")
        thumb "gui/notebook/thumb.png"


    style preferences_label_text is notebook_label_text:
        size 45
        color "444"
    style preferences_text is notebook_text:
        color "666"
        # outlines [(1, "666", 1, 1)]
        size 52
        selected_outlines [(1, "666", 1, 1)]
        selected_underline True
    style preferences_button_text is preferences_text



    screen preferences():

        tag menu

        default text_example = True

        style_prefix "preferences"

        use notebook_navigation(_("Настройки")):

            vbox:

                xpos .19
                ypos .3
                spacing 20

                xsize 540
                ysize 670


                label _("Режим окна")

                frame:
                    ysize 116
                    textbutton _("полноэкранный") yalign .5 action Preference("display", "fullscreen")
                    add "gui/notebook/fullsize.png"  yalign .5 xalign 1.0

                frame:
                    ysize 116
                    textbutton _("оконный") yalign .5 action Preference("display", "window")
                    add "gui/notebook/windowed.png" xalign 1.0



                label _("Пропуск")

                frame:
                    ysize 116
                    textbutton _("всего текста") yalign .5 action Preference("skip", "toggle")
                    add "gui/notebook/all_text.png"  yalign .5 xalign 1.0

                frame:
                    ysize 116
                    textbutton _("после выборов") yalign .5 action Preference("after choices", "toggle")
                    add "gui/notebook/after_choice.png" xalign 1.0



            vbox:

                xpos .53
                ypos .3
                # spacing 0#20

                xsize 540
                ysize 670

                yfill False


                label _("аудио")

                frame:
                    ysize 20

                    bar value Preference("music volume") xsize .7 yalign .5 xalign 1.0 style "notebook_bar"
                    textbutton _("Музыка") yalign .5 action ToggleMute("music") text_selected_underline False text_selected_strikethrough True

                frame:
                    ysize 20

                    bar value Preference("sound volume") xsize .7 yalign .5 xalign 1.0 style "notebook_bar"
                    textbutton _("звуки") yalign .5 action ToggleMute("sfx") text_selected_underline False  text_selected_strikethrough True

                label _("Скорость текста")

                frame:
                    ysize 20

                    bar value Preference("text speed") xsize .6 yalign .5 style "notebook_bar"
                    text (str(int(preferences.text_cps))+" символов/сек." if preferences.text_cps else _("Моментально")) yalign .5 xalign 1.0 size 35


                add Frame("gui/notebook/fullsize.png", 20, 20) xsize 500 ysize 120


            if text_example:
                textbutton "Пример скорости текста" xpos .54 ypos .78 action ToggleScreenVariable("text_example"), Show("text_example") text_selected_underline False text_selected_outlines []



    screen text_example():

        # python:
        #     if not renpy.get_screen("preferences"):
        #         renpy.hide_screen("test_example")

        showif renpy.get_screen("preferences"):

            textbutton "Пример скорости текста":
                text_slow_cps preferences.text_cps xpos .54 ypos .78 action [Hide("text_example"), Show("text_example")] text_style "preferences_text" text_selected_underline False text_selected_outlines []

        else:

            timer .00001 action Hide("text_example")



    screen file_slots(title):

        default page_name_value = FilePageNameInputValue(pattern=_("{} страница"), auto=_("Автосохранения"), quick=_("Быстрые сохранения"))

        style_prefix "notebook"


        use notebook_navigation(title):

            label page_name_value.get_text() ypos .2 xalign .71 yoffset 20 text_size 40 # оффсет = 60-размер текста

            vbox:

                xalign .27
                ypos .325

                xsize 540
                # ysize 670
                spacing 10

                for slot in range(1, 4):

                    hbox:

                        spacing 30

                        button:
                            action FileAction(slot)

                            yalign 0.5

                            xsize config.thumbnail_width
                            ysize config.thumbnail_height

                            background None
                            hover_background Solid("FF0",xsize=config.thumbnail_width+8, ysize=config.thumbnail_height+8)

                            padding (4, 4)


                            add FileScreenshot(slot, Solid("555", xsize=config.thumbnail_width , ysize=config.thumbnail_height))

                            frame:

                                xalign .5
                                yalign .5
                                xfill True
                                padding (0, 5)

                                background Solid("444", xsize=config.thumbnail_width)

                                text FileSaveName(slot, empty=_("Пустой слот")) text_align .5 xalign .5 color "FFF" hover_color "FF0"


                        textbutton "X":
                            text_font "DejaVuSans.ttf"
                            text_bold True
                            text_size 70
                            text_color "0000"
                            text_outlines [(3, "000", 0, 0)]
                            text_hover_outlines [(3, "FF0", 0, 0), (2, "000", 0, 0)]
                            yalign .5
                            action FileDelete(slot)


                        key "save_delete" action FileDelete(slot)

                hbox:
                    style_prefix "page"

                    xalign 0.5
                    yalign 1.0

                    yoffset -20 #Для дрочки используйте оффсеты

                    spacing gui.page_spacing

                    textbutton _("<") action FilePagePrevious() text_style "notebook_text" text_hover_color "FF0"  text_selected_color "000" text_color "444" text_size 65 yalign 0.5

                    textbutton _("{#auto_page}А") action FilePage("auto") text_style "notebook_text" text_hover_color "FF0"  text_selected_color "000" text_color "444" text_size 39 yalign 0.5

                    textbutton _("{#quick_page}Б") action FilePage("quick") text_style "notebook_text" text_hover_color "FF0"  text_selected_color "000" text_color "444" text_size 39 yalign 0.5

                    for page in range(1, 5):
                        textbutton "[page]" action FilePage(page) text_style "notebook_text" text_hover_color "FF0"  text_selected_color "000" text_color "444" text_size 50 yalign 0.5


            vbox: # Я мог на изи забыть синхронизировать координаты при задрочке


                #xpos .53
                xalign .73
                ypos .325
                xsize 400
                # ysize 705
                spacing 10




                for slot in range(4, 7):

                    hbox:

                        spacing 30


                        button:
                            action FileAction(slot)

                            yalign 0.5

                            xsize config.thumbnail_width
                            ysize config.thumbnail_height

                            background None
                            hover_background Solid("FF0",xsize=config.thumbnail_width+8, ysize=config.thumbnail_height+8)

                            padding (4, 4)


                            add FileScreenshot(slot, Solid("555", xsize=config.thumbnail_width , ysize=config.thumbnail_height))

                            frame:

                                xalign .5
                                yalign .5
                                xfill True
                                padding (0, 5)

                                background Solid("444", xsize=config.thumbnail_width)

                                text FileSaveName(slot, empty=_("Пустой слот")) text_align .5 xalign .5 color "FFF" hover_color "FF0"


                        textbutton "X":
                            text_font "DejaVuSans.ttf"
                            text_bold True
                            text_size 70
                            text_color "0000"
                            text_outlines [(3, "000", 0, 0)]
                            text_hover_outlines [(3, "FF0", 0, 0), (2, "000", 0, 0)]
                            yalign .5
                            action FileDelete(slot)


                        key "save_delete" action FileDelete(slot)


                hbox:
                    style_prefix "page"

                    xalign 0.5
                    yalign 1.0

                    spacing gui.page_spacing

                    yoffset -20


                    for page in range(5, 11):
                        textbutton "[page]" action FilePage(page) text_style "notebook_text" text_hover_color "FF0"  text_selected_color "000" text_color "444" text_size 50 yalign 0.5

                    textbutton _(">") action FilePageNext() text_style "notebook_text" text_hover_color "FF0" text_selected_color "000" text_color "444" text_size 60 yalign 0.5


    screen notes(note=None):

        tag menu

        $ note = note or last_note

        default page = 0

        use notebook_navigation("Блокнот"):

            if note:

                if len(note.text) > page*2:
                    frame:

                        xpos .19
                        ypos .3
                        xsize 540
                        ysize 670

                        background None#Frame(Solid("F007"))

                        text note.text[page*2]# first_indent 3


                if len(note.text) > page*2+1:
                    frame:

                        xpos .525
                        ypos .3
                        xsize 540
                        ysize 670

                        background None#Frame(Solid("F007"))

                        text note.text[page*2+1]# first_indent 3


                hbox:
                    xalign .67
                    ypos .2
                    xsize 130
                    textbutton "<" action If(page>0, SetScreenVariable("page", page-1)) text_style "notebook_text" text_hover_color "FF0" text_color "000" text_insensitive_color "444" text_size 60 yalign 0.5
                    text str(page+1) style "notebook_text" color "000" size 60 yalign 0.5
                    textbutton ">" action If(page*2+1<len(note.text), SetScreenVariable("page", page+1)) text_style "notebook_text" text_hover_color "FF0" text_color "000" text_insensitive_color "444" text_size 60 yalign 0.5

            else:

                if notes:
                    timer 0.00001 action OpenNote(list(notes)[0])
                else:
                    timer 0.00001 action ShowMenu("save")
