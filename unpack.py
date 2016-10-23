#!/usr/bin/env python

import sys
import re
import paktools

'''Unpacks a .pak file into a directory'''

def main():
  if len(sys.argv) <= 1:
    print("Usage: %s <file> [directory]" % sys.argv[0])
    return
  
  file      = sys.argv[1]
  file2     = sys.argv[2]
  directory = sys.argv[3] if len(sys.argv) >= 3 else re.sub("\.pak$", "", file)
  
  paktools.UnpackFileIntoDirectory(file, file2, directory)

if __name__ == '__main__':
  main()
