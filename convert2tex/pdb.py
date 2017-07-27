#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import subprocess
import os

def generate_contents(temp_fn):
    # convert content encoding from big5-2003 to utf8
    utf8_contents = subprocess.check_output((["iconv", "-f", "big5-2003", "-t", "utf8", temp_fn]))
    lines = [l.strip() for l in utf8_contents.split('\n')]

    for i, l in enumerate(lines):
        if l.isdigit():
            del lines[i]
            break
    
    return "\n".join(lines).decode('UTF-8') 

def extract_contents_from_pdb(fn, out_fn):
    f = open(fn, 'rb')

    # read pdb header
    t = f.read(76)
    record = f.read(2)
    record = ord(record[0])*256 + ord(record[1])
    t = f.read(record*8)

    # read contents encoding with big5-2003
    s = f.read()
    s = s.replace('\x0d', '').replace('\x1b', '\x0a').replace('\x00', '\x0a\x0a')

    f.close()

    # write contents encoding with big5-2003
    out_f = open(out_fn, 'w')
    out_f.write(s[:-4] + "\n\n")
    out_f.close()
    
    return generate_contents(out_fn)


def remove_temporary_files(fn, *unrm_fn_list):
    remove_file_list = [f for f in os.listdir(".") if f.startswith(fn[:-4])]
    for unrm_fn in unrm_fn_list:
        if unrm_fn in remove_file_list:
            remove_file_list.remove(unrm_fn)

    cmd = ["rm", "-f"]
    cmd.extend(remove_file_list)
    subprocess.call(cmd)
    return " ".join(remove_file_list)

