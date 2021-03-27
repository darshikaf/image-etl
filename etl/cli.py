#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click

from etl import __version__
from etl.execute import Configuration, Executor


@click.group()
@click.version_option(__version__)
def cli() -> None:
    """
  This is a simple CLI tool for extracting, tranforming and loading image data.
  Please refer to https://github.com/darshikaf/image-etl/blob/master/README.md for installation and usage instructions.

  ARGS: src dest

  EXAMPLE: etl start <src-path> <dest-path>
    
  """
    pass


@cli.command(help="Starts ETL process.")
@click.argument("src", metavar="<src>", type=click.Path(exists=True))
@click.argument("dest", metavar="<dest>", type=click.Path(exists=False))
def start(src, dest) -> None:
    """etl start <src> <dest>"""
    executor = Executor(Configuration(src, dest))
    executor.execute()


def main() -> None:
    cli()

