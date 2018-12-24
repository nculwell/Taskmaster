#!/usr/bin/python3
# vim: et ts=8 sts=4 sw=4

import markdown
from html.parser import HTMLParser
from html.entities import name2codepoint
import sys, difflib

def MarkdownToText(md):
    html = MarkdownToHtml(md)
    text = HtmlToText(html)
    return text

def MarkdownToHtml(md):
    html = markdown.markdown(md)
    return html

def HtmlToText(html):
    parser = HP()
    parser.feed(html)
    return parser.getText()

DOC_TYPE_TSK_DESC = 1
DOC_TYPE_TSK_COMMENT = 2

def DiffFiles(filename1, filename2):
    with open(filename1) as f:
        lines1 = f.readlines()
    with open(filename2) as f:
        lines2 = f.readlines()
    return Diff(lines1, lines2)

def Diff(lines1, lines2):
    diff = difflib.unified_diff(lines1, lines2, n=0)
    lines = ( x for x in diff if not x.startswith('+') )
    parsed = ParseDiff(lines)
    return parsed

def ApplyDiff(source, diff):
    source = _Lines(source)
    diff = _Lines(diff)
    srcIter = iter(source)
    srcLine = 1
    result = []
    for delta in diff:
        _, (deltaStart, deltaLength), deltaLines = delta
        while srcLine < deltaStart:
            result.append(next(srcIter))
            srcLine += 1
        result.extend(deltaLines)
        while srcLine < deltaStart + deltaLength:
            discard = next(srcIter)
            srcLine += 1
    return result

def ParseDiff(diff):
    print("ParseDiff")
    d = iter(diff)
    line = next(d)
    while not line.startswith('@'):
        #print("SKIP", line)
        line = next(d)
    chunk = []
    while True:
        fr, to = _ParseLineNumbers(line)
        try:
            line = next(d)
            while line.startswith('-'):
                chunk.append(line[1:])
                line = next(d)
            yield (fr, to, chunk)
            chunk = []
        except StopIteration:
            yield (fr, to, chunk)
            return
        except:
            raise

def _ParseLineNumbers(line):
    line = line.strip()
    #print("PARSING:", line)
    numbers = line.split()[1:][:2]
    #print("P2", numbers)
    numLens = [ (n[1:].split(',') + [1])[:2] for n in numbers ]
    #print("P3", numLens)
    return ( [ int(m) for m in n ] for n in numLens )

def _Lines(arg):
    if isinstance(arg, str):
        return arg.split('\n')
    else:
        return arg

BLOCK_TAGS = set((
    'div', 'ul', 'ol', 'p',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
))

class HP(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self._txt = []
    def _add(self, text):
        self._txt.append(text)
    def getText(self):
        return ''.join(self._txt)
    def handle_starttag(self, tag, attrs):
        if tag in BLOCK_TAGS:
            self._add('\n')
        elif tag == 'li':
            self._add('* ') # TODO: ul/ol
        # TODO: pre, blockquote, li, tables
    def handle_endtag(self, tag):
        if tag in BLOCK_TAGS or tag in ('br', 'li'):
            self._add('\n')
    def handle_data(self, data):
        if data == '\n':
            return
        self._add('[')
        self._add(data)
        self._add(']')
    def handle_entityref(self, name):
        c = unichr(name2codepoint[name])
        self._add(c)
    def handle_charref(self, name):
        if name.startswith('x'):
            c = unichr(int(name[1:], 16))
        else:
            c = unichr(int(name))
        self._add(c)

if __name__ == '__main__':
    with open('test.md') as f:
        md = f.read()
    text = MarkdownToText(md)
    print(text)
    print('----------')
    diff = DiffFiles('wsserv.py', 'diff-wss.py')
    #parsed = ParseDiff(diff)
    for line in diff:
        print(line)
    #sys.stdout.writelines(diff)

