from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from jumpdir.directories import Directories
from jumpdir.pathfinder import PathFinder
from jumpdir.bookmarks import Bookmarks

import argparse
import os
import sys

HOME = os.getenv('HOME')
BOOKMARKS = os.path.join(HOME, '.jdbookmarks.json')


def parse_args(args):
    "Parse list/tuple of arguments with argparse module"
    parser = argparse.ArgumentParser(description='jumpdir')
    subparsers = parser.add_subparsers(help='sub-command help', dest='commands')

    # jumpdir search ...
    parser_search = subparsers.add_parser('search',
                                          help='search home directory for a directory matching given search term'
                                          )
    parser_search.add_argument('search_term', help='directory name to search for (case insensitive).',)
    parser_search.set_defaults(which='search')

    # jumpdir add ...
    parser_add = subparsers.add_parser('add', help='add bookmark')
    parser_add.add_argument('name', help='name of bookmark to add')
    parser_add.add_argument('-p', '--path', default=os.getcwd(),
                            help="define path that bookmark points to"
                            )

    # jumpdir delete ...
    parser_delete = subparsers.add_parser('delete', help='delete bookmark')
    parser_delete.add_argument('name',
                               help='name of bookmark to remove'
                               )

    # jumpdir list ...
    parser_list = subparsers.add_parser('list', help='list saved bookmarks')

    return parser.parse_args(args)


def main(argv=sys.argv[1:]):
    args = parse_args(argv)
    bm = Bookmarks(BOOKMARKS)

    # Sub command logic
    if not args.commands:
        raise ValueError("jumpdir: error: no command given")
    elif args.commands == 'add':
        bm.add_bookmark(args.name)
    elif args.commands == 'delete':
        bm.del_bookmark(args.name)
    elif args.commands == 'list':
        bm.list_bookmarks()
    elif args.commands == 'search':
        pass

    if args.search_term == HOME:
        return HOME

    search_term = args.search_term
    pfinder = PathFinder(search_term)

    # Search through bookmarks
    for dname in bm:
        if pfinder.check_match(dname):
            return bm[dname]

    # Search through home folder
    ddict = Directories(HOME)
    for dname in ddict:
        if pfinder.check_match(dname):
            return ddict.shallowest_path_to(dname)

if __name__ == '__main__':
    main()
