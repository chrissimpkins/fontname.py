#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ==========================================================================
# fontname.py
# Copyright 2017 Christopher Simpkins
# MIT License
#
# Dependencies:
#   1) fonttools Python library (https://github.com/fonttools/fonttools)
#         - install with `pip install fonttools`
#
# Usage:
#   python fontname.py [FONT FAMILY NAME] [FONT PATH 1] <FONT PATH ...>
#
# Notes:
#   Use quotes around font family name arguments that included spaces
# ===========================================================================

from __future__ import unicode_literals

import sys
import os

from fontTools import ttLib
from fontTools.misc.py23 import tounicode, unicode

def main(argv):
    # command argument tests
    print(" ")
    if len(argv) < 2:
        sys.stderr.write("[fontname.py] ERROR: you did not include enough arguments to the script." + os.linesep)
        sys.stderr.write("Usage: python fontname.py [FONT FAMILY NAME] [FONT PATH 1] <FONT PATH ...>" + os.linesep)
        sys.exit(1)

    # begin parsing command line arguments
    try:
        font_name = tounicode(argv[0])  # the first argument is the new typeface name
    except UnicodeDecodeError as e:
        sys.stderr.write("[fontname.py] ERROR: Unable to convert argument to Unicode. " + unicode(e) + os.linesep)
        sys.exit(1)

    font_path_list = argv[1:]  # all remaining arguments on command line are file paths to fonts

    # iterate through all paths provided on command line and rename to `font_name` defined by user
    for font_path in font_path_list:
        # test for existence of font file on requested file path
        if file_exists(font_path):
            pass  # do nothing, it is there
        else:
            sys.stderr.write("[fontname.py] ERROR: the path '" + font_path +"' does not appear to be a valid file path." + os.linesep)
            sys.exit(1)

        tt = ttLib.TTFont(font_path)
        namerecord_list = tt['name'].names
        variant = ""

        # determine font variant for this file path from name record nameID 2
        for record in namerecord_list:
            if record.nameID == 2:
                variant = record.toUnicode()  # cast to str type in Py 3, unicode type in Py 2
                break

        # test that a variant name was found in the OpenType tables of the font
        if len(variant) == 0:
            sys.stderr.write("[fontname.py] Unable to detect the font variant from the OpenType name table in '" + font_path + "'." + os.linesep)
            sys.stderr.write("Unable to complete execution of the script.")
            sys.exit(1)
        else:
            nospaces_font_name = font_name.replace(" ", "")   # used for the Postscript name in the name table (no spaces allowed)

            nameID1_string = font_name                            # font family name
            nameID4_string = font_name + " " + variant            # full font name
            nameID6_string = nospaces_font_name + "-" + variant   # Postscript name (no spaces allowed, dash delimited)

            # modify the opentype table data in memory with updated values
            for record in namerecord_list:
                if record.nameID == 1:
                    record.string = nameID1_string
                elif record.nameID == 4:
                    record.string = nameID4_string
                elif record.nameID == 6:
                    record.string = nameID6_string

        # write changes to the font file
        try:
            tt.save(font_path)
            print("[✓] Updated '" + font_path + "' with the name '" + nameID4_string + "'")
        except Exception as e:
            sys.stderr.write("[fontname.py] ERROR: unable to write new name to OpenType tables for '" + font_path + "'." + os.linesep)
            sys.stderr.write(unicode(e))
            sys.exit(1)



# Utilities

def file_exists(filepath):
    """Tests for existence of a file on the string filepath"""
    if os.path.exists(filepath) and os.path.isfile(filepath):  # test that exists and is a file
        return True
    else:
        return False

if __name__ == '__main__':
    main(sys.argv[1:])
