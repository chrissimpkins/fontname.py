#!/usr/bin/env python3

# ==========================================================================
# fontname.py
# Copyright 2019 Christopher Simpkins
# MIT License
#
# Dependencies:
#   1) Python 3.6+ interpreter
#   2) fonttools Python library (https://github.com/fonttools/fonttools)
#         - install with `pip3 install fonttools`
#
# Usage:
#   python3 fontname.py [FONT FAMILY NAME] [FONT PATH 1] <FONT PATH ...> [--style FONT_STYLE] [--weight FONT_WEIGHT]
#
# Notes:
#   Use quotes around font family name arguments that include spaces
# ===========================================================================

import os
import sys
import argparse

from fontTools import ttLib

def main(argv):
    # command argument tests
    print(" ")
    parser = argparse.ArgumentParser(description='Rename font files with specified font family name, style, and weight.')
    parser.add_argument('font_name', type=str, help='the new typeface name')
    parser.add_argument('font_paths', nargs='+', type=str, help='list of font file paths')
    parser.add_argument('--style', type=str, help='the style of the font')
    parser.add_argument('--weight', type=str, help='the weight of the font')
    parser.add_argument('--force-style', type=str, help='force the style even if already determined')
    parser.add_argument('--force-weight', type=str, help='force the weight even if already determined')
    args = parser.parse_args(argv)

    font_name = args.font_name
    font_path_list = args.font_paths

    for font_path in font_path_list:
        if not file_exists(font_path):
            sys.stderr.write(
                f"[fontname.py] ERROR: the path '{font_path}' does not appear to be a valid file path.{os.linesep}"
            )
            sys.exit(1)

        tt = ttLib.TTFont(font_path)

        style = args.style if args.style else ""
        weight = args.weight if args.weight else ""
        force_style = args.force_style if args.force_style else ""  # Initialize as empty string
        force_weight = args.force_weight if args.force_weight else ""  # Initialize as empty string

        # Determine font style and weight from specified arguments
        if not style and not weight:
            sys.stderr.write(
                f"[fontname.py] ERROR: Both style and weight must be specified.{os.linesep}"
            )
            sys.exit(1)

        # Update 'name' table with the specified style and weight
        for record in tt["name"].names:
            if record.nameID == 2:
                if force_style:
                    style = force_style
                if force_weight:
                    weight = force_weight
                record.string = f"{weight} {style}"

        postscript_font_name = font_name.replace(" ", "")
        nameID1_string = font_name
        nameID16_string = font_name
        nameID4_string = f"{font_name} {style} {weight}"
        nameID6_string = f"{postscript_font_name}-{style.replace(' ', '')}-{weight.replace(' ', '')}"

        for record in tt["name"].names:
            if record.nameID == 1:
                record.string = nameID1_string
            elif record.nameID == 4:
                record.string = nameID4_string
            elif record.nameID == 6:
                record.string = nameID6_string
            elif record.nameID == 16:
                record.string = nameID16_string

        if "CFF " in tt:
            try:
                cff = tt["CFF "]
                cff.cff[0].FamilyName = nameID1_string
                cff.cff[0].FullName = nameID4_string
                cff.cff.fontNames = [nameID6_string]
            except Exception as e:
                sys.stderr.write(
                    f"[fontname.py] ERROR: unable to write new names to CFF table: {e}"
                )

        try:
            tt.save(font_path)
            print(f"[OK] Updated '{font_path}' with the name '{nameID4_string}', style '{style}', and weight '{weight}'")
        except Exception as e:
            sys.stderr.write(
                f"[fontname.py] ERROR: unable to write new name to OpenType name table for '{font_path}'. {os.linesep}"
            )
            sys.stderr.write(f"{e}{os.linesep}")
            sys.exit(1)

# Utilities


def file_exists(filepath):
    """Tests for existence of a file on the string filepath"""
    return os.path.exists(filepath) and os.path.isfile(filepath)


def weight_to_weightclass(weight):
    """Converts font weight name to the OS/2 usWeightClass value"""
    weight_mapping = {
        "Thin": 100,
        "ExtraLight": 200,
        "Light": 300,
        "Regular": 400,
        "Medium": 500,
        "SemiBold": 600,
        "Bold": 700,
        "ExtraBold": 800,
        "Black": 900,
    }
    return weight_mapping.get(weight, 400)  # Default to Regular if weight is not recognized


if __name__ == "__main__":
    main(sys.argv[1:])