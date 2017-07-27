#-*- coding: utf8 -*-
WORD_DICTIONARY_PATH = "/home/epub/public_website/convert2tex/word_s2t.txt"
PHASE_DICTIONARY_PATH = "/home/epub/public_website/convert2tex/phrase_s2t.txt"

class DictionarySingleton(object):
    _instance = None
    def __init__(self):
        f = open(WORD_DICTIONARY_PATH, 'r')
        self.w_dict = dict([tuple(l.split(',')[0:2]) for l in f.read().decode('UTF-8').split('\r\n')])
        f.close()

        f = open(PHASE_DICTIONARY_PATH, 'r')
        self.p_dict = dict([tuple(l.split(',')[0:2]) for l in f.read().decode('UTF-8').split('\r\n')])
        f.close()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DictionarySingleton, cls).__new__(
                                cls, *args, **kwargs)


        return cls._instance

    def word_dic(self):
        return self.w_dict

    def phase_dic(self):
        return self.p_dict


# only one instance 
TRANSLATE_DICTIONARY = DictionarySingleton()

def convert_word(s_string, w_dic):
    t_string = s_string
    for k, v in w_dic.items():
        if k in t_string:
            t_string = t_string.replace(k, v)

    return t_string

#def convert_phase(string_in, dic):
    #i=0
    #s = string_in
    #while i < len(s):
        #for j in range(len(s) - i +1, 0, -1):
            #if s[i:j] in dic:
                #t = dic[s[i:j]]
                #s = s.replace(s[i:j], t) 
                #i += len(t) -1
                #break
        #i += 1

    #return s 


def convert_UTF8_content(content):
    s2t_dicts = DictionarySingleton()
    content_lines = [convert_word(l, s2t_dicts.word_dic()) for l in content.decode('UTF-8').splitlines()]
    return "\n".join([convert_word(l, s2t_dicts.phase_dic()) for l in content_lines])

