#!/usr/bin/env python

import sys
import paktools

'''Make a patch'''

def main():
  if len(sys.argv) <= 1:
    print("Usage: {0} [stockPO] [editedPO]".format(sys.argv[0]))
    return
  
  originalPo     = sys.argv[1]
  editedPo    = sys.argv[2]
  
  paktools.CreatePatch(originalPo, editedPo)

if __name__ == '__main__':
  main()
