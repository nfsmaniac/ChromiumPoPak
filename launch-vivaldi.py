#!/usr/bin/env python

# Copyright (c) 2017, nfsmaniac
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * All advertising materials mentioning features or use of this software
#       must display the following acknowledgement:
#       This product includes software developed by the Vivaldi Czech Translation team.
#     * Neither the name of the Vivaldi Czech Translation team nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import sys
import requests
import pefile
import subprocess
import zipfile
import batch_unpack
import batch_patch
import batch_pack
    
def main():
  pe = pefile.PE(r'vivaldi.exe')
  FileVersionLS    = pe.VS_FIXEDFILEINFO.FileVersionLS
  FileVersionMS    = pe.VS_FIXEDFILEINFO.FileVersionMS
  vivaldi_ver = str((FileVersionMS >> 16, FileVersionMS & 0xFFFF, FileVersionLS >> 16, FileVersionLS & 0xFFFF)).replace(", ", ".").replace("(", "").replace(")", "")

  Locales_dir = os.path.join(vivaldi_ver, "Locales")
  
  if os.path.isfile(os.path.join(Locales_dir, "patch.done")) == True:
    subprocess.Popen("vivaldi.exe")
    sys.exit(0)
  else:
    for file in os.scandir(Locales_dir):              # Cleanup BAK files (for case of manual 'patch.done' file deletion)
      if file.name.endswith(".bak"):
        os.remove(file.path)
    print("Downloading patch repository")  
    response = requests.get(r'http://vivaldi.ml/download/vivaldi-patches-for-launcher/?wpdmdl=102', stream=True)  # Download patch repository
    with open('patch.zip', 'wb') as handle:
      for block in response.iter_content(4096):
        handle.write(block)
    handle.close()
    
    if not response.ok:                               # something wrong with downloading
      subprocess.Popen("mshta.exe \"javascript:alert('Failed to download patches from Internet.');close()\"", shell=True)
      subprocess.Popen("vivaldi.exe")
      sys.exit(0)
    
    else:    
      os.makedirs("patch", exist_ok=True)
      with zipfile.ZipFile('patch.zip', "r") as patches:
        patches.extractall("patch")
    
      batch_unpack.unpack(Locales_dir, "POfiles")
      batch_patch.patch("patch", "POfiles")
      batch_pack.pack("POfiles", Locales_dir)
    
      with open(os.path.join(Locales_dir, "patch.done"), "a") as checkfile:
        checkfile.write("Greetings from the Czech Republic!\n\n(c)2017 nfsmaniac")
    
      subprocess.Popen("vivaldi.exe")       # launch Vivaldi
    
      for f in os.listdir("patch"):         # Cleanup
        os.remove(os.path.join("patch", f))
      os.rmdir("patch")
      for f in os.listdir("POfiles"):       # Cleanup
        os.remove(os.path.join("POfiles", f))
      os.rmdir("POfiles")
      os.remove("patch.zip")
    
      subprocess.Popen("mshta.exe \"javascript:alert('Enjoy your better translated Vivaldi!\\n\\nCredits:\\n----------------\\nnfsmaniac\\t\\t(founder, maintainer, Czech translator)\\nAn_dz\\t\\t(past development support)\\nra-mon\\t\\t(French translator, bug reporter)\\nahoj1234\\t\\t(Czech translator)\\nCheVe11e_191\\t(Slovak translator)\\nzmeYpc\\t\\t(Bulgarian translator)');close()\"", shell=True)
      sys.exit(0)     

if __name__ == '__main__':
  main()
