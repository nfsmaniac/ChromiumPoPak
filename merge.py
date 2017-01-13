#!/usr/bin/env python

import sys
import paktools

'''Merge (update/refill) PO from POT file (e.g. OneSky App removes untranslated msgids)'''

def main():
  if len(sys.argv) <= 1:
    print("Usage: {0} [translatedPO] [en-US.POT] [outputPO]".format(sys.argv[0]))
    return
  
  translatedPo    = sys.argv[1]
  enPot           = sys.argv[2]
  outPo           = sys.argv[3]
    
  paktools.MergePO(translatedPo, enPot, outPo)

if __name__ == '__main__':
  main()
