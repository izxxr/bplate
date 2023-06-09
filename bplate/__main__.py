# MIT License

# Copyright (c) 2023 I. Ahmad

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import annotations

from typing import Set, List
from bplate import core, __version__

import click
import pathlib
import shutil
import os
import platform
import json


@click.group()
def cli():
    pass

@cli.command('version')
@click.option('--all', is_flag=True, default=False, help="Show other information about bplate and user's machine.")
def version(all: bool):
    if not all:
        click.echo(__version__)
        return
    
    click.echo(f'Version: {__version__}')
    click.echo(f'Platform: {platform.platform()} {platform.architecture()[0]}')

@cli.command()
@click.argument('path', type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True))
def new(path: str):
    """Creates and stores a new boilerplate template.

    The boilerplate template will be available for later usage
    using the `bplate init` command.

    The PATH argument is the path where boilerplate code is located. The provided
    path must point to a readable directory and not a file.
    """
    click.secho('Creating new boilerplate...')

    boilerplates = core.ensure_bplate_data_dir('boilerplates')
    target = pathlib.Path(path)

    name = None
    config = None
    cfg_path = target / 'bplate_config.json'

    if os.path.exists(cfg_path):
        click.secho('bplate_config.json found in root directory, opening.')
        try:
            with open(cfg_path, 'r') as f:
                config = json.loads(f.read())
        except Exception as f:
            raise core.click_error('Failed to load bplate_config.json. The file may be malformed or not openable.')
        else:
            name = config.get('name')
            if name:
                click.secho('Config successfully loaded.')
    if not name:
        if config:
            click.secho('Failed to get boilerplate name from bplate_config.json')
        name = click.prompt('[i] Boilerplate name')

    assert name is not None
    data = boilerplates.joinpath(name)

    if data.exists():
        msg = click.style('[!] Another boilerplate with name %r exists, Overwrite?' % name, fg='red', bold=True)
        click.confirm(msg, abort=True)
        shutil.rmtree(data)

    if config is None:
        click.echo('Creating bplate_config.json...')
        config = {'name': name}
        with open(cfg_path, 'w') as f:
            json.dump(config, f, indent=4)

    click.secho('Copying files from %s to %s...' % (target, data))
    data.mkdir()

    files_copied = 0
    ignored_patterns: Set[str] = set(config.get('ignore_patterns', []))
    dest = config.get('dest')

    if dest:
        target = target.joinpath(dest)
        if not target.exists():
            raise core.click_error(f'The path {target} does not exist.')

    for root, _, files in os.walk(target):
        for name in files:
            file_path = pathlib.Path(os.path.join(root, name))
            if any(file_path.match(pat) for pat in ignored_patterns):
                continue

            dest_parts = list(pathlib.Path(dest).parts) if dest else []

            # root contains the name of target directory as well
            # we only need the names of subdirectories so we will
            # remove the first part of the path.
            root_parts = list(pathlib.Path(root).parts)
            root_parts.pop(0)  # remove the root (target) directory name

            # this piece of code changes data path to point to the
            # directory provided by "dest" config option.
            to_remove: List[str] = [part for part in dest_parts if part in root_parts]
            for part in to_remove:
                root_parts.remove(part)

            target_path = os.path.join(root, name)
            data_path = data.joinpath(*root_parts)

            if not os.path.exists(data_path):
                os.makedirs(data_path)

            shutil.copy2(target_path, os.path.join(data_path, name))
            files_copied += 1

    click.secho(f'Successfully copied {files_copied} files.')

    if config is None:
        click.secho('[i] A "bplate_config.json" file has been created in root directory that ' \
                    'can be edited to customize the information and generation config of boilerplate.',
                    fg='blue')

    click.secho('[!] Boilerplate created successfully.\n', fg='green')


@cli.command('delete')
@click.argument('name')
def delete(name: str):
    """Deletes a boilerplate.

    The argument NAME represents the name of boilerplate that is
    being deleted.
    """
    target = core.ensure_bplate_data_dir('boilerplates')
    bp_path = target / name
    if not os.path.exists(bp_path):
        raise core.click_error('No boilerplate with name %r exists.' % name)

    click.confirm('This action is irreversible, are you sure you want to proceed?', abort=True)
    click.secho('Deleting boilerplate files...', fg='blue')
    shutil.rmtree(bp_path)

    click.secho('[!] Deleted boilerplate %r successfully.' % name, fg='green')


@cli.command('list')
def list_():
    """Shows the list of all available boilerplates."""
    target = core.ensure_bplate_data_dir('boilerplates')
    count = 0

    for item in target.iterdir():
        if not item.is_dir() or item.name.startswith('_'):
            continue
        if not os.path.exists(item / 'bplate_config.json'):
            continue

        click.secho(f'* {item.name}')
        count += 1

    click.secho(f'\n{count if count > 0 else "No"} boilerplates listed.', bold=True, fg='blue')

@cli.command('init')
@click.argument('name')
@click.argument('path', type=click.Path(file_okay=False, dir_okay=True, readable=True))
def init(name: str, path: str):
    """Generates the boilerplate at the given path.

    The argument NAME represents the name of boilerplate to generate
    and PATH represents the location where it should be generated.

    If the directory that PATH points do doesn't exist, it will
    be created.
    """
    click.echo('Initializing boilerplate...')
    boilerplate = core.get_boilerplate_info(name)

    if not os.path.exists(path):
        click.secho('Creating target directory...')
        os.makedirs(path)

    click.secho('Copying files...')
    files_copied = 0

    for root, _, files in os.walk(boilerplate.data_path):
        for name in files:
            if name in core.DEFAULT_IGNORED_INIT_FILES:
                continue

            # Get parts from after ".bplate-data/boilerplates/<boilerplate-name>"
            # XXX: This seems like a hack, maybe a better workaround?
            parts = list(pathlib.Path(root).parts)
            parts = parts[parts.index('.bplate-data')+3:]

            target_path = os.path.join(path, *parts)

            if not os.path.exists(target_path):
                os.makedirs(target_path)

            shutil.copy2(os.path.join(root, name), target_path)
            files_copied += 1

    click.secho(f'Copied {files_copied} files successfully.')
    click.secho('[!] Boilerplate has been generated successfully.', fg='green')

@cli.command('show')
@click.argument('name')
def show(name: str):
    """Shows information about a stored boilerplate.

    The NAME argument represents the boilerplate to show information for.
    """
    boilerplate = core.get_boilerplate_info(name)
    cfg = boilerplate.config

    click.secho(f'\n{boilerplate.name}\n', fg='blue')
    click.echo(f'{cfg.description or "No description available"}\n')
    click.echo(f'Author: {cfg.author or "No author available"}')
    click.echo(f'Version: {cfg.version or "No version available"}')
    click.echo(f'URL: {cfg.url or "No URL available"}')

if __name__ == '__main__':
    cli()
