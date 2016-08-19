#!/usr/bin/python
 # -*- coding: utf-8 -*-

"""
Build slide deck to reveal.js and 
"""

from __future__ import unicode_literals

from glob import glob
import codecs
import os
import os.path
import re
from string import Template

from s3_patterns import s3_patterns, handbook_group_order
from common import make_pathname, make_title, create_directory


def cmd_slides(args):
    """Build slides decks"""

    if args.skeleton: 
        create_source_files_for_slides(args)
    if args.reveal: 
        build_reveal_slides(args)
    if args.deckset: 
        build_deckset_slides(args)


def create_source_files_for_slides(args):
    """Create dummy source files for slides. If file or folder exists, don't touch it."""

    create_directory(args.source)

    def make_file(root, filename_root, title_root, markup = '#'):
        """Create file if it does not exist."""
        filename = os.path.join(root, '%s.md' % make_pathname(filename_root))
        if not os.path.exists(filename):
            with codecs.open(filename, 'w+', 'utf-8') as fp:
                fp.write('%s %s\n\n' % (markup, make_title(title_root)))
        else:
            if args.verbose: 
                print "skipped %s" % title_root

    for group in s3_patterns.keys():
        # create group dir
        group_root = os.path.join(args.source, make_pathname(group))
        create_directory(group_root)
        # create group index file
        make_file(group_root, "index", group, '#')
        # create individual patterns (add pattern name as headline)
        for pattern in s3_patterns[group]:
            make_file(group_root, pattern, pattern, '##')

def build_deckset_slides(args):
    """Create a source file for a deckset presentation."""
    r = DecksetWriter(args)
    r.build()   

class DecksetWriter(object):
    CONTENT_MARKER = "<!-- INSERT-CONTENT -->"

    def __init__(self, args):
        self.args = args
        self.source = self.args.source
        self.template_path = os.path.join(os.path.dirname(self.args.target), 'deckset_template.md')
    
    def build(self):
   
        with codecs.open(self.args.target, 'w+', 'utf-8') as self.target:
            with codecs.open(self.template_path, 'r', 'utf-8') as self.template:

                self.copy_template_header()
                # insert_title
                self._copy_markdown(self.source, 'title.md')
                for group in handbook_group_order:
                    self.insert_group(group)
                # insert closing 
                self._copy_markdown(self.source, 'closing.md')
                self.copy_template_footer()

    def copy_template_header(self):
        for line in self.template:
            if line.strip() == self.CONTENT_MARKER:
                break
            else: 
                self.target.write(line)

    def copy_template_footer(self):
        for line in self.template:
            self.target.write(line)

    def insert_group(self, group):
        folder = os.path.join(self.source, make_pathname(group))
        self._copy_markdown(folder, 'index.md')                
        for pattern in sorted(s3_patterns[group]):
            self._copy_markdown(folder, '%s.md' % make_pathname(pattern))
            
    def _copy_markdown(self, folder, name):
        with codecs.open(os.path.join(folder, name), 'r', 'utf-8') as section:
            for line in section:
                self.target.write(line)
        self.target.write('\n\n---\n\n')


def build_reveal_slides(args):
    """
    Build reveal.js presentation. <target> is a file inside the reveal.js folder, 
    template.html is expected in the same folder.
    """
    r = RevealJsWriter(args)
    r.build()   


class RevealJsWriter(object):

    CONTENT_MARKER = "<!-- INSERT-CONTENT -->"

    def __init__(self, args):
        self.args = args
        self.source = self.args.source
        self.template_path = os.path.join(os.path.dirname(self.args.target), 'template.html')
    
    def build(self):
   
        with codecs.open(self.args.target, 'w+', 'utf-8') as self.target:
            with codecs.open(self.template_path, 'r', 'utf-8') as self.template:

                self.copy_template_header()
                self.insert_title()
                for group in handbook_group_order:
                    self.insert_group(group)
                self.insert_closing()
                self.copy_template_footer()

    def copy_template_header(self):
        for line in self.template:
            if line.strip() == self.CONTENT_MARKER:
                break
            else: 
                self.target.write(line)

    def copy_template_footer(self):
        for line in self.template:
            self.target.write(line)

    def insert_title(self):
        self._start_section()
        self._start_slide()
        self._copy_markdown(self.source, 'title.md')
        self._end_slide()
        self._end_section()

    def insert_closing(self):
        self._start_section()
        self._start_slide()
        self._copy_markdown(self.source, 'closing.md')
        self._end_slide()
        self._end_section()

    def insert_group(self, group):
        folder = os.path.join(self.source, make_pathname(group))
        
        self._start_section()
        
        self._start_slide()
        self._copy_markdown(folder, 'index.md')
        self._end_slide()
        
        for pattern in sorted(s3_patterns[group]):
            self._start_slide()
            self._copy_markdown(folder, '%s.md' % make_pathname(pattern))
            self._end_slide()
        
        self._end_section()

    def _start_section(self):    
        self.target.write('<section>')

    def _end_section(self):    
        self.target.write('</section>')

    def _start_slide(self):
        self.target.write('<section data-markdown>')
        self.target.write('<script type="text/template">')

    def _end_slide(self):
        self.target.write('</script>')
        self.target.write('</section>')

    def _copy_markdown(self, folder, name):
        with codecs.open(os.path.join(folder, name), 'r', 'utf-8') as section:
            convert_to_reveal(section, self.target)


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


def increase_headline_level(line):
    line = '#' + line
    if line.endswith('#'):
        line = line + '#'
    return line


SLIDE_START = """
<section data-markdown>
    <script type="text/template">
"""

SLIDE_END = """    
    </script>
</section>
"""

IMG_TEMPLATE = '![](%s)'
IMG_PATTERN = re.compile("\!\[(.*)\]\((.*)\)")
FLOATING_IMAGE = Template("""<img class="float-right" src="$url" width="50%" />""")

def convert_to_reveal(source, target):
    lw = LineWriter(target, source.newlines)
    for line in source:
        l = line.strip()    
        if not l:
            lw.mark_empty_line()
        elif l == '---':
            lw.write(SLIDE_END)
            lw.write(SLIDE_START)
            # omit line, do not change empty line marker!
            pass 
        elif l.startswith('##'):
            lw.write(increase_headline_level(l))
        elif line.lstrip().startswith("!["):
            # fix image
            m = IMG_PATTERN.match(l)
            lw.write(convert_image(m.group(1), m.group(2)))
        else:
            lw.write(line)


def convert_image(format, img_url):
    """Replace floating images with img tag, pass all others."""
    # TODO: convert background images (needs two pass and buffer)
    format = format.lower()
    if 'right' in format:
        return FLOATING_IMAGE.substitute(url=img_url)
    else:
        return '![](%s)' % img_url
