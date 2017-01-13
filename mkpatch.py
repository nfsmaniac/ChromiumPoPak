#!/usr/bin/env python

import sys
import paktools

'''Make a patch'''

def main():
  if len(sys.argv) <= 1:
    print("Usage: {0} [stockPO] [editedPO] [output-patchPO]".format(sys.argv[0]))
    return
  
  originalPo    = sys.argv[1]
  editedPo      = sys.argv[2]
  patchPo       = sys.argv[3]
  
  paktools.CreatePatch(originalPo, editedPo, patchPo)

if __name__ == '__main__':
  main()
