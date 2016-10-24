# Chromium Language PAK
Fork with focus on Vivaldi browser that allows conversion of language PAK files to Gettext PO and from PO to PAK

## From PAK to Gettext PO
Call `unpack.py` with _directory_ as a po file. Example: `python unpack.py en-US.pak cs.pak en_US.po`

## From Gettext PO to PAK
Simply call `pack.py` with _directory_ as a po file. Example: `python pack.py en_US.po`
