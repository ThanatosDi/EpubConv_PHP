#!/usr/bin/env python
#-*- coding: utf8 -*-

import sys
import getopt
import subprocess
import string

from epub import extract_content_from_epub 
from s2t import convert_UTF8_content 
from pdb import extract_contents_from_pdb

""" Font and page attribute setting"""

FONT_NAME="DFMing Std W5"
VERTICAL_PAGE_ATTRIBUTE="landscape"
VERTICAL_FONT_ATTRIBUTE="Vertical=RotatedGlyphs"

GET_CONTENT_MESSAGE = "Parse text content from epub/ pdb file: "
TRANSLATE_MESSAGE = "Translate Simple Chinese to Tranditional Chinese: "
CONVERT_VERTIAL_SYMBOL_MESSAGE = "Convert symbol to support vertial writing: "
YIELD_TEX_FILE_MESSAGE = "Generate tex(xelatex) output file: "
HELP_MESSAGE = """convert2tex.py -s -h -w -l -f font_name filename
-h show the help
-s traslate simple chinese text to tradional chinese text 
-w horizontal writing
-l compile the generated file with xelatex 
-f set main font name
"""

XELATEX_HEADER="""%!TEX TS-program = xelatex
%!TEX encoding = UTF-8 Unicode

\documentclass[12pt, fleqn, $vertical_page_attribute]{article}
\usepackage[b5paper, left=2.5cm, right=2.5cm, top=2.5cm, bottom=3.5cm]{geometry}

\usepackage{fontspec}
\usepackage{xeCJK}
\setCJKmainfont[$vertical_font_attribute]{$font_name}
\usepackage{parskip}
\setlength{\parskip}{.2cm}

\\renewcommand\CJKglue{\hskip -0.3pt plus 0.08\\baselineskip}
\linespread{1.15}
\parindent=0pt
\\renewenvironment{quote}
  {\list{}{\\topsep 0ex\parsep 0ex\setlength\leftmargin{1.5em}%
\\rightmargin\leftmargin}\item\\relax\linespread{1.0}\small}%
{\endlist}

\XeTeXlinebreaklocale "zh"
\XeTeXlinebreakskip = 0pt plus 1pt 

\\title{}
\\author{}
\\pagestyle{empty}

\\begin{document}
"""

XELATEX_FOOTER="""
\\end{document}
"""



simple_chinese_2_tradtional_chinese = convert_UTF8_content

def get_pdb_content(fn):
    temp_fn = fn[:fn.rfind('.')]
    content = extract_contents_from_pdb(fn, temp_fn)
    subprocess.call(["rm", "-rf", temp_fn])
    return content

def get_epub_content(fn):
    return extract_content_from_epub(fn)

def get_txt_content(fn):
    f = open(fn)
    content = f.read()
    f.close()
    return content

def get_content(fn):
    content = ""
    if fn.endswith(".pdb"):
        content = get_pdb_content(fn)
    elif fn.endswith(".epub"):
        content = get_epub_content(fn)
    elif fn.endswith(".txt"):
        content = get_txt_content(fn)

    return content

def convert_vertial_symbol(content):
    symbol_map = {u"“": u"﹁",
                  u"”": u"﹂",
                  u"…": u" $\cdots$ ",
                  u"_": u"\_",
                  u'　': u'  ',
                  u'——': u' --- ',
                  u'?': u'？',
                  u'!': u'！'}

    for k, v in symbol_map.items():
        content = content.replace(k, v)

    return content

def add_xelatex_header_footer(content, header, footer):
    return header + "\n\n".join(["\quad\quad " + l if l.strip() else l for l in content.split('\n')]) + footer

def convert_file(fn, s2t, vertial_writing_convert):
    # get text content
    print GET_CONTENT_MESSAGE + fn 
    content = get_content(fn)
    xelatex_header_template = string.Template(XELATEX_HEADER)

    if content:
        if not fn.endswith('pdb'):
            # convert Simple Chinese to Tradional Chinese
            if s2t:
                print TRANSLATE_MESSAGE + fn
                content = simple_chinese_2_tradtional_chinese(content)

            # convert symbol to support vertial writing
            if vertial_writing_convert:
                print CONVERT_VERTIAL_SYMBOL_MESSAGE + fn
                content =  convert_vertial_symbol(content) 

        # add xelatex header and footer
        print YIELD_TEX_FILE_MESSAGE + fn[:fn.rfind('.')]  + ".tex"
        vpa = VERTICAL_PAGE_ATTRIBUTE if vertial_writing_convert else ""
        vfa = VERTICAL_FONT_ATTRIBUTE if vertial_writing_convert else ""
        content = add_xelatex_header_footer(
                    content, 
                    xelatex_header_template.substitute(
                        font_name=FONT_NAME,
                        vertical_page_attribute=vpa,
                        vertical_font_attribute=vfa),
                    XELATEX_FOOTER)
        
        # write to file
        f = open(fn[:fn.rfind('.')] + ".tex", "w")
        f.write(content.encode('UTF-8'))
        f.close()
        return fn[:fn.rfind('.')] + ".tex"

    return ""


def main():
    if len(sys.argv) == 1:
        print HELP_MESSAGE 
        return 

    s2t = False 
    vertial_writing_convert = True 
    xelatex_compile = False

    optlist, args = getopt.getopt(sys.argv[1:], "hf:ls")
    for opt, value in optlist:
        if opt == "-h":
            print HELP_MESSAGE
            return 
        if opt == "-w":
            vertial_writing_convert = False
        if opt == "-f":
            FONT_NAME = value
        if opt == "-l":
            xelatex_compile = True
        if opt == "-s":
            s2t = True

    if args:
        # get text content
        for fn in args:
            tex_fn = convert_file(fn, s2t, vertial_writing_convert)

            if xelatex_compile and tex_fn:
                subprocess.check_output(["xelatex", tex_fn])
    else:
        print "No input file names"


if __name__ == "__main__":
    main()
