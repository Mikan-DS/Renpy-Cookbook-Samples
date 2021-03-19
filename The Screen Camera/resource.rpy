# -*- coding: utf-8 -*-
# Credits: https://vk.com/vbif97
init:

    python:
        x_drop = 0
        y_drop = 0
        def detective_dragged(drags, drop):
            global x_drop, y_drop
            x_drop = drags[0].x
            y_drop = drags[0].y

            renpy.restart_interaction()

    image korra = "images/korra.jpg"

    screen phone_photo():
        drag:
            xpos x_drop ypos y_drop
            drag_name "phone"
            droppable False
            drag_handle (0, 0, 1.0, 1.0)
            dragged detective_dragged
            frame:
                xysize (467, 953)
                background "images/phone.png"

                add "korra" crop (x_drop + 25, y_drop + 110, 405, 720) xpos 25 ypos 110

label splashscreen: # Debug

    scene korra
    call screen phone_photo

    pause
    return
