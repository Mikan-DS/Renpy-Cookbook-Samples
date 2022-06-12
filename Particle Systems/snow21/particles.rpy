# -*- coding: utf-8 -*-

init:
    python:
        def particle_working(trans, st, at):
            """
            Костыльно, но зато просто
            """

            try:
                trans.particle["xmod"] += (.00001 - renpy.random.random()*.00002)
                trans.yalign += trans.particle["speed"]+0.0007
                trans.xalign += trans.particle["xmod"]
                if trans.yalign > 1.1 or trans.xalign > 1.1 or trans.xalign < -0.1:
                    raise
                return .01
            except:
                trans.alpha = .5+(renpy.random.random()/2)
                trans.zoom = .2+(renpy.random.random()/2)
                trans.xalign = renpy.random.random()
                trans.yalign = -.1
                trans.particle = {
                    "xmod": (1 - renpy.random.random()*2)/1000+.0004,
                    "speed": renpy.random.random()/500
                }
                return renpy.random.random()*5


    transform particle_moves():
        alpha 0
        function particle_working
        pause .3
        repeat


    screen snow_falling(count=25):

        text "[count] снежинок одновременно"
        for i in range(count):
            add "particle.png" at particle_moves
