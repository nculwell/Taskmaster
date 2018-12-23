#!/usr/bin/python3
# vim: et ts=8 sts=4 sw=4

import markdown
from html.parser import HTMLParser
from html.entities import name2codepoint
from .pg import *

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

def CreateDoc(docTypeId, bodyText):
    Insert('doc', [
        ('doc_type_id', docTypeId),
        ('body', bodyText),
        ('revision_note', 'Created.'),
    ])

def UpdateDoc(docId, newBodyText, revisionNumber, revisionNote):
    doc = Query1("select * from doc where id=%s", docId)
    if doc['revision_number'] != str(revisionNumber):
        raise Exception("Document has been edited since it was loaded.")
    Update('doc', [
        ('body', newBodyText),
        ('revision_note', revisionNote),
        ('revision_number', revisionNumber + 1),
    ], [
        ('id', docId),
        ('revision_number', revisionNumber),
    ])

def DiffFiles(filename1, filename2):
    with open(filename1) as f:
        lines1 = f.readlines()
    with open(filename2) as f:
        lines2 = f.readlines()
    return Diff(lines1, lines2)

def Diff(lines1, lines2):
    diff = difflib.unified_diff(lines1, lines2, n=0)
    sys.stdout.writelines(diff)

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

def Test:
    with open('test.md') as f:
        md = f.read()
    text = MarkdownToText(md)
    print(text)
    print('----------')
    DiffFiles('wsserv.py', 'diff-wss.py')

