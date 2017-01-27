# -*- coding: utf-8 -*-
import glob
from contextlib import contextmanager
from tempfile import NamedTemporaryFile

import click


click.disable_unicode_literals_warning = True


@click.group('code-standards')
def main():
    pass


@main.command()
@click.argument('path')
def apply(path):
    isort(path)
    autoflake(path)
    autopep8(path)


@main.command()
@click.argument('path')
def isort(path):
    import os
    from isort.main import main as isort_main

    click.echo('code-standards apply')
    click.echo('isort')
    isort_args = [
        #'--verbose',
        '-m3',
        '-l120',
        #'--order-by-type',
        #'--combine-as',
        #'--force-alphabetical-sort-within-sections',
        #'--force-alphabetical-sort',
        #'--force-sort-within-sections',
        #'--lines-between-types=1',
        #'--atomic',
        #'-y',
        path,
    ]
    if os.path.isdir(path):
        isort_args.insert(0, '--recursive')
    call_main(isort_main, *isort_args)


@main.command()
@click.argument('path')
def autoflake(path):
    import os

    click.echo('autoflake')
    from autoflake import main as autoflake_main
    autoflake_args = [
        '-i',
        '--remove-all-unused-imports',
        path
    ]
    if os.path.isdir(path):
        autoflake_args.insert(0, '--recursive')
    call_main(autoflake_main, *autoflake_args)


@main.command()
@click.argument('path')
def autopep8(path):
    import os

    click.echo('autopep8')
    from autopep8 import main as autopep8_main
    autopep8_args = [
        '-a',
        '-i',
        '--max-line-length=120',
        path
    ]
    if os.path.isdir(path):
        autopep8_args.insert(0, '--recursive')
    call_main(autopep8_main, *autopep8_args)


def call_main(func, *argv):
    import sys
    old_argv = sys.argv
    sys.argv = [''] + list(argv)
    try:
        return func()
    finally:
        sys.argv = old_argv

