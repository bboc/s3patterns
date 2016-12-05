#!/usr/bin/env python

import argparse
import os
import shutil
import re
import os.path
import sys

from s3_patterns import s3_patterns, all_patterns, handbook_group_order
from config import (
    additional_content_to_export,
    artefacts_to_export, 
    groups_to_rename, 
    MD_FILE_TEMPLATE,
    patterns_to_rename)
from common import make_pathname, make_title, create_directory
from slides import cmd_slides
from convert_jekyll_files import expand_cross_references, replace_references


def cmd_build(args):
    patterns = all_patterns()

    if args.toc:
        build_toc_files(args, patterns)

    if args.skeleton:
        build_skeleton_files(args, patterns, s3_patterns.keys())

    if args.excluded:
        list_excluded_files(args, s3_patterns.keys())

    if args.index:
        generate_index_files()

    if args.graph:
        generate_graph()


def cmd_export(args):
    """Export all content files to a separate folder, optionally suffix with --original."""

    additional_content_to_export = ['introduction', 'changelog']
    artefacts_to_export = [
        '_DROPBOX_WORKFLOW.md',
        '_TODO.md',
        'README.md',
        'S3-patterns-handbook.epub',
        'S3-patterns-handbook.pdf',
    ]
    template = MD_FILE_TEMPLATE
    patterns = all_patterns()
    dst_dir = '_export'

    if args.dropbox == True:
        template = '%s--original.md'

    # clear previous export
    shutil.rmtree(dst_dir, ignore_errors=True)

    create_directory(dst_dir)

    def copy_and_add_suffix(name):
        shutil.copy(MD_FILE_TEMPLATE % name,
                    os.path.join(dst_dir, template % name))

    # copy patterns
    for pattern in patterns:
        copy_and_add_suffix(make_pathname(pattern))

    # copy group content
    for group in sorted(s3_patterns.keys()):
        copy_and_add_suffix('%s--content' % make_pathname(group))

    # copy additional content files
    for item in additional_content:
        copy_and_add_suffix(item)

    if args.dropbox == True:
        # copy images
        shutil.copytree('img', os.path.join(dst_dir, 'img'))
        # copy artefacts
        for item in artefacts:
            shutil.copy(item, dst_dir)


def front_matter(fp, title=''):
    fp.write('---\n')
    if title:
        fp.write('title: %s\n' % title)
    fp.write('---\n\n')


def build_toc_files(args, patterns, root='content-tmp'):
    """(Re-)build all includes with tables of contents."""
    print "writing files to", root
    create_directory(root)

    def write_link(fp, link_title, link_path):
        fp.write("* [%s](%s)\n" % (link_title, link_path))

    def write_toc_include(items, filename, target_prefix=''):
        """Create a table of contents from items and write to filename."""
        with file(filename, 'w+') as fp:
            for item in items:
                write_link(
                    fp, make_title(item), target_prefix+make_pathname(item)+'.html')

    def write_group_master(folder, group):
        gpath = make_pathname(group)
        with file(os.path.join(folder, '%s--master.md' % gpath), 'w+') as fp:
            front_matter(fp, make_title(group))
            fp.write('\n{{%s--content.md}}\n' % gpath)
            fp.write('\n{{%s--toc.md}}\n' % gpath)

    # patterns index
    write_toc_include(patterns, os.path.join(root, 'all-patterns.md'))
    write_toc_include(sorted(s3_patterns.keys()), os.path.join(
        root, 'index--groups--toc.md'))  # groups TOC

    # build a TOC for each group
    for group in sorted(s3_patterns.keys()):
        write_toc_include(sorted(s3_patterns[group]), os.path.join(
            root, '%s--toc.md' % make_pathname(group)))
        write_group_master(root, group)


def build_skeleton_files(args, patterns, groups, root='content-tmp'):
    """Build skeleton content files for groups and patterns."""

    create_directory(root)

    def make_file(filename_root, title_root):
        with file(os.path.join(root, MD_FILE_TEMPLATE % make_pathname(filename_root)), 'w+') as fp:
            front_matter(fp, make_title(title_root))
            fp.write('\n\n...\n')

    # create patterns files
    for pattern in patterns:
        make_file(pattern, pattern)

    # create group content files
    for group in groups:
        make_file('%s--content' % group, group)


def generate_index_files(root='content'):
    """mmd commands to compile index files from masters."""

    print "# patterns index"
    print 'multimarkdown --to=mmd --output=index.md index--master.md\n'

    print "# group indexes"
    for group in sorted(s3_patterns.keys()):
        # output multimarkdown command to create build group index files
        print 'multimarkdown --to=mmd --output=%(group)s.md %(group)s--master.md' % {'group': make_pathname(group)}

def generate_graph():
    for group in handbook_group_order:
        filename = "%s.gv.txt" % make_pathname(group)
        with file(filename, 'w') as dst:
            dst.write('graph {\n')
            #dst.write('digraph "%s" {\n' % make_title(group))
            for pattern in s3_patterns[group]:
                dst.write('"%s" -- "%s"\n' % (make_title(group), make_title(pattern)))
            dst.write("}\n")
            print "neato -Tpng %s -o%s.png" % (filename, make_pathname(group))

def list_excluded_files(args, groups):

    def _print(name, suffix):
        print '\t"%s--%s.md",' % (name, suffix)

    for group in sorted(groups):
        group = make_pathname(group)
        for suffix in ['content', 'toc', 'master']:
            _print(group, suffix)


