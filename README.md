# Chromium Language PAK
Fork that allows conversion of language PAK files to Gettext PO and from PO to PAK

## From PAK to Gettext PO or POT
Call `unpack.py` with _directory_ as a po or pot file. Examples:

`python unpack.py en-US.pak en-US.po` creates a PO file
`python unpack.py en-US.pak en-US.pot` creates a POT file

## From Gettext PO to PAK
Simply call `pack.py` with _directory_ as a po file. Example: `python pack.py en-US.po`
