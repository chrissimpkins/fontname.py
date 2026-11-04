#!/usr/bin/env python
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: nil; py-indent-offset: 4 -*-
### shebang `/usr/bin/env python` due to Python Virtual Environment

"""
fontname.py - A tool to change metadata of TTF/OTF fonts.
Copyright (C) 2017-2021 Christopher Simpkins, 2026 Matthias "Maddes" Bücher
MIT License - https://spdx.org/licenses/MIT.html

It is recommended to run fontname.py via the accompanying shell script or batch file.
These create the correct Python virtual environment.

For command line usage information run:
Linux/MinGW (recommended): fontname.sh --help
Windows (recommended): fontname.bat --help
Linux: python3 fontname.py --help
Windows: py -3 fontname.py --help

Dependencies:
1) Python 3.6+
2) fonttools Python library (https://github.com/fonttools/fonttools)
   - this is automatically handled by the accompanying shell script or batch file
   - or install via `pip3 install fonttools`

OTF/TTF Specs:
https://learn.microsoft.com/en-us/typography/opentype/spec/name
https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6name.html
"""

__version__ = "2.1.0"
__author__ = "Christopher Simpkins"
__license__ = "MIT License"
__copyright__ = "Copyright (C) 2017-2021 Christopher Simpkins, 2026 Matthias \"Maddes\" Bücher"
__homepage__ = "https://github.com/chrissimpkins/fontname.py"
__contact__ = __homepage__

### python standard modules
import argparse
import os
import sys

### fix script name for argparse output
try:
    sys.argv[0] = os.environ["FONTNAME_PATH"]
except KeyError as e:
    pass


### ----------------------------------------
### --- ArgParse Setup
### --- https://docs.python.org/3.6/library/argparse.html
### ----------------------------------------
def createArgParser() -> argparse.ArgumentParser:
    ### Create description
    description = f"\
{format(os.path.basename(sys.argv[0])):s} v{__version__:s}\n\
Licensed under {__license__:s}. This program comes with ABSOLUTELY NO WARRANTY.\n\
{__copyright__:s}\n\
{__homepage__:s}\n\
A tool to change metadata of TTF/OTF fonts."

    ### Build Arg Parser
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
    ### font paths
    parser.add_argument(dest="font_path_list", metavar="PATH_TO_FONT", nargs="+", help="path to TTF/OTF font file.")
    ### font family name
    parser.add_argument("--family", action="store", dest="font_family", metavar="FAMILY_NAME", help="font family name (quote value if it contains spaces). if not defined, then taken from nameID 1 or 16.")
    ### font version
    parser.add_argument("--version", action="store", dest="font_version", metavar="VERSION_STRING", help="font version (major.minor.patch) for nameID 5.")
    ### font name format options
    parser.add_argument("--no-subfamily", action="store_true", dest="ignore_subfamily", help="do not use font subfamily (\"style\") for building font names.")

    return parser
# --- /createArgParser()

### ----------------------------------------
### --- /ArgParse Setup
### ----------------------------------------



### ----------------------------------------
### --- Utilities
### ----------------------------------------

def file_exists(filepath):
    """Tests for existence of a file at the string filepath"""
    return os.path.exists(filepath) and os.path.isfile(filepath)

### ----------------------------------------
### --- /Utilities
### ----------------------------------------



### ----------------------------------------
### --- Main
### ----------------------------------------

