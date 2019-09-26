#!/usr/bin/env python3

"""
This file contains a set of rules for web repo content,
blog articles and overall files rules (Da Rules)
Author: Oscar Eduardo Prado oprado@fluidattacks.com
"""

#Rules for all asciidoc files
CONTENTRULES = {
    # Check use of incorrect names to address the company
    "pcregrep -on 'Fluid(?! Attacks)|Fluidsignal Group"
    "|fluidsignal(?!\\.formstack)|\\ fluid[)}\\ \\]] |FLUID\\W|FLUIDAttacks'":
    "The only accepted name is Fluid Attacks. ",

    # Check blank spaces after headers
    "pcregrep -Mrn '^=.*.[A-Z].*.*\\n.*[A-Z]'":
    "Leave a blank space after a header. ",

    # Check that the references are numbered
    "pcregrep -Mnr '^== Referenc.*.*\\n.*\\n[A-Za-z]'":
    "References must be numbered. ",

    # Check the titles of the images are well placed
    "pcregrep -Mnr 'image::?.*\\n\\.[a-zA-Z]'":
    "Image captions are placed before the image, not after. ",

    # Check that slugs have under 44 characters
    "pcregrep -nr  '^:slug: .{44,}'":
    "The \"slug\" can have 43 characters maximum. ",

    # Check that 4 '-' delimit the code block, not more, not less
    "pcregrep -nr '^-{5,}' ":
    "Code blocks must be delimited by exactly four hyphens '-'. ",

    # Check that the start attribute is never used
    "pcregrep -nr '\\[start'":
    "Use a plus sing '+' to concatenate the content that breaks the numbering "
    "instead of the [start] attribute",

    # Check that the slug ends in a '/'
    "pcregrep -nr '^:slug:.*[a-z]$'":
    "The \"slug\" must end in '/'. ",

    # Check alternative text in images
    "pcregrep -Mnr '^image\\:\\:?.*\\[\\]' ":
    "Images must have an alt description.",

    # Check double quotes are not used in the title
    "pcregrep -nr '^={1,6}\\s.*\"' ":
    "Do not use double quotes \" in titles. ",

    # Check that code does not follow inmmediatly after a paragraph
    "pcregrep -Mnr '^[a-zA-Z0-9].*\n.*\\[source' ":
    "Source code must be separated from a paragraph using a plus sign '+'. ",

    #Titles must not exceed 60 characters
    "pcregrep -o '^=\\s.{60,}' ":
    "Titles must not exceed 60 characters. ",

    # Check that every .adoc has keywords defined
    "pcregrep -L '^:keywords:' ":
    "The attribute \"keywords\" must be defined.",

    # Check that the every .adoc has description defined
    "pcregrep -L '^:description:' ":
    "The attribute \"description\" must be defined. ",

    # Check all Asciidoc metadata are lowercase
    "pcregrep -nr '^:[A-Z]' ":
    "All metadata attributes in asciidoc files must be lowercase.",

    # Check that titles and subtitles don't contain monospaces
    "pcregrep -nr '^=.*\\+.+\\+.*'":
    "Titles and subtitles must not contain monospaces.",

    # Check that the meta description is in [250-300] char range
    "pcregrep -no '(?<=^:description: ).{306,}$|(?<=^:description:).{0,249}$'":
    "Descriptions must be in the [250-300] characters range.",

    #Check that local URLs always uses relative paths:
    "pcregrep -n 'link:http(s)?://fluidattacks.com/web' ":
    "Local URLs must use relative paths. ",

    #Only autonomicmind.com is allowed
    "pcregrep -o '(autonomicmind.co(?!m))' ":
    "The only allowed domain is autonomicmind.com. ",

    # Check that caption is not manually placed
    "pcregrep -ni '^\\.image\\s\\d|^\\.table\\s\\d|^\\.figure\\s\\d\' ":
    "Captions must not contain \"Image #\", \"Figure #\" or \"Table #\".\n\n"
}

#Rules for Blog articles
ARTRULES = {
    #Check that every article in blog has a valid title lenght
    "pcregrep -no '(?<=^= ).{37,}'":
    "The title lenght exceeds 35 characters.",

    #Check that every article in blog has a subtitle defined
    "pcregrep -L '^:subtitle:'":
    "The attributte \"subtitle\" must be defined. ",

    #Check that every article in blog has a valid subtitle lenght
    "pcregrep -o '(?<=^:subtitle: ).{56,}' ":
    "The subtitle lenght exceeds 55 characters. ",

    # Check that articles have alt description for their featured images
    "pcregrep -L  '^:alt:' ":
    "The articles must have the \"alt\" metadata set "
    "for their representative image."
}

#General Checks
GENCHECKS = {
    # Check there are not any articles with the .asc extension
    "find content -iname '*.asc' | grep -E './.*'":
    "Extension \".asc\" is no longer supported. ",

    # Check that names do not have underscore
    "find content -iname '*_*' | grep -E './.*'":
    "Use hyphen '-' instead of underscore '_' for filenames. ",

    # Check no uppercase characters are used in the filenames
    "find content | grep -E '.*[A-Z].*'":
    "Filenames must always be lowercase.",

    #Check that there are no spaces in filenames
    "find content -iname '* *' | grep -E './.*'":
    "Filenames must not have spaces in them, use hyphen \"-\" instead. "
}

#Images Checks
IMGCHECKS = {
    #Image size must not exceed 300kb
    "find content/ -iname '*.png' -size +300k":
    "Image file size must not exceed 300Kb. ",

    #Only valid image extension is PNG
    "find . -iname '*.jpeg' -o -iname '*.jpg' "
    "-o -iname '*.bmp' -o -iname '*.tiff'":
    "The only allowed extension for images is PNG. ",
}
