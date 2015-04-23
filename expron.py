#!/usr/bin/python

import sys
import os
import re
import pycurl
import StringIO

QUERY_URL = 'http://endic.naver.com/search.nhn?sLn=en&query={}'
RE_OBJECT = re.compile(r'playlist="([^"]+)"')

def main(word):
    page_source = fetch_page_source(word)
    pron_url = extract_pron_url(page_source)
    if pron_url:
        filename = word+'.mp3'
        download_pronfile(filename, pron_url)
        play_downloaded(filename)

def fetch_page_source(word):
    url = QUERY_URL.format(word)
    b = StringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, b)
    c.perform()
    c.close()
    return b.getvalue()

def extract_pron_url(page_source):
    mo = RE_OBJECT.search(page_source)
    if mo:
        return mo.group(1)

def download_pronfile(filename, url):
    with open(filename, 'wb') as f:
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(c.WRITEDATA, f)
        c.perform()
        c.close()

def play_downloaded(filename):
    cmd = '( afplay {} & )'.format(filename)
    os.system(cmd)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print 'expron.py {a_word}'