def main(args):
    ### pypi modules ("lazy" load to allow calling help without installed extra modules)
    try:
        from fontTools import ttLib
    except Exception as e:
        print(
            f"[fontname.py] ERROR: module fonttools from pypi.org missing.",
            "It is recommended to use the accompanying shell script or batch file to create a separate Python virtual environment.",
            "Otherwise create and activate a virtual environment with module fonttools installed via pip.",
            file=sys.stderr
        )
        print(
            f"[fontname.py] {e}",
            file=sys.stderr
        )
        sys.exit(1)

    ### Iterate through all paths provided on command line
    for font_path in args.font_path_list:
        print(f"[fontname.py] Processing {font_path}...")
        ### test for existence of font file on requested file path
        if not file_exists(font_path):
            print(
                f"[fontname.py] ERROR: the path \"{font_path}\" does not appear to be a valid file path.",
                file=sys.stderr
            )
            sys.exit(1)

        tt = ttLib.TTFont(font_path)
        namerecord_list = tt["name"].names

        ### Determine information from font (family, subfamily, version, etc.)
        font_family = None
        font_subfamily = None
        font_version = None
        #
        found_family = False
        found_subfamily = False
        found_version = False
        for record in namerecord_list:
            if not found_family \
            and ( record.nameID == 1 or record.nameID == 16 ): # Font Family name / Typographic Family name
                print(f"> Family: \"{str(record)}\" (from Name ID {record.nameID})")
                font_family = str(record).strip()
                found_family = True
            elif not found_subfamily \
            and ( record.nameID == 2 or record.nameID == 17 ): # Font Subfamily name / Typographic Subfamily name
                print(f"> Subfamily: \"{str(record)}\" (from Name ID {record.nameID})")
                font_subfamily = str(record).strip()
                found_subfamily = True
            elif not found_version \
            and ( record.nameID == 5 ): # Version string
                print(f"> Version: \"{str(record)}\" (from Name ID {record.nameID})")
                font_version = str(record).replace("Version ","").strip()
                found_version = True
            else:
                continue # next record
            #
            if found_family \
            and found_subfamily \
            and found_version:
                break # leave name record loop

        ### If subfamily ("style") was found not in the OpenType tables of the font, then check wether to skip the font
        if not font_subfamily:
            print(
                f"[fontname.py] ERROR: Unable to detect the font subfamily from the OpenType name table in \"{font_path}\".",
                file=sys.stderr
            )
            if not args.ignore_subfamily:
                print(
                    "[fontname.py] ERROR: Unable to process this font.",
                    file=sys.stderr
                )
            continue # next font

        ### Prepare new base values for name record entries
        if args.font_family and args.font_family.strip():
            font_family = args.font_family.strip()
        if not font_family:
            print(
                f"[fontname.py] ERROR: Unable to detect the font family from the OpenType name table in \"{font_path}\".",
                file=sys.stderr
            )
            continue # next font
        #
        if args.font_version and args.font_version.strip():
            font_version = args.font_version.strip()

        ### 1/16: Font Family name
        nameID1_string = font_family
        nameID16_string = font_family
        ### 3: Unique font identifier / Unique subfamily identification
        nameID3_string = f"{font_family}{f' {font_subfamily}' if not args.ignore_subfamily else ''}"
        ### 4: Full font name
        nameID4_string = f"{font_family}{f' {font_subfamily}' if not args.ignore_subfamily else ''}"
        ### 5: Version string
        nameID5_string = f"Version {font_version}" if font_version else ""

        ### PostScript name
        ### - no spaces allowed in family name or the PostScript suffix. should be dash delimited
        postscript_font_family = font_family.replace(" ", "")
        postscript_font_subfamily = font_subfamily.replace(" ", "")
        nameID6_string = f"{postscript_font_family}{f'-{postscript_font_subfamily}' if not args.ignore_subfamily else ''}"

        ### Modify the opentype table data in memory with updated values
        for record in namerecord_list:
            if record.nameID == 1: # Font Family name
                record.string = nameID1_string
                print(f"Setting Name: \"{str(record)}\" (in Name ID {record.nameID}/Platform ID {record.platformID})")
            elif record.nameID == 3: # Unique font identifier / Unique subfamily identification
                record.string = nameID3_string
                print(f"Setting Name: \"{str(record)}\" (in Name ID {record.nameID}/Platform ID {record.platformID})")
            elif record.nameID == 4: # Full font name
                record.string = nameID4_string
                print(f"Setting Name: \"{str(record)}\" (in Name ID {record.nameID}/Platform ID {record.platformID})")
            elif record.nameID == 5: # Version string
                record.string = nameID5_string
                print(f"Setting Version: \"{str(record)}\" (in Name ID {record.nameID}/Platform ID {record.platformID})")
            elif record.nameID == 6: # PostScript name
                record.string = nameID6_string
                print(f"Setting Name: \"{str(record)}\" (in Name ID {record.nameID}/Platform ID {record.platformID})")
            elif record.nameID == 16: # Typographic Family name
                record.string = nameID16_string
                print(f"Setting Name: \"{str(record)}\" (in Name ID {record.nameID}/Platform ID {record.platformID})")

        ### CFF table naming for CFF fonts (only)
        if "CFF " in tt:
            try:
                cff = tt["CFF "]
                cff.cff[0].FamilyName = nameID1_string
                cff.cff[0].FullName = nameID4_string
                cff.cff.fontNames = [nameID6_string]
            except Exception as e:
                print(
                    f"[fontname.py] ERROR: unable to write new names to CFF table: {e}",
                    file=sys.stderr
                )

        ### Write changes to the font file
        try:
            tt.save(font_path)
            print(f"[fontname.py] Success: Updated \"{font_path}\"")
        except Exception as e:
            print(
                f"[fontname.py] ERROR: unable to write new name to OpenType name table for \"{font_path}\".",
                file=sys.stderr
            )
            print(
                f"[fontname.py] {e}",
                file=sys.stderr
            )
            sys.exit(1)


if __name__ == "__main__":
    ### Parse arguments from the command line
    parser = createArgParser()
    arguments = parser.parse_args()

    print(parser.description)
    main(arguments)

    sys.exit(0)
