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
        from raidoc.build import build
        build(dest=args.dest)

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

