#!/usr/bin/env python3
"""
Script to check if images inside the repo are properly optimized
in size, extension and dimensions
Author: Oscar Eduardo Prado oprado@fluidattacks.com
Version 1.4
Patch notes 1.4:
- Externalized repo changes in a different function
"""
import os
import sys
import print_helper
import getchanges

EXIT_CODE = 0

#Define Rules

print_helper.print_success("Checking images ...\n")

#Image size must not exceed 300kb
OUT = os.popen("find content/ -iname '*.png' -size +300k").read()
if OUT:
    print_helper.print_failure("Issue found in the following file(s):\n")
    print_helper.print_failure(OUT)
    print_helper.print_warning("Image file size must not exceed 300Kb. "\
                               "Please correct the file(s) and try again\n\n")
    EXIT_CODE = 1

#Only valid image extension is PNG
OUT = os.popen("find . -iname '*.jpeg' -o -iname '*.jpg' \
                -o -iname '*.bmp' -o -iname '*.tiff'").read()
if OUT:
    print_helper.print_failure("Issue found in the following file(s):\n")
    print_helper.print_failure(OUT)
    print_helper.print_warning("The only allowed extension for images is PNG. "\
                             "Please correct the file(s) and try again\n\n")
    EXIT_CODE = 1

#All blog entries must have a cover.png file
ARTS = os.popen("find content/blog -mindepth 1 -type d").read()
ARTS = ARTS.split()
for ART in ARTS:
    if not os.path.exists(ART+'/cover.png'):
        print_helper.print_failure("Issue found in the following article(s):\n")
        print_helper.print_failure(ART+"\n")
        print_helper.print_warning("All blog entries must have a cover.png file. "\
                                   "If you already have a cover image, "  \
                                   "please rename it to cover.png. \n\n")

        EXIT_CODE = 1
  # Check that cover.png has the proper dimensions
    else:
        OUT = os.popen('identify -format "%wx%h" '+ART+'/cover.png').read()
        if not OUT == "600x280":
            print_helper.print_failure("Issue found in the following article(s):\n")
            print_helper.print_failure(ART+"\n")
            print_helper.print_warning("All cover images must have the size 600x280. "\
                                       "Please modify the cover size. \n\n")

            EXIT_CODE = 1

#Check that new images are optimized
print_helper.print_warning("Checking image optimization ...\n")
#get changes in the repo:
CHANGES, EXIT_CODE = getchanges.repochanges(EXIT_CODE)

for FILE in CHANGES:
    if ".png" in FILE:
        COMMAND = 'optipng '+FILE+' |& pcregrep "already"'
        OUT = os.popen("bash -c '{}'".format(COMMAND)).read()
        if not "already optimized" in OUT:
            print_helper.print_failure("Issue found in the following image(s):\n")
            print_helper.print_failure(FILE+"\n")
            print_helper.print_warning("All png files must be optimized. "\
                                       "Run \"optipng\" or visit https://compresspng.com/es/"\
                                      " to optimize. \n\n")
            EXIT_CODE = 1
        else:
            print_helper.print_success(FILE+" is optimized :) \n")

print_helper.print_success("\nDone!\n")

sys.exit(EXIT_CODE)
