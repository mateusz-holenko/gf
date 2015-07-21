#!/usr/bin/python3
import codecs
##########################################################################################################
#                                                                                                        #
# Based on:                                                                                              #
# http://stackoverflow.com/questions/436220/python-is-there-a-way-to-determine-the-encoding-of-text-file #
#                                                                                                        #
##########################################################################################################
encodings = ['utf-8', 'windows-1250']

def try_read_file(file, action, fail_action):
    global encodings
    for e in encodings:
        try:
            with codecs.open(file, 'r', encoding=e) as f:
                for line in f.readlines():
                    action(line)
            return True
        except UnicodeDecodeError:
            fail_action(e)
        else:
            return False

def read_file(file):
    global encodings
    for e in encodings:
        try:
            with codecs.open(file, 'r', encoding=e) as f:
                return f.readlines()
        except UnicodeDecodeError:
            pass
    return None

