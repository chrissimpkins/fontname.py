# fontname.py

## About

`fontname.py` is a `.ttf` and `.otf` font renaming script that is developed in Python.  It supports font renaming with the Python 3.6+ interpreter.

## Dependency
- [fonttools](https://github.com/fonttools/fonttools) Python library (requires v4.0.0+)

Install with:

```
pip3 install fonttools
```

## Usage

The script usage is as follows:

```
$ python3 fontname.py [NEW FONT FAMILY NAME] [FONT PATH 1] <FONT PATH ...>
```

This script updates the OpenType name table records nameID 1, 4, 6, and 16 with appropriately formatted font names using the font style definition in the font and the new font family name defined by the user as the first command line argument.  The CFF fontName, familyName, and fullName fields are edited in CFF fonts (*.otf).  You can include any number of subsequent font paths on the command line.  The style will be detected in the OpenType tables of the fonts filepath arguments and will be used to create new name strings in the OpenType tables.

**Note**: this re-writes the name tables in the fonts passed as arguments on the command line (i.e. writes files in place) so make copies first if you intend to maintain the fonts with the former naming for any reason (though you can simply re-write with the previous name if you forget...).

### Examples

```
$ python3 fontname.py "Hack DEV" Hack-Regular.ttf
```

![fscw-hack](https://user-images.githubusercontent.com/4249591/32151555-2a456982-bcf4-11e7-8ec8-57f8dbbd40a4.png)


```
$ python3 fontname.py "Source Code Pro DEV" SourceCodePro-Regular.otf
```

![fscw-scp](https://user-images.githubusercontent.com/4249591/32151559-2e58a688-bcf4-11e7-9d39-7c8accdc41a6.png)


```
$ python3 fontname.py "DejaVu Sans Mono DEV" DejaVuSansMono-Bold.ttf
```

![fscw-djv](https://user-images.githubusercontent.com/4249591/32151564-3414a644-bcf4-11e7-93c3-93bc2bbaebdb.png)

These should all be detected as "different" fonts so that you can install them side-by-side with the pre-modified versions.

## License

[MIT License](LICENSE)