#!/usr/bin/env python

import sys
import paktools

'''Packs a directory into a .pak file'''

def main():
  if len(sys.argv) <= 1:
    print("Usage: {0} <directory> [file]".format(sys.argv[0])
    return
  
  directory = sys.argv[1]
  file      = sys.argv[2] if len(sys.argv) >= 3 else "{0}.pak".format(directory.replace(".po", ""))
  
  paktools.PackDirectoryIntoFile(directory, file)

if __name__ == '__main__':
  main()
