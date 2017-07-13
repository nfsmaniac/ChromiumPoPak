#!/usr/bin/env python
#(c) 2017 nfsmaniac

import os
import sys
#import requests
import batch_unpack
import batch_patch
import batch_pack
    
def main():
  if len(sys.argv) <= 1:
    #print("Usage: {0} [folder with PAK files] [comma separated list of language codes]".format(sys.argv[0]))
    print("Usage: {0} [folder with PAK files] [folder with PO files]".format(sys.argv[0]))
    return
  
  pak_dir      = sys.argv[1]
  #languages    = sys.argv[2]
  po_dir    = sys.argv[2]
  
  for file in os.scandir(pak_dir):              # Cleanup BAK files
    if file.name.endswith(".bak"):
      os.remove(file.path)
  #print("Downloading " + languages + " from Weblate...")
  #
  #os.makedirs("patch", exist_ok=True)
  #lang_list = languages.split(",")
  #
  #for language in lang_list:
  #  response = requests.get(r'https://translations.vivaldi.com/download/vivaldi/vivaldi-browser/' + language, stream=True)  # language
  #  with open(os.path.join("patch", language + '.po'), 'wb') as handle:
  #    for block in response.iter_content(4096):
  #      handle.write(block)
  #  handle.close()
  #  
  #  if not response.ok:                         # something wrong with downloading
  #    print("Failed to download 'https://translations.vivaldi.com/download/vivaldi/vivaldi-browser/" + language + "'.")


  batch_unpack.unpack(pak_dir, "POfiles")
  #batch_patch.patch("patch", "POfiles")
  batch_patch.patch(po_dir, "POfiles")
  batch_pack.pack("POfiles", pak_dir)

  #for f in os.listdir("patch"):         # Cleanup
  #  os.remove(os.path.join("patch", f))
  #os.rmdir("patch")
  for f in os.listdir("POfiles"):       # Cleanup
    os.remove(os.path.join("POfiles", f))
  os.rmdir("POfiles")
  
  print("\n[DONE]")  

if __name__ == '__main__':
  main()
