#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from common import make_pathname
from config import MD_FILE_TEMPLATE, HTML_FILE_TEMPLATE
import codecs
import os
import re


class LineWriter(object):

    def __init__(self, target, newlines):
        self.target = target
        if not newlines:
            self.newlines = '\n'
        else:
            self.newlines = newlines
        self.prev_line_empty = False

    def write(self, line):
        """Write line to target, reset blank line counter, output newline if necessary."""
        if self.prev_line_empty:
            self.target.write(self.newlines)
        self.target.write(line.rstrip())
        self.target.write(self.newlines)
        self.prev_line_empty = False

    def mark_empty_line(self):
        self.prev_line_empty = True


FULL_CROSS_REFERENCE = re.compile("\[(.*?)\](\(.+?.html\))")

def copy_and_fix_headlines(dst_dir, filename, headline_level=1, reference_converter=False):
    """
    Copy files to destination directory, increase headline level, 
    move page headline from front matter.
    """
    result_path = os.path.join(dst_dir, filename)
    begin_front_matter = False
    end_front_matter = False
    with codecs.open(filename, 'r', 'utf-8') as source:
        with codecs.open(result_path, 'w', 'utf-8') as target:
            lw = LineWriter(target, source.newlines)
            for line in source:
                l = line.rstrip()
                if begin_front_matter and not end_front_matter:
                    if l == '---':
                        end_front_matter = True
                    else:
                        try: 
                            key, value = l.split(':', 1)
                        except ValueError:
                            raise Exception("metadata must be in the format 'key: value' (%s)" % filename)
                        if key.strip() == 'title':
                            lw.write('%(hashes)s %(title)s %(hashes)s' % {
                                     'hashes': '#'*headline_level, 'title': value.strip()})
                    continue

                if not l:
                    lw.mark_empty_line()
                elif l == '---':
                    if not begin_front_matter:
                        begin_front_matter = True
                    else:
                        # omit line, do not change empty line marker!
                        pass
                elif l.startswith('#'):
                    lw.write(increase_headline_level(l, headline_level))
                else:
                    if callable(reference_converter):
                        result = FULL_CROSS_REFERENCE.findall(l)
                        # replace all link targets
                        for (text, target) in result:
                            l = l.replace(target, reference_converter(text,target))
                        lw.write(l)
                    else: 
                        lw.write(line)


SHORT_CROSS_REFERENCE = re.compile("(\[[\w\s\-]+?\]\[\])")

def expand_cross_references(source_filename, target_filename):

    with codecs.open(source_filename, 'r', 'utf-8') as source:
        with codecs.open(target_filename, 'w', 'utf-8') as target:
            for line in source:
                target.write(replace_references(line))


def replace_references(line):
    result = SHORT_CROSS_REFERENCE.findall(line)
    for ref in result:
        title = ref[1:-3]
        new_ref = "[%s](%s)" % (title, HTML_FILE_TEMPLATE % make_pathname(title))
        line = line.replace(ref, new_ref)
    return line

 
def increase_headline_level(line, times):
    for x in range(times-1):
        line = '#' + line
        if line.endswith('#'):
            line = line + '#'
    return line
