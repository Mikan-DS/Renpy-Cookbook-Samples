 # -*- coding: utf-8 -*-

default money = 410
default time = "23:59"

default inventory = inventory

default messages = []#["".join([renpy.random.choice(["", "", "", "",]+list("bfjs o 3i")) for i in range(50)]) for i in range(100)]

default strength = 98
default intellect = 0
default stamina = 48
default charisma = 67

default mcname = "Name"

init:

    python:
        inventory = []

        def overlay_path(path):
            return "order/gui/"+path # менять путь тут

        def set_at_mouse_pos(tl, *args, **kwargs):
            tl.xpos, tl.ypos = renpy.get_mouse_pos()
            return 0.001

        class InventoryItem:
            items = {}
            def __init__(self, name, image, action=None):
                """
                Так как не уточнили какие функции должен иметь
                инвентарь, я создал этот простой класс
                в котором есть имя (через которое можно добавлять вещи)
                картинка (которая собственно будет добавляться в инвентаре)
                и действие, которое выполняется при нажатии на инвентарь
                """
                self.name=name
                self.image=image
                self.action=action or NullAction()
                InventoryItem.items[name]=self
            def __call__(self):
                renpy.run(self.action)
            def __repr__(self):
                return "Item: <%s>"%self.name
            def __eq__(self, other):
                if isinstance(other, InventoryItem):
                    return self.name==other.name

        def add_item(name):
            inventory.append(InventoryItem.items[name])
        def remove_item(name):
            item = InventoryItem.items[name]
            if item in inventory:
                inventory.remove(item)

        def new_message(text):
            messages.append(text)


        #inventory = [InventoryItem("Phone%d"%i, "phone_icon.png", Function(remove_item, "Phone%d"%i)) for i in range(14)]
        #add_item("Phone")

    screen gui_overlay:
        tag overlay

        button:
            pos 35, 35
            xysize 147, 147
            background Frame(overlay_path("cell_frame_background.png"))
            add overlay_path("backpack.png") align .5, .5
            action Show("gui_inventory", dissolve)

        hbox:
            xysize 235, 52
            pos 194, 15
            frame:
                ysize 46
                xminimum 106
                background Frame(overlay_path("cell_text_background.png"))
                text "[money]$" size 24 color "A6002B" align .5, .5

            frame:
                ysize 46
                xminimum 106
                background Frame(overlay_path("cell_text_background.png"))
                text "[time]" size 24 color "A6002B" align .5, .5

        button:
            pos 1629, 15
            xysize 97, 97
            background Frame(overlay_path("cell_frame_background.png"))
            add overlay_path("game_map.png") align .5, .5
            action NullAction()#Show("map", dissolve)

        button:
            pos 1737, 36
            xysize 149, 149
            background Frame(overlay_path("cell_frame_background.png"))
            add overlay_path("phone_icon.png") align .5, .5
            action Show("phone", dissolve)


    screen gui_inventory:
        tag overlay

        default item_offset = 0
        default what_item_now = ""

        frame:

            xfill True
            ysize 217
            padding 0, 0
            background Frame(overlay_path("inventory_background.png"), tile=True)


        frame:
            background None
            padding 0, 0
            xfill True
            at transform:
                on show, replace:
                    xoffset -1703
                    ease .5 xoffset 0
            hbox:
                pos 272, 35
                xysize 1593, 147
                for i in range(9):
                    $ item = None if len(inventory) <= i+item_offset else inventory[i+item_offset]
                    button:
                        xysize 147, 147
                        background Frame(overlay_path("cell_frame_background%s.png"%(i%2*2 or "")))
                        if item:
                            action Function(item), SetScreenVariable("what_item_now", "")
                            hovered SetScreenVariable("what_item_now", item.name)
                            add overlay_path(item.image) align .5, .5
                        unhovered SetScreenVariable("what_item_now", "")

            imagebutton idle overlay_path("left.png") pos (217, 89) action SetScreenVariable("item_offset", max(0, item_offset-1))
            imagebutton idle overlay_path("right.png") pos (1850, 89) action SetScreenVariable("item_offset", min(item_offset+1, max(len(inventory)-9, 0)))

        button:
            pos 35, 35
            xysize 147, 147
            background Frame(overlay_path("cell_frame_background.png"))
            add overlay_path("backpack.png") align .5, .5
            action Show("gui_overlay", dissolve)

        if what_item_now:
            frame:
                at Transform(function=set_at_mouse_pos)
                ysize 46
                xminimum 106
                background Frame(overlay_path("cell_text_background.png"))
                text "[what_item_now]" size 24 color "A6002B" align .5, .5

    screen phone_bg:

        button:
            add Solid("0004")
            action Hide("phone")
        button:
            xalign .7
            xysize 520, 1038
            add overlay_path("phone/phone.png")
            frame:
                padding 0, 0
                pos 34, 31
                xsize 440
                background None
                add overlay_path("phone/screen.png")
                transclude
            add overlay_path("phone/upper_panel.png") pos 128, 31

    screen phone:
        tag phone
        modal True

        use phone_bg:
            hbox:
                spacing 20
                pos 70, 124
                imagebutton idle overlay_path("phone/icons/log.png") action Show("phone_log", dissolve)
                imagebutton idle overlay_path("phone/icons/stats.png") action Show("phone_stats", dissolve)

    screen phone_log:
        tag phone
        modal True

        use phone_bg:
            add overlay_path("phone/title_box.png")
            imagebutton idle overlay_path("phone/back.png") ypos 61 action Show("phone", dissolve)
            add overlay_path("phone/chat_image.png") pos 50, 53
            text "Name" color "#222" size 28 pos 122, 63 bold True

            viewport:
                xysize 440, 800
                pos 7, 120
                mousewheel True
                vbox:
                    spacing 20
                    for message in messages:
                        frame:
                            background Frame(overlay_path("phone/bubble.png"), 25, 25)
                            xminimum 200
                            xmaximum 430
                            padding 30, 25
                            text message color "000" xmaximum 370

    screen phone_stats:
        tag phone
        modal True

        use phone_bg:
            add overlay_path("phone/title_box.png")
            imagebutton idle overlay_path("phone/back.png") ypos 61 action Show("phone", dissolve)
            text _("Статистика") color "#222" size 28 pos 50, 63 bold True

            add overlay_path("phone/Mask.png") pos 126, 226

            text "[mcname]" size 38 color "222" xalign .5 ypos 441 bold True

            vbox:
                area (37, 596, 342, 257)
                use stats_bar(_("сила"),"#B7AFE3","strength")
                use stats_bar(_("интелект"),"#90BAA6","intellect")
                use stats_bar(_("стамина"),"#CB81AD","stamina")
                use stats_bar(_("харизма"),"#EBA089","charisma")


    screen stats_bar(name, color, value):
        frame:
            xysize 377, 49
            padding 0,0
            background overlay_path("phone/white_bar.png")
            add Frame(im.MatrixColor(overlay_path("phone/white_bar.png"), im.matrix.colorize("#6612", color)), 20) xsize (getattr(store, value)+10)/110.0

            add overlay_path("phone/stats/%s.png"%value) yalign .5 xpos 10
            text _(name) color "222" size 38 align .5, .5
