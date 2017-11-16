# fontname.py

## About

`fontname.py` is a `.ttf` and `.otf` font renaming script that is developed in Python.  It supports font renaming with current versions of the Python 2 and Python 3 interpreters.

## Dependency
- [fonttools](https://github.com/fonttools/fonttools) Python library

Install with:

```
pip install fonttools
```

## Usage

The script usage is as follows:

```
$ python fontname.py [NEW FONT FAMILY NAME] [FONT PATH 1] <FONT PATH ...>
```

It updates the OpenType name tables nameID 1, 4, and 6 with appropriately formatted font names using the font variant already defined in the font file and the new font family name defined by the user as the first command line argument.  You can include any number of subsequent font file paths on the command line.  The variant type will be detected in the OpenType tables of the font(s) on the filepaths that are passed as arguments on the command line and will be used to create new name strings in the OpenType tables.

### Examples

```
$ python fontname.py "Hack DEV" Hack-Regular.ttf
```

![fscw-hack](https://user-images.githubusercontent.com/4249591/32151555-2a456982-bcf4-11e7-8ec8-57f8dbbd40a4.png)


```
$ python fontname.py "Source Code Pro DEV" SourceCodePro-Regular.otf
```

![fscw-scp](https://user-images.githubusercontent.com/4249591/32151559-2e58a688-bcf4-11e7-9d39-7c8accdc41a6.png)


```
$ python fontname.py "DejaVu Sans Mono DEV" DejaVuSansMono-Bold.ttf
```

![fscw-djv](https://user-images.githubusercontent.com/4249591/32151564-3414a644-bcf4-11e7-93c3-93bc2bbaebdb.png)

These should all be detected as "different" fonts so that you can install them side-by-side with the pre-modified versions.

**Note**: this re-writes the name tables in the fonts passed as arguments on the command line so make copies first if you intend to maintain the fonts with the former naming scheme.
