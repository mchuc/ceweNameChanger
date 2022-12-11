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
    import datetime
except:
    print("You have to install Pillow: python -m pip install Pillow")
    print("Exiting...")
    exit(0)

SEARCH_PATH = os.path.dirname(__file__)
FILTER0 = r"^.*(\.jpg|\.png|\.jpeg)$"  # just only JPG ang PNG images
FILTER1 = r"^[0-9]{4}\-[0-9]{2}\-[0-9]{2}.*(\.jpg|\.png|\.jpeg)$"  # correctName
FILTER2 = r"^([^0-9.]*)([0-9]{8})"


def file_list(path):
    output = []
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            if re.match(FILTER0, file, re.MULTILINE | re.IGNORECASE):
                if re.match(FILTER1, file, re.MULTILINE | re.IGNORECASE):
                    print("I'm skiping correct fileneme: ", file)
                else:
                    print("Adding file: ", file)
                    output.append(file)
            else:
                print("I'm skiping file: ", file, " it's not JPEG or PNG")
    return output


def rename_file(path, from_, to_):
    try:
        file_1 = os.path.join(path, from_)
        file_2 = os.path.join(path, to_)
        os.rename(file_1, file_2)
    except Exception as e:
        print("**** ERROR when changing filename: ", file_1, " => ", file_2)
        return False
    return True


def begin():
    print("*****************************************")
    print("ceweNameChanger")
    print("(C) Marcin Chuć 2022")
    print("*****************************************")

    print("I'm looking in the directory ", SEARCH_PATH, " ...")
    files = file_list(SEARCH_PATH)
    if len(files)>0:
        print("Working... (not to hard)...")
    else:
        print("Oh, nothing to do! Bye!")
    for f in files:
        file_name = os.path.join(SEARCH_PATH, f)
        if os.path.isfile(file_name):
            try:
                image = Image.open(file_name)
                exifdata = image.getexif()
                image.close()
                file_ending = re.match(FILTER0, f, re.IGNORECASE).group(0)
                file_date = exifdata.get(306)
                file_date = file_date.replace(":", "-").replace(" ", "-")
                new_file_name = file_date + "-" + file_ending
                if rename_file(SEARCH_PATH, f, new_file_name):
                    print("Job ready. Old file name:", f, " => a new one: ", new_file_name)
                else:
                    print("Change this filename manually: ", f)
            except Exception as e:
                '''
                Well, here we go... trouble in heaven
                '''
                print("")
                print("")
                print("******** ERROR in file ", f, " => ", e)
                print("Data from EXIF: ", exifdata)
                answer = -1

                while (answer != 1) and (answer != 0):
                    print("Do you want to give your own name to this file? 1: Yes, 0: No")
                    try:
                        answer = int(input())
                    except:
                        answer =-1

                if answer == 1:
                    file_name_1 = datetime.datetime.fromtimestamp(os.path.getctime(file_name)).strftime("%Y-%m-%d-") + f
                    file_name_2 = None
                    print("My suggested file name:")
                    print("1: ", file_name_1)

                    '''
                    look for the date in the file name - usually 8 consecutive digits
                    '''
                    if re.match(FILTER2, f, re.IGNORECASE):
                        file_name_2 = re.match(FILTER2, f, re.IGNORECASE).group(2)
                        file_name_2 = file_name_2[0:4]+"-"+file_name_2[4:6]+"-"+file_name_2[6:8]+"-"+f
                        print("2: ", file_name_2)

                    print("3: Your own filename + orginal name ending, ie: XXXX-XX-XX-",f)

                    answer = -1
                    while (answer !=1) and (answer!=2) and (answer!=3):
                        try:
                            print("What do You choose?:")
                            answer=int(input())
                        except:
                            answer=-1

                        if answer==1:
                            if rename_file(SEARCH_PATH, f, file_name_1):
                                print("Job ready. Old file name:", f, " => a new one: ", file_name_1)
                            else:
                                print("Change this filename manually: ", f)

                        elif answer==2:
                            if file_name_2 is not None:
                                if rename_file(SEARCH_PATH,f,file_name_2):
                                    print("Job ready. Old file name:", f, " => a new one: ", file_name_2)
                                else:
                                    print("Change this filename manually: ", f)
                            else:
                                print("Ups. This option is inactive now")
                                answer=-1
                        elif answer==3:
                            print("Input new own name for file ",f)
                            try:
                                file_name_3 = str(input())
                            except:
                                file_name_3=""
                                answer=-1

                            if len(file_name_3)>0:
                                file_name_3 = file_name_3+"-"+f
                                if rename_file(SEARCH_PATH,f,file_name_3):
                                    print("Job ready. Old file name:", f, " => a new one: ", file_name_3)
                                else:
                                    print("Change this filename manually: ", f)

                        else: #wrong answer, not 1-3
                            answer=-1





if __name__ == '__main__':
    begin()
