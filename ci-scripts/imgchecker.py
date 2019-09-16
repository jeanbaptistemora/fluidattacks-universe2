#!/usr/bin/env python3
"""
Script to check if images inside the repo are properly optimized
in size, extension and dimensions
Author: Oscar Eduardo Prado oprado@fluidattacks.com
Version 1.5
Patch notes 1.5:
- Externalize repetitive Checks
- Using error_print function for custom error msgs
"""
import os
import sys
from print_helper import error_print, print_success
import getchanges
from rules import IMGCHECKS

EXIT_CODE = 0

#Define Rules

print_success("Checking images ...\n")

#All blog entries must have a cover.png file
ARTS = os.popen("find content/blog -mindepth 1 -type d").read()
ARTS = ARTS.split()
for ART in ARTS:
    if not os.path.exists(ART+'/cover.png'):
        message = "All blog entries must have a cover.png file. "\
        "If you already have a cover image, please rename it to \"cover\".png."
        error_print(ART, '', message)
        EXIT_CODE = 1

  # Check that cover.png has the proper dimensions
    else:
        OUT = os.popen('identify -format "%wx%h" '+ART+'/cover.png').read()
        if not OUT == "600x280":
            message = "All cover images must have the size 600x280. "\
            "Please modify the cover size."
            error_print(ART, '', message)
            EXIT_CODE = 1

#Check that new images are optimized
print_success("Checking image optimization ...\n")
#get changes in the repo:
CHANGES, EXIT_CODE = getchanges.repochanges(EXIT_CODE)

for FILE in CHANGES:
    if ".png" in FILE:
        COMMAND = 'optipng '+FILE+' |& pcregrep "already"'
        OUT = os.popen("bash -c '{}'".format(COMMAND)).read()
        if not "already optimized" in OUT:
            message = "All png files must be optimized. Run \"optipng\" "\
            "or visit https://compresspng.com/es/ to optimize"
            error_print(FILE, '', message)
            EXIT_CODE = 1
        else:
            print_success(FILE+" is optimized :) \n")

# Repetitive checks from the dictionary
for check, message in IMGCHECKS.items():
    out = os.popen(check).read()
    if out:
        error_print("", out, message)
        exit_code = 1

print_success("\nDone!\n")

sys.exit(EXIT_CODE)
