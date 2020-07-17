"""
код основан на репо https://github.com/danielfett/htmldiff
который является форком https://github.com/cygri/htmldiff
"""

import io
from difflib import SequenceMatcher

import six

from boltons.ioutils import SpooledBytesIO

from comparison import constants


def utf8_encode(val):
    """Return a string in bytes; use utf-8 for unicode strings."""
    if isinstance(val, six.text_type):
        return val.encode('utf-8')
    elif isinstance(val, six.binary_type):
        return val
    else:
        raise TypeError('{} is not a unicode or str object'.format(val))


def is_junk(x):
    """
    Used for the faster but less accurate mode.

    :type x: string
    :param x: string to match against
    :returns: regex matched or lowercased x
    """
    return constants.WS_RE.match(x) or x.lower() in constants.STOPWORDS_RU


class TagIter(object):
    """Iterable that returns tags in sequence."""

    def __init__(self, html_string):
        self.html_string = html_string
        self.pos = 0
        self.end_reached = False
        self.buffer = []

    def __iter__(self):
        return self

    def __next__(self):
        if self.buffer:
            return self.buffer.pop(0)

        if self.end_reached:
            raise StopIteration
        
        match = constants.TAG_RE.search(self.html_string, pos=self.pos)
        if not match:
            self.end_reached = True
            return self.html_string[self.pos:]

        self.buffer.append(match.group(0))
        val = self.html_string[self.pos:match.start()]
        self.pos = match.end()
        return val

    def next(self):
        return self.__next__()


class HTMLMatcher(SequenceMatcher):
    """SequenceMatcher for HTML data."""

    start_insert_text = '<ins>'
    end_insert_text = '</ins>'
    start_delete_text = '<del>'
    end_delete_text = '</del>'
    stylesheet = """
                 del {
                       text-decoration: line-through;
                       background-color: #fbb;
                       color: #555;
                     }
                 ins {
                       text-decoration: none;
                       background-color: #d4fcbc;
                     }"""

    def __init__(self, source1, source2, accurate_mode):

        if accurate_mode:
            SequenceMatcher.__init__(self, lambda x: False, source1, source2, False)
        else:
            SequenceMatcher.__init__(self, is_junk, source1, source2, False)

    def set_seqs(self, a, b):
        SequenceMatcher.set_seqs(self, self.split_html(a), self.split_html(b))

    def split_html(self, t):
        result = []
        for item in TagIter(t):
            if item.startswith(bytes('<','utf-8')):
                result.append(item)
            else:
                result.extend(constants.WORD_RE.findall(item))
        return result

    def diff_html(self, insert_stylesheet=True):
        opcodes = self.get_opcodes()
        a = self.a
        b = self.b
        out = SpooledBytesIO()
        for tag, i1, i2, j1, j2 in opcodes:
            if tag == 'equal':
                for item in a[i1:i2]:
                    out.write(item)
            if tag == 'delete':
                self.text_delete(a[i1:i2], out)
            if tag == 'insert':
                self.text_insert(b[j1:j2], out)
            if tag == 'replace':
                if (self.is_invisible_change(a[i1:i2], b[j1:j2])):
                    for item in b[j1:j2]:
                        out.write(item)
                else:
                    self.text_delete(a[i1:i2], out)
                    self.text_insert(b[j1:j2], out)
        html = out.getvalue()
        out.close()
        if insert_stylesheet:
            html = self.insert_stylesheet(html)
        return html

    def is_invisible_change(self, seq1, seq2):
        #LOG.debug('Checking if change is visible...')
        if len(seq1) != len(seq2):
            return False
        for i in range(0, len(seq1)):
            if seq1[i][0] == '<' and seq2[i][0] == '<':
                continue
            if all((constants.WS_RE.match(seq1[i]),
                    constants.WS_RE.match(seq2[i]))):
                continue
            if seq1[i] != seq2[i]:
                return False
        return True

    def text_delete(self, lst, out):
        text = []
        for item in lst:
            if item.startswith(bytes('<', 'utf-8')):
                self.out_delete(''.join(text), out)
                text = []
            else:
                text.append(item.decode('utf-8'))
        self.out_delete(''.join(text), out)

    def text_insert(self, lst, out):
        text = []
        for item in lst:
            if item.startswith(bytes('<', 'utf-8')):
                self.out_insert(''.join(text), out)
                text = []
                out.write(item)
            else:
                text.append(item.decode('utf-8'))
        self.out_insert(''.join(text), out)

    def out_delete(self, s, out):
        if not s.strip():
            val = s
        else:
            val = ''.join((self.start_delete_text, s, self.end_delete_text))
        out.write(bytes(val, 'utf-8'))

    def out_insert(self, s, out):
        if not s.strip():
            val = s
        else:
            val = ''.join((self.start_insert_text, s, self.end_insert_text))
        out.write(bytes(val, 'utf-8'))

    def insert_stylesheet(self, html, stylesheet=None):
        """
        Добавляет стили css в header html. Пробует найти тег head и вставить
        после него, если head не существует, то вставляет в начало строки.

        :type html: str
        :param html: строка html
        :type stylesheet: str
        :param stylesheet: css стили для включения в header документа
        :returns: модифицированную html строку с добавленным стилем css
        """
        if not stylesheet:
            stylesheet = self.stylesheet
        #LOG.debug('Inserting stylesheet...')
        match = constants.HEAD_RE.search(html)
        pos = match.end() if match else 0
        return ''.join((
            (html[:pos]).decode('utf-8'),
            '\n<style type="text/css">\n',
            stylesheet,
            '</style>',
            (html[pos:]).decode('utf-8'),
        ))


def diff_strings(orig, new, accurate_mode):
    """
    На входе две строки html, выход строка со сравнением

    :type orig: string
    :param orig: первая строка для сравнения
    :type new: string
    :param new: вторая строка для сравнения с первой
    :type accurate_moode: boolean
    :param accurate_moode: режим сравнения
    :returns: строка, содержащая содержание сравнение первой и второй строки
    """
    # Make sure we are dealing with bytes...
    orig = utf8_encode(orig)
    new = utf8_encode(new)
    h = HTMLMatcher(orig, new, accurate_mode)
    return h.diff_html(True)


def diff_files(initial_path, new_path, accurate_mode):
    """
    Сравнение двух html файлов

    :type initial_path: object
    :param initial_path: первый файл для сравнения
    :type new_path: object
    :param new_path: второй файл для сравнения с первым
    :type accurate_mode: boolean
    :param accurate_mode: режим сравнения, от этого зависит время выполнения,
                          True мебленный, False быстрый
    :returns: строка, содержащая содержание сравнение первого и вторго файлов
    """
    f = io.BytesIO(bytes(initial_path, encoding= 'utf-8'))
    source1 = constants.COMMENT_RE.sub(bytes('','utf-8'), f.read())

    f = io.BytesIO(bytes(new_path, encoding= 'utf-8'))
    source2 = constants.COMMENT_RE.sub(bytes('','utf-8'), f.read())

    return diff_strings(source1, source2, accurate_mode)
