# -*- coding: utf-8 -*-
init -998 python:

    class open_3:
        """Возрадуйтесь! Запись в ютф теперь куда легче!"""
        def __init__(self, file, mode="w", encoding="UTF-8"):
            assert not "b" in mode, "для режима байтов используйте обычный open"
            self.file = open(file, mode+"b")
            self.encoding = encoding
        def write(self, what):
            what = what.encode(self.encoding)
            self.file.write(what)
        def read(self):
            return self.file.read().decode(self.encoding)
        def __enter__(self):
            return self
        def __exit__(self, *args, **kwargs):
            self.file.close()


    def get_image_tags(image):
        return image.split("_")


    def composite_wrap(size, images):

        images_string = ""
        for image in images:
            images_string+=', (0, 0), "%s"'%image

        return "im.Composite(%s%s)"%(str(size), images_string)


    def timed_sprite_wrap(image):

        images_string = """ConditionSwitch(
        "sprite_time=='night'",
            im.MatrixColor(%s,
                im.matrix.tint(0.63, 0.78, 0.82)
                ),
        "sprite_time=='sunset'",
            im.MatrixColor(%s,
                im.matrix.tint(0.94, 0.82, 1.0)
            ),
        True,
            %s
    )"""%(image, image, image)

        return images_string



    def simple_bg_wrap(name, image, tag):
        return '    image bg %s %s = "%s"'%(name, tag, image)

    def timed_bg_wrap(name, location):



        if len(location) > 1:
            if "day" in location:
                d_file = location.pop("day")
            else:
                k = list(location.keys())[0]
                d_file = location.pop(k)
            string = "    image bg %s = ConditionSwitch(\n"%name

            for k, file in location.items():
                string += '        "current_string_time()==\\"%s\\"",\n'%k
                string += '            "%s",\n'%file

            string += '        "True",\n'
            string += '            "%s"'%d_file

            string += ")"
        else:
            k = list(location.keys())[0]
            subname = "static" if k == name else k
            string = """
    image bg %s = "%s"
    image bg %s %s = "%s"\n
"""%(name, location[k], name, subname, location[k])

        return string


