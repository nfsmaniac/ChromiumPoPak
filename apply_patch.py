#!/usr/bin/env python

import sys
import paktools

'''Apply a patch'''

def main():
  if len(sys.argv) <= 1:
    print("Usage: {0} [new-originalPO] [patchingPO]".format(sys.argv[0]))
    return
  
  originalPo    = sys.argv[1]
  patchPo       = sys.argv[2]
  
  paktools.ApplyPatch(originalPo, patchPo)

if __name__ == '__main__':
  main()
