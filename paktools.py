#!/usr/bin/env python

# Original file: http://code.google.com/searchframe#OAMlx_jo-ck/src/tools/grit/grit/format/data_pack.py
# Copyright (c) 2012 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
# (http://code.google.com/searchframe#OAMlx_jo-ck/src/LICENSE)

# This file:
#
# Copyright (c) 2012 Adobe Systems Incorporated. All rights reserved.
#  
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"), 
# to deal in the Software without restriction, including without limitation 
# the rights to use, copy, modify, merge, publish, distribute, sublicense, 
# and/or sell copies of the Software, and to permit persons to whom the 
# Software is furnished to do so, subject to the following conditions:
#  
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#  
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
# DEALINGS IN THE SOFTWARE.

PYTHONIOENCODING="UTF-8"

'''Provides functions to handle .pak files as provided by Chromium. If the optional argument is a file, it will be unpacked, if it is a directory, it will be packed.'''

import collections
import os
import struct
import sys
import re
import shutil
import time
import polib

PACK_FILE_VERSION = 4
HEADER_LENGTH = 2 * 4 + 1  # Two uint32s. (file version, number of entries) and
                           # one uint8 (encoding of text resources)
BINARY, UTF8, UTF16 = list(range(3))

class WrongFileVersion(Exception):
  pass

DataPackContents = collections.namedtuple('DataPackContents', 'resources encoding')

def ReadDataPack(input_file):
  """Reads a data pack file and returns a dictionary."""
  with open(input_file, "rb") as file:
    data = file.read()
  original_data = data

  # Read the header.
  version, num_entries, encoding = struct.unpack("<IIB", data[:HEADER_LENGTH])
  if version != PACK_FILE_VERSION:
    print("Wrong file version in ", input_file)
    raise WrongFileVersion

  resources = {}
  if num_entries == 0:
    return DataPackContents(resources, encoding)

  # Read the index and data.
  data = data[HEADER_LENGTH:]
  kIndexEntrySize = 2 + 4  # Each entry is a uint16 and a uint32.
  for _ in range(num_entries):
    id, offset = struct.unpack("<HI", data[:kIndexEntrySize])
    data = data[kIndexEntrySize:]
    next_id, next_offset = struct.unpack("<HI", data[:kIndexEntrySize])
    resources[id] = original_data[offset:next_offset]

  return DataPackContents(resources, encoding)

def WriteDataPackToString(resources, encoding):
  """Write a map of id=>data into a string in the data pack format and return it."""
  ids = sorted(resources.keys())
  ret = []

  # Write file header.
  ret.append(struct.pack("<IIB", PACK_FILE_VERSION, len(ids), encoding))
  HEADER_LENGTH = 2 * 4 + 1            # Two uint32s and one uint8.

  # Each entry is a uint16 + a uint32s. We have one extra entry for the last
  # item.
  index_length = (len(ids) + 1) * (2 + 4)

  # Write index.
  data_offset = HEADER_LENGTH + index_length
  for id in ids:
    ret.append(struct.pack("<HI", id, data_offset))
    data_offset += len(resources[id].encode())

  ret.append(struct.pack("<HI", 0, data_offset))

  # Write data.
  for id in ids:
    ret.append(resources[id].encode())
  return b''.join(ret)

def WriteDataPack(resources, output_file, encoding):
  """Write a map of id=>data into output_file as a data pack."""
  content = WriteDataPackToString(resources, encoding)
  with open(output_file, "wb") as file:
    file.write(content)

def PackDirectoryIntoFile(directory, pakFile):
  print("Packing {0} as {1}".format(directory, pakFile))

  # if it's a gettext file we signal it
  if os.path.isfile(directory) and re.search("\.po(t)?$", directory):
    pot = True
  elif not os.path.isdir(directory):
    print("{0} is not a directory (or does not exist)".format(directory))
    return False

  if not pot:
    files = os.listdir(directory)
    files.sort()

    numeric = re.compile("^\d+$")

    data = {}
    for (id) in files:
      if not numeric.match(id):
        continue
      input_file = "%s/%s" % (directory, id)
      with open(input_file, "rb") as file:
        data[int(id)] = file.read()
  else:
    data = {}
    po = polib.pofile(directory)
    for entry in po:
      id = entry.msgctxt
      if entry.msgstr == "":
        POstring = entry.msgid
      else:
        POstring = entry.msgstr
      #print(id)
      #print(POstring) 
      data[int(id)] = POstring

  WriteDataPack(data, pakFile, UTF8)

  return True

def UnpackFileIntoDirectory(pakFile, pakFile2, poFile):
  print("Converting {0} to {1}".format(pakFile2, poFile))

  if not os.path.isfile(pakFile):
    print("{0} is not a file (or does not exist)".format(pakFile))
    return False

  data = ReadDataPack(pakFile)
  data2 = ReadDataPack(pakFile2)
  #print data.encoding

  name = os.path.basename(poFile)
  name = os.path.splitext(name)
  if name[1].lower() == ".po":
    po = polib.POFile()
    # just development version, better metadata is to be done
    po.metadata = {
        'Project-Id-Version': '1.0',
        'Report-Msgid-Bugs-To': 'you@example.com',
        'POT-Creation-Date': '2007-10-18 14:00+0100',
        'PO-Revision-Date': '2007-10-18 14:00+0100',
        'Last-Translator': 'you <you@example.com>',
        'Language-Team': 'English <yourteam@example.com>',
        'MIME-Version': '1.0',
        'Content-Type': 'text/plain; charset=utf-8',
        'Content-Transfer-Encoding': '8bit',
    }
    for (resource_id, contents), (resource_id2, contents2) in zip(data.resources.items(), data2.resources.items()):
      po_flag = None
      #fileheader = contents.strip()[0:3].decode('utf-8', 'ignore')
      HTML_string = re.compile(r'(</.*>)')
      string_id = str(resource_id)
      original_string = str(contents, 'utf-8')
      translated_string = str(contents2, 'utf-8')
        
      if translated_string == original_string and original_string != "Vivaldi" and original_string.isdigit() == False:
        translated_string = ""
        
      #if fileheader[0:1] == '<':
      if HTML_string.search(original_string) != None:
        po_flag = "HTML (EULA, error pages, etc.)"
              
      entry = polib.POEntry(
          comment=po_flag,
          msgctxt=string_id,
          msgid=original_string,
          msgstr=translated_string          
      )
      po.append(entry)
      
    po.save(poFile)
  else:
    if os.path.exists(directory):
      shutil.rmtree(directory)
    os.makedirs(directory)

    for (resource_id, contents) in data.resources.items():
      output_file = "{0}/{1}".format(directory, resource_id)
      with open(output_file, "wb") as file:
        file.write(contents)

def FindIdForNameInHeaderFile(name, headerFile):
  print("Extracting ID for {0} from header file {1}".format(name, headerFile))
  with open(headerFile, "rb") as file:
    match = re.search("#define {0} (\d+)".format(name), file.read()) # not sure about the syntax
    return int(match.group(1)) if match else None 

def main():
  if len(sys.argv) <= 1:
    print("Usage: {0} <file_or_directory>".format(sys.argv[0]))
    return

  path = sys.argv[1]
  if os.path.isdir(path):
    PackDirectoryIntoFile(path, path + ".pak")
  else:
    UnpackFileIntoDirectory(path, re.sub("\.pak$", "", path))

if __name__ == '__main__':
  main()
