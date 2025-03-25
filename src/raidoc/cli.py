"""
cli.py: Command-line interface to RAIDOC
"""

import argparse
from pathlib import Path

ACTION_BUILD = 'build'

def cli():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )

    subparsers = parser.add_subparsers(
        title='Action',
        dest='action',
        description='Which action to perform',
        )

    _add_build_action(subparsers)

    args = parser.parse_args()

    if args.action == ACTION_BUILD:
        #from raidoc.build import build
        #build(dest=args.dest)
        from raidoc.builder import Builder
        from raidoc.getdeps import getdeps

        builder = Builder(Path('./doc'))
        builder._prepass()
        for page in builder.pages:
            if page.path is None:
                # FIXME hack for autogen
                continue
            builder._render_page(page)

        builder.render(Path('./build'))

        Path('./build/dep').mkdir(exist_ok=True)
        getdeps(Path('./doc/dep'), Path('./build/dep'))

    else:
        # This should never happen, since
        # argparse validates this.
        parser.error('Unknown action')

def _add_build_action(subparsers):
    """Setup parsers for 'build' action."""
    parser_build = subparsers.add_parser(
        ACTION_BUILD,
        )

    parser_build.add_argument(
        'dest',
        type=Path,
        help='Output directory',
        default='./build',
        nargs='?'
        )

