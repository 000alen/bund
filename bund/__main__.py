from io import StringIO
from typing import Optional, TypedDict
from bund import bundle
import argparse
import sys


class Args(TypedDict):
    packages: list[str]
    default_package: str
    outfile: StringIO
    set_hook: Optional[bool]


parser = argparse.ArgumentParser()
parser.add_argument(
    "packages",
    nargs="+"
)
parser.add_argument(
    "-o",
    "--outfile",
    nargs="?",
    type=argparse.FileType("w"),
    default=sys.stdout
)
parser.add_argument(
    "--set-except",
    default=None,
    dest="set_hook",
    action="store_true"
)
parser.add_argument(
    "--no-except",
    default=None,
    dest="set_hook",
    action="store_false"
)
parser.add_argument(
    "-d",
    "--default-pkg",
    default=None,
    dest="default_package"
)

args: Args = parser.parse_args()
if args.default_package is None:
    args.default_package = args.packages[0]


bundle(args.packages, args.default_package, args.outfile, args.set_hook)