init -998 python:

    if 0:
        sprites_info = renpy.re.compile(r'.*(?<=/sprites/)([^/]*)/([^/]*)(/?)')

        files_to_init = {"timed_bg_wrap": {}, "sprites": {}, "bg": {}}

        for file in renpy.list_files(): # На релизах будем заменять вот это на обычное обьявление
            tags = file.split("/")
            file_name = tags[-1].rsplit(".", 1)[-2]


            if "bg" in tags:
                file_tags = file_name.rsplit("_", 1)

                if len(file_tags)>1 and file_tags[-1] in ["day", "morning", "evening", "night"]:
                    location_folder = file_tags[0]
                    if not location_folder in files_to_init["timed_bg_wrap"]:
                        files_to_init["timed_bg_wrap"][location_folder] = {}
                    files_to_init["timed_bg_wrap"][location_folder][ file_tags[-1] ] = file

                files_to_init["bg"][file_name] = file

            elif "sprites" in tags:

                # character, folder, static = sprites_info.match(file).groups()
                file_tags = sprites_info.match(file)
                if file_tags:
                    character, folder, static = file_tags.groups()
                    file_tags = get_image_tags(file_name)

                    if not character in files_to_init["sprites"]:
                        files_to_init["sprites"][character] = {}
                    wf = files_to_init["sprites"][character]

                    if not static:
                        if not "static" in wf:
                            wf["static"] = {}

                        if character == file_tags.pop(0):
                            wf["static"][" ".join(file_tags)] = file

                    if folder == "bodys":

                        if not "bodys" in wf:
                            wf["bodys"] = {}

                        wf["bodys"][file_tags[0]] = file

                    elif folder == "poses_dresses":

                        if not "poses_dresses" in wf:
                            wf["poses_dresses"] = {}

                        wf["poses_dresses"][(file_tags[0], file_tags[1])] = file

                    elif folder == "bodys_emotions":

                        if not "many_bodys" in wf:
                            wf["many_bodys"] = {}
                        wf = wf["many_bodys"]
                        if not file_tags[0] in wf:
                            wf[file_tags[0]] = {}
                        if not "emotions" in wf[file_tags[0]]:
                            wf[file_tags[0]]["emotions"] = {}
                        wf = wf[file_tags[0]]["emotions"]
                        wf[file_tags[1]] = file

                    elif folder == "bodys_poses_dresses":

                        if not "many_bodys" in wf:
                            wf["many_bodys"] = {}
                        wf = wf["many_bodys"]
                        if not file_tags[0] in wf:
                            wf[file_tags[0]] = {"poses_dresses": {}}
                        if not "poses_dresses" in wf[file_tags[0]]:
                            wf[file_tags[0]]["poses_dresses"] = {}
                        wf = wf[file_tags[0]]["poses_dresses"]
                        wf[" ".join([file_tags[1], file_tags[2]])] = file


                    elif folder == "emotions":

                        if not "emotions" in wf:
                            wf["emotions"] = {}
                        wf["emotions"][file_tags[0]] = file



        def generate_sprite(folder, name, *names):
            names = list(names)

            variants = {}

            if names:
                subfolder = names.pop(0)
                for subvar in generate_sprite(folder, subfolder, *names):
                    if name in folder:
                        for i, j in folder[name].items():
                            n = {name: (i, j)}
                            n.update(subvar)
                            yield n
                    else:
                        return subval
            else:
                if name in folder:
                    for i, j in folder[name].items():
                        yield {name: (i, j)}
                else:
                    yield {}


        sprites_composite_size = (720, 720)

        with open_3(config.basedir+"\\game\\sprites.rpy") as file:
            tab = "    "
            file.write("# -*- coding: utf-8 -*-\ninit:\n\n")

            if files_to_init["bg"]:

                file.write(tab+"# BG\n\n")

                for bg, images in files_to_init["bg"].items():
                    file.write(tab+"image bg %s = \"%s\""%(bg, images)+"\n")


            if files_to_init["timed_bg_wrap"]:

                file.write(tab+"# TIMED BG\n\n")

                for bg, images in files_to_init["timed_bg_wrap"].items():
                    file.write(timed_bg_wrap(bg, images)+"\n")

            if files_to_init["sprites"]:

                file.write("\n\n\n"+tab+"# SPRITES\n\n")

                for character, folder in files_to_init["sprites"].items():
                    # file.write(tab+"# %s\n\n"%character)

                    # for emotion_name, emotion_file in folder["emotions"]:
                    if "poses_dresses" in folder:
                        for (pose, dress), dress_image in folder["poses_dresses"].items():
                            for emotion, emotion_image in folder["emotions"].items():
                                images = [dress_image, emotion_image]
                                call_name = "%s %s %s %s"%(character, emotion, pose, dress)
                                #file.write(tab+"image %s = %s\n"%(call_name, composite_wrap(sprites_composite_size, images)))
                                file.write(tab+"image %s = %s\n"%(call_name, timed_sprite_wrap(composite_wrap(sprites_composite_size, images))))



                    if "bodys" in folder:
                        for pose, body_image in folder["bodys"].items():
                            for emotion, emotion_image in folder["emotions"].items():
                                images = [body_image, emotion_image]

                                if len(body_image)>1:
                                    call_name = "%s %s"%(character, emotion)
                                    file.write(tab+"image %s = %s\n"%(call_name, timed_sprite_wrap(composite_wrap(sprites_composite_size, images))))


                                call_name = "%s %s %s"%(character, emotion, pose)
                                file.write(tab+"image %s = %s\n"%(call_name, timed_sprite_wrap(composite_wrap(sprites_composite_size, images))))

                    if "many_bodys" in folder:
                        for body_folder in folder["many_bodys"].values():
                            # raise Exception(str(body_folder))
                            for dress, dress_image in body_folder["poses_dresses"].items():
                                for emotion, emotion_image in body_folder["emotions"].items():
                                    images = [dress_image, emotion_image]
                                    call_name = "%s %s %s"%(character, emotion, dress)
                                    #file.write(tab+"image %s = %s\n"%(call_name, composite_wrap(sprites_composite_size, images)))
                                    file.write(tab+"image %s = %s\n"%(call_name, timed_sprite_wrap(composite_wrap(sprites_composite_size, images))))



                    if "static" in folder:
                        for static_name, static in folder["static"].items():
                            file.write(tab+"image %s %s = %s\n"%(character, static_name, timed_sprite_wrap('"'+static+'"')))

                    file.write("\n\n")