def cmd_update(args):
    """Update one or more target directories by renaming patterns and pattern groups."""
    print args
    # rename all patterns and groups
    for target in args.target: 
        for root, dirs, files in os.walk(target):
            for filename in files:
                dummy, ext = os.path.splitext(filename)
                if ext == '.md':
                    match_and_rename(root, filename)
    
    print "*" * 80
    print " now you need to fix all titles and then remove the prefix '--'"
    print 
    print "if you run this on the handbook source, remember to:"
    
    print " 1. build --toc"
    print " 2. build --exluded  (for config.yml)"
    print " 3. build --index (for build commands)"
    print " 4. run the build command to refresh everything"
    print " 5. build handbook and website and check everything"
    print " 6. commit"

def match_and_rename(root, filename):
    """Check if filename matches one of the old filenames and rename to new name.

     For patterns check match for:
     - plain filename.md
     - --original.md
     - --draft-*.md

     For groups check match for:
    - plain.md 
    - '--content'
    - '--master'
    --'toc'
    """
    def rename(old_part, new_part):
        new_name = '--%s%s' % (new_part, filename[len(old_part):])
        print "rename", root, filename, '-->', new_name
        os.rename(os.path.join(root, filename),
                  os.path.join(root, new_name))

    GROUP_TEMPLATES = [MD_FILE_TEMPLATE, '%s--master.md', '%s--toc.md']
    GROUP_PREFIX_TEMPLATES = ['%s--content']

    PATTERN_TEMPLATES = [MD_FILE_TEMPLATE]
    PATTERN_PREFIX_TEMPLATES = ['%s--original', '%s--draft']

    def process_class(items_to_rename, full_templates, prefix_templates):

        for old_name, new_name in items_to_rename:
            op = make_pathname(old_name)
            np = make_pathname(new_name)
            for t in full_templates:
                oldname = t % op
                if filename == oldname:
                    rename(op, np)
            for t in prefix_templates:
                prefix = t % op
                if filename.startswith(prefix):
                    rename(op, np)

    process_class(groups_to_rename, GROUP_TEMPLATES, GROUP_PREFIX_TEMPLATES)
    process_class(patterns_to_rename, PATTERN_TEMPLATES, PATTERN_PREFIX_TEMPLATES)


def cmd_references(args):
    """Expand all cross-references [name][] to links that 
    Jekyll understands [name](name.html).
    if args.source is a folder, process all patterns within that folder,
    if it is a file, process that file (regardless of whether it is a pattern
    or not). If folder args.target is given, write output to that folder,
    print to stdout otherwise.
    """
    if os.path.isdir(args.source):
        if not args.target:
            print "please give a target"
            sys.exit(1)
        if not os.path.isdir(args.target):
            print "target", args.target, "is not a directory"
            sys.exit(1)
        for pattern in all_patterns():
            print "processing", pattern
            source_file = os.path.join(args.source, make_pathname(pattern))
            target_file = os.path.join(args.target, make_pathname(pattern))
            expand_cross_references(MD_FILE_TEMPLATE % source_file, 
                                    MD_FILE_TEMPLATE % target_file)
    else:
        with file(args.source, 'r') as source:
            for line in source:
                line = line.rstrip()
                print replace_references(line)


if __name__ == "__main__":

    # setup argparse
    parser = argparse.ArgumentParser(
        description='build files for s3 patterns website and handbooks')

    parser.add_argument('--verbose', '-v', action='count')
    subparsers = parser.add_subparsers()
    build = subparsers.add_parser('build',
                                  help="Helpers for building files and indexes.")
    build.add_argument('--toc', action='store_true',
                       help='(re-)build all includes with tables of contents.')
    build.add_argument('--skeleton', action='store_true',
                       help='build skeleton content files for groups and patterns.')
    build.add_argument('--excluded', action='store_true',
                       help='Create exclude list for _config.yaml.')
    build.add_argument('--index', action='store_true',
                       help='Output commands for generate-index-files.')
    build.add_argument('--graph', action='store_true',
                       help='Output files to generate illustrations.')

    build.set_defaults(func=cmd_build)

    export = subparsers.add_parser('export',
                                   help="Export content files to share on dropbox.")
    export.add_argument('--dropbox', action='store_true',
                        help='Suffix files with "--original", add images and pdf/epub versions.')
    export.set_defaults(func=cmd_export)

    export = subparsers.add_parser('slides',
                        help="Build slide deck.")
    export.add_argument('--skeleton', action='store_true',
                        help='Build skeleton directories and files for slides.')
    export.add_argument('--reveal', action='store_true',
                        help='Build reveal.js presentation.')
    export.add_argument('--deckset', action='store_true',
                        help='Build deckset presentation.')
    export.add_argument('--target', 
                        help='Target file (for reveal.js and deckset builds.')
    export.add_argument('source', 
                        help='Directory for source files.')
    
    export.set_defaults(func=cmd_slides)

    update = subparsers.add_parser('update',
                                   help="Update filenames in one or several locations.")
    update.add_argument('target', nargs='+',
                        help='One or several target folders.')

    update.set_defaults(func=cmd_update)

    references = subparsers.add_parser('references',
                                   help="Expand all cross-references in pattern files.")
    references.add_argument('source',
                        help='Source folder or file.')
    references.add_argument('target', nargs='?', default=None,
                        help='Target folder if source is a folder.')

    references.set_defaults(func=cmd_references)


    args = parser.parse_args()
    args.func(args)
