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

from bplate import core

import click
import pathlib
import shutil
import os
import json


@click.group()
def cli():
    pass


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
    cfg_path = os.path.join(target, 'bplate_config.json')

    if os.path.exists(cfg_path):
        click.secho('bplate_config.json found in root directory, opening.')
        try:
            with open(cfg_path, 'r') as f:
                config = json.loads(f.read())
        except Exception as f:
            raise core.click_error('Failed to load blate_config.json. The file may be malformed or not openable.')
        else:
            name = config.get('name')
            if name:
                click.secho('Config successfully loaded.')
    if not name:
        if config:
            click.secho('Failed to get boilerplate from bplate_config.json')
        name = click.prompt('[i] Boilerplate name')

    assert name is not None
    data = boilerplates.joinpath(name)

    if data.exists():
        msg = click.style('[!] Another boilerplate with name %r exists, Overwrite?', fg='red', bold=True)
        click.confirm(msg, abort=True)
        shutil.rmtree(data)

    if config is None:
        click.echo('Creating bplate_config.json...')
        with open(cfg_path, 'w') as f:
            json.dump({'name': name}, f, indent=4)

    click.secho('Copying files from %s to %s...' % (target, data))
    data.mkdir()

    files_copied = 0

    for root, _, files in os.walk(target):
        for name in files:
            if name in core.IGNORED_FILES:
                continue
            
            # root contains the name of target directory as well
            # we only need the names of subdirectories so we will
            # remove the first part of the path.
            parts = list(pathlib.Path(root).parts)
            parts.pop(0)  # remove the root (target) directory name

            target_path = os.path.join(root, name)
            data_path = os.path.join(data, *parts)

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
    bp_path = os.path.join(target, name)
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
        if not os.path.exists(os.path.join(item, 'bplate_config.json')):
            continue

        click.secho(f'* {item.name}')
        count += 1

    click.secho(f'\n{count if count > 0 else "No"} boilerplates listed.', bold=True, fg='blue')


if __name__ == '__main__':
    cli()
