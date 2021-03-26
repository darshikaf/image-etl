#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
etl

Usage:
    etl start
        (--src-path=<source-path>)
        (--dest-path=<destination-path>)
    etl -h | --help
    etl --version

Options:
    -h --help                           Show this screen.
    --src-path                          Path to the source directory.
    --dest-path                         Path to write output.
    --version                           Shows version.
Help:
    Please refer to https://github.com/darshikaf/image-etl for more information.
"""

from docopt import docopt

from etl import __version__
from etl.extract import DataBunch

import sys
from typing import List, TextIO


def main():
    options = docopt(__doc__, version=__version__)
    src_path = options.get("--src-path")
    dest_path = options.get("--dest-path")
    data_bunch = DataBunch(src_path, dest_path)
    data_bunch.execute()

