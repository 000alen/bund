from bund import process_files, __version__, is_package
import argparse
import os
import sys

from bund.typings import CFG


def parse_args() -> CFG:
    parser = argparse.ArgumentParser()
    parser.add_argument("packages", nargs="+")
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument("-o", "--outfile", nargs="?",
                        type=argparse.FileType("w"),
                        default=sys.stdout)
    parser.add_argument("--set-except", default=None, dest="set_hook",
                        action="store_true")
    parser.add_argument("--no-except", default=None, dest="set_hook",
                        action="store_false",)
    parser.add_argument("-d", "--default-pkg", default=None,
                        dest="default_package")
    cfg = parser.parse_args()
    if cfg.default_package is None:
        def_file = cfg.packages[0] if len(cfg.packages) == 1 else ""
        cfg.default_package = def_file
    return cfg


def validate_args(cfg):
    missing = False
    for package in cfg.packages:
        if not is_package(package):
            sys.stderr.write("ERROR: %s is not a python package" % package)
            missing = True
    if missing:
        sys.exit(1)

    if cfg.default_package:
        if cfg.default_package not in cfg.packages:
            sys.stderr.write("ERROR: %s is not a valid default package" %
                             cfg.default_pkg)
            sys.exit(2)
        cfg.default_package = os.path.split(cfg.default_package)[1]


cfg = parse_args()
validate_args(cfg)
process_files(cfg)
