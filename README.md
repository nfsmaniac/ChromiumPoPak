# Vivaldi Translation Team PAK–PO converter
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

Call `batch-pack.py` with _in_dir_ as input folder containing multiple PO files and _out_dir_ as output folder where PAK files will be saved. You don't need to create the output directory first. Also if you leave there some PAK file, the script will make a backup first. Example: `python batch-pack.py converted Locales`

### Create & Apply patch
For easy migration of translation between Vivaldi browser releases, it is needed to create a patch. Call `mkpatch.py` with _originalPO_ as stock PO file generated from official PAK file and _editedPO_ as changed PO file by you.
Example: `python mkpatch.py cs.po cs_edit.po`

To apply a patch, call `apply-patch.py` with _originalPO_ as stock PO file generated from official PAK file and _patchPO_ as a patch file generated in previous step.
Example: `python apply-patch.py cs.po cs_patch.po`
