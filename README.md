# Chromium Language PAK
Fork with focus on Vivaldi browser that allows conversion of language PAK files to Gettext PO and from PO to PAK

## Requirments
* Python 3 (tested on 3.5)
  * **polib** module `pip install polib`
  
## Guide

### From PAK to Gettext PO
Call `unpack.py` with _directory_ as a po file. Example: `python unpack.py en-US.pak cs.pak cs.po`

### From Gettext PO to PAK
Simply call `pack.py` with _directory_ as a po file. Example: `python pack.py en_US.po`

### Batch conversion
Call `batch-unpack.py` with _in_dir_ as input folder containing multiple PAK files and _out_dir_ as output folder where PO files will be saved. You don't need to create the output directory first. Also if you leave there some PO file, the script will make a backup first. Example: `python batch-unpack.py Locales converted`
