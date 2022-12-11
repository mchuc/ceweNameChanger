#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# install pillow
# python -m pip install pillow
#
########################################################
# (C) Marcin Chuć 2022 marcin -is working- at afya.pl
########################################################
try:
    import re
    import os
    from PIL import Image
except:
    print("You have to install Pillow: python -m pip install Pillow")
    print("Exiting...")
    exit(0)

SEARCH_PATH = os.path.dirname(__file__)
FILTER0 = r"^.*(\.jpg|\.png|\.jpeg)$"  # just only JPG ang PNG images
FILTER1 = r"^[0-9]{4}\-[0-9]{2}\-[0-9]{2}.*(\.jpg|\.png|\.jpeg)$"  # correctName



def file_list(path):
    output = []
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            if re.match(FILTER0, file, re.MULTILINE | re.IGNORECASE):
                if re.match(FILTER1, file, re.MULTILINE | re.IGNORECASE):
                    print("I'm skiping correct fileneme: ", file)
                else:
                    print("Adding file", file)
                    output.append(file)
            else:
                print("I'm skiping file: ", file, " it's not JPEG or PNG")
    return output


def begin():
    print("Getting files from ", SEARCH_PATH, " ...")
    files = file_list(SEARCH_PATH)
    print("Working... (not to hard)...")
    for f in files:
        file_name = os.path.join(SEARCH_PATH, f)
        if os.path.isfile(file_name):
            try:
                image = Image.open(file_name)
                exifdata = image.getexif()
                image.close()
                file_date = exifdata.get(306)
                file_date = file_date.replace(":", "-").replace(" ", "-")
                file_ending = re.match(FILTER0, f, re.IGNORECASE).group(0)
                new_file_name = file_date + "-" + file_ending
                new_file_name_path = os.path.join(SEARCH_PATH,new_file_name)
                os.rename(file_name,new_file_name_path)
                print("Done. Old file name:", f, " => a new one: ", new_file_name)
            except Exception as e:
                print("******** ERROR in file ", f, " => ", e)

if __name__ == '__main__':
    begin()