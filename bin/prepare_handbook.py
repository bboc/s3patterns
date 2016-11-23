#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import shutil
from functools import partial 

from s3_patterns import s3_patterns, handbook_group_order, all_patterns
from config import additional_texts_for_handbook
from common import make_pathname, make_title, create_directory
from convert_jekyll_files import copy_and_fix_headlines


def prepare_handbook(args):
    """Prepare all source files so handbook can be compiled through mmd/latex and pandoc/epub."""
    patterns = all_patterns()
    
    ## build filename lookup
    pattern_filename_lookup = {make_pathname(pattern): pattern for pattern in patterns}
    refcon = partial(reference_converter, pattern_filename_lookup)


    dst_dir = os.path.join('handbook', 'tmp')

    create_directory(dst_dir)
    if set(handbook_group_order) != set(s3_patterns.keys()):
        raise Exception(
            "ERROR: Handbook group order does not reflect actual pattern groups!")

    convert_and_copy_all_files_to_tmp(dst_dir, patterns, refcon)
    create_master_file_with_all_patterns(dst_dir)


def reference_converter(pattern_filename_lookup, text, target):
    """Convert links to markdown files to cross-references. If the link matches 
    the text, return '[]', otherwise return the '[pattern title]'."""
    pattern = pattern_filename_lookup[target[1:-6]]
    if text == make_title(pattern):
        return "[]"
    else:
        return "[%s]" % make_title(pattern)


def convert_and_copy_all_files_to_tmp(dst_dir, patterns, refcon):
    """
    Copy all pattern and group--content files to handbook/tmp, 
    convert front matter title to headline, adapt all headline levels as required
    and process cross-reference links.
    """
    for pattern in patterns:
        copy_and_fix_headlines(dst_dir, '%s.md' % make_pathname(pattern), 3, reference_converter=refcon)

    for group in sorted(s3_patterns.keys()):
        copy_and_fix_headlines(
            dst_dir, '%s--content.md' % make_pathname(group), 2, reference_converter=refcon)

    for (filename, headline_level) in additional_texts_for_handbook: 
        copy_and_fix_headlines(dst_dir, filename, headline_level, reference_converter=refcon)


def create_master_file_with_all_patterns(dst_dir):
    """Create tmp/patterns--master.md with transcludes for all groups and their patterns."""
    with file(os.path.join(dst_dir, 'patterns--master.md'), 'w+') as fp:
        for group in handbook_group_order:
            fp.write('\n\n{{%s--content.md}}\n' % make_pathname(group))
            for pattern in s3_patterns[group]:
                fp.write('\n{{%s.md}}\n' % make_pathname(pattern))


if __name__ == "__main__":



    # setup argparse
    parser = argparse.ArgumentParser(
        description='copy and prepare markdown files for compiling the handbook.')
    parser.add_argument('--verbose', '-v', action='count')

    args = parser.parse_args()
    prepare_handbook(args)
