## Changelog

### v2.1.0

- add support for [name table record ID 3](https://docs.microsoft.com/en-us/typography/opentype/spec/name) edits
- add support for setting font version string in [name table record ID 5](https://docs.microsoft.com/en-us/typography/opentype/spec/name)
- add command line option to ignore font subfamily/style for related name table record IDs
- refactor script to use Python's standard command line arguments parser and make it more Pythonic
- add POSIX shell script to create a separate Python virtual environment, in order to avoid messing up the system's Python environment (best practice); works on Linux and MinGW/git bash on Windows
- add Windows batch file to create a separate Python virtual environment, in order to avoid messing up the system's Python environment (best practice)

### v2.0.0

- add CFF table edit writes in CFF (*.otf) fonts: updates fontName, fullName, and familyName CFF fields
- import order formatting with isort

### v1.0.0

- refactor fontname.py script to support Python 3.6+ interpreter only
- drop support for all versions of the Python 2 interpreter
- black source formatting
- add support for [name table record ID 16](https://docs.microsoft.com/en-us/typography/opentype/spec/name) edits

### v0.3.0

- bugfix: corrected PostScript name table record ID 6 suffix write. Previously spaces were not removed from this string value and they should be removed.
- minor update to control flow statement to make it more concise
- source code formatting improvements

### v0.2.0

- removed check mark symbol (U+2713) from print statement - this was leading to Unicode decoding error on Win platform for some users

### v0.1.0

- initial release
