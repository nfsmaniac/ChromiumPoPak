#!/usr/bin/env python

import os
import sys
import fnmatch
import paktools

'''Batch convert all gettext PO files in a directory to PAK'''

def main():
  if len(sys.argv) <= 1:
    print("Usage: {0} [input directory] [output directory]".format(sys.argv[0]))
    return
  
  in_dir      = sys.argv[1]
  out_dir     = sys.argv[2]
  
  backup_done = False  

  if len(fnmatch.filter(os.listdir(in_dir), '*.po')) > 0:
    files_count = len(fnmatch.filter(os.listdir(in_dir), '*.po'))
    current_file = 0  
    for file in os.listdir(in_dir):
      if file.endswith(".po"):
        if not os.path.exists(out_dir):
          os.makedirs(out_dir)
          backup_done = True
        if os.path.exists(out_dir) == True and backup_done == False:
          print("WARNING: Directory exists! Don't worry, backing up existing PO files.")
          for POfile in os.listdir(out_dir):
            os.rename(os.path.join(out_dir, POfile), os.path.join(out_dir, POfile.replace(".pak", ".bak")))
          backup_done = True
      
        POfile = os.path.join(in_dir, file)
        PAKfile = os.path.join(out_dir, file.replace(".po", ".pak"))

        print("[{0} of {1} done]".format(current_file, files_count))
        paktools.PackDirectoryIntoFile(POfile, PAKfile)
        current_file += 1
    print("\n[Conversion complete!]")
  else:
    print("ERROR: No file 'en-US.pak' found! Check the input directory or make sure that 'en-US.pak' exists.")

if __name__ == '__main__':
  main()
