#!/usr/bin/env python
#-*- coding: utf8 -*-

import sys
import zipfile
import s2t 

def convert_epub_sc2tc(input_fn, output_fn):
    
    # read epub file and convert
    input_fh = zipfile.ZipFile(input_fn, "r")
    fn_list_sc = [fn for fn in input_fh.namelist() if any(fn.endswith(x) for x in ['html', 'htm', 'ncx', 'opf'])]
    fn_list_bin = list(set(input_fh.namelist()).difference(fn_list_sc)) 

    content_list_tc = [s2t.convert_UTF8_content(input_fh.read(fn).replace('zh-CN', 'zh-TW')) for fn in fn_list_sc]
    content_list_bin = [input_fh.read(fn) for fn in fn_list_bin]

    input_fh.close()

    # write epub file
    out_fh = zipfile.ZipFile(output_fn, "w")
    for fn, content in zip(fn_list_sc, content_list_tc):
        out_fh.writestr(fn, content.encode('UTF-8'))
    for fn, content in zip(fn_list_bin, content_list_bin):
        out_fh.writestr(fn, content)
    
    out_fh.close()



def main():
    epub_fn_list = []
    if len(sys.argv) < 2:
        print "epubs2t.py sample.epub"
    else:
        epub_fn_list = sys.argv[1:]

    for epub_fn in epub_fn_list:
        if epub_fn.endswith('.epub'):
            convert_epub_sc2tc(epub_fn, epub_fn[:-5] + "_tc.epub")
            print "Convert " + epub_fn + " to " + epub_fn[:-5] + "_tc.epub Sucessfully."


if __name__ == "__main__":
    main()
