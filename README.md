# fontname.py

## About
A command line tool written in Python for modifying metadata in TrueType (`.ttf`) and OpenType (`.otf`) font files.
The script modifies OpenType name records and, for CFF-based OpenType fonts, also updates the corresponding CFF name fields.
Renaming fonts makes it easy to create custom font variants that can coexist with the original fonts on the same system.

Names are built either by a given family name on the command line or from the name inside the font file.
The subfamily/style is taken from the name inside the font file.


## Features
- Update font family names
- Update version information
- Optionally remove the style/subfamily from generated names
- Update OpenType name table records:
  - ID 1: Font Family
  - ID 3: Unique Font Identifier
  - ID 4: Full Font Name
  - ID 5: Version String
  - ID 6: PostScript Name
  - ID 16: Typographic Family Name
- Update CFF naming information in `.otf` fonts:
  - Family Name
  - Full Name
  - fontNames
- Process multiple font files in a single run

This script updates the OpenType name table records nameID 1, 3, 4, 6, and 16 with appropriately formatted font names using the font style definition in the font and a possible new font family name defined via command line.
The CFF fontName, familyName, and fullName fields are edited in CFF fonts (`.otf`).
You can include any number of subsequent font paths on the command line.
The font style is automatically detected from the OpenType name table of the font files and will be used to create new name strings in the OpenType tables.

Updates the OpenType name table records nameID 5 if a version is specified.

**Note**: rewrites the name tables in the font files passed as arguments on the command line (i.e. writes files in place) so make copies first if you intend to maintain the fonts with the former naming for any reason (though you can simply rewrite with the previous name if you forget...).


## Important Notes
- Font files are modified in-place.
- Create a backup before processing fonts.
- Font's subfamily/style is automatically detected from the font metadata unless `--no-subfamily` is stated.
- The script preserves the font data itself and only updates metadata records.


## Installation - Requirements / Dependencies
- [Python](https://www.python.org) 3.6 or newer.
- [fonttools](https://github.com/fonttools/fonttools) v4.0 or newer. \
  Install via `pip install fonttools` [from PyPi](https://pypi.org/project/fonttools/).
- Alternatively, use the accompanying shell script for Linux/MinGW or batch file for Windows, which create and manage a dedicated Python virtual environment.


## Usage
```
$ ./fontname.sh --help
usage: fontname.sh [-h] [--family FAMILY_NAME] [--version VERSION_STRING] [--no-subfamily] PATH_TO_FONT [PATH_TO_FONT ...]

positional arguments:
  PATH_TO_FONT          path to TTF/OTF font file.

options:
  -h, --help                show this help message and exit
  --family FAMILY_NAME      font family name (quote value if it contains spaces). if not defined, then taken from nameID 1 or 16.
  --version VERSION_STRING  font version (major.minor.patch) for nameID 5.
  --no-subfamily            do not use font subfamily ("style") for building font names.
```


### Examples
Original font:
```
Family (ID 1): Hack
Subfamily (ID 2): Regular
Version (ID 5): 1.0.0
```

Command:
```
$ ./fontname.sh --family "Hack DEV" Hack-Regular.ttf
```

Result:
```
Family (ID 1): Hack DEV
Unique font identifier (ID 3): Hack DEV Regular
Full font name (ID 4): Hack DEV Regular
PostScript Name (ID 6): HackDEV-Regular
```

It should be detected as a "different" font (ID 3) so that you can install them side-by-side with the pre-modified versions.


## License
Released under the [MIT License](LICENSE).
