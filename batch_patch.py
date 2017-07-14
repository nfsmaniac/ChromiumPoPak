#!/usr/bin/env python

import os
import sys
import fnmatch
import paktools

'''Batch migrate translation from patch'''

def main():
  if len(sys.argv) <= 1:
    print("Usage: {0} [input directory] [output directory]".format(sys.argv[0]))
    return
  
  in_dir      = sys.argv[1]
  out_dir     = sys.argv[2]  

  patch(in_dir, out_dir)

def patch(in_dir, out_dir):
  if len(fnmatch.filter(os.listdir(in_dir), '*.po')) > 0:
    files_count = len(fnmatch.filter(os.listdir(in_dir), '*.po'))
    current_file = 0
    for file in os.listdir(out_dir):                    # Cleanup
      if ".bak" in file:
        os.remove(file)  
    for file in os.listdir(in_dir):
      if file.endswith(".po"):
      
        patchfile = os.path.join(in_dir, file)
        POfile = os.path.join(out_dir, file.replace("_patch", ""))

        print("[{0} of {1} done]".format(current_file, files_count))
        paktools.ApplyPatch(POfile, patchfile)
        current_file += 1
    print("\n[Patching complete!]")

if __name__ == '__main__':
  main()
