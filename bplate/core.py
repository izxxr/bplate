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

from typing import Optional, Dict, Any, List
from dataclasses import dataclass

import os
import json
import click
import pathlib

__all__ = (
    'DEFAULT_IGNORED_FILES',
    'DEFAULT_IGNORED_INIT_FILES',
    'BoilerplateInfo',
    'ensure_bplate_data_dir',
    'click_error',
)


DEFAULT_IGNORED_FILES = (
    '.git/',
    '__pycache__/',
)

DEFAULT_IGNORED_INIT_FILES = (
    'bplate_config.json',
)


@dataclass
class BoilerplateConfig:
    """The boilerplate's configuration from bplate_config.json."""

    name: str
    description: Optional[str] = None
    author: Optional[str] = None
    version: Optional[str] = None
    url: Optional[str] = None
    ignore_files: Optional[List[str]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> BoilerplateConfig:
        """Constructs a boilerplate config from the given """
        return BoilerplateConfig(
            name=data['name'],
            description=data.get('description'),
            author=data.get('author'),
            version=data.get('version'),
            url=data.get('url'),
            ignore_files=data.get('ignore_files'),
        )


@dataclass
class BoilerplateInfo:
    """Holds information about a boilerplate."""

    name: str
    data_path: pathlib.Path
    config_data: Dict[str, Any]
    config: BoilerplateConfig = None  # type: ignore  # late binding

    def __post_init__(self) -> None:
        self.config = BoilerplateConfig.from_dict(self.config_data)


def ensure_bplate_data_dir(subdir: Optional[str] = None) -> pathlib.Path:
    """Ensures that the .bplate-data directory or subdirectory exists.

    When subdir parameter is not given, returns the `pathlib.Path` instance
    for the ~/.bplate-data directory otherwise path for the given subdirectory.
    """
    pathstr = os.path.expanduser(os.path.join('~', f'.bplate-data'))
    if subdir:
        pathstr = os.path.join(pathstr, subdir)

    path = pathlib.Path(pathstr)
    if path.exists():
        return path

    os.makedirs(pathstr + os.path.sep)
    return path


def click_error(message: str, *, warn: bool = False) -> click.ClickException:
    """Returns a `click.ClickException` instance with styled message.

    If warn is True, the message foreground is orange instead of red.
    """
    fg = 'orange' if warn else 'red'
    return click.ClickException(click.style(message, fg=fg, bold=True))


def get_boilerplate_info(name: str) -> BoilerplateInfo:
    """Returns `BoilerplateInfo` for a boilerplate.

    This should be called inside a command context in order to properly propagate
    the raised `click.ClickException` to user.
    """
    target = ensure_bplate_data_dir('boilerplates')
    data_path = pathlib.Path(os.path.join(target, name))
    cfg_path = os.path.join(data_path, 'bplate_config.json')

    if not os.path.exists(cfg_path):
        raise click_error('No boilerplate with name %r exists.' % name)

    try:
        with open(cfg_path, 'r') as f:
            config = json.loads(f.read())
    except Exception as f:
        raise click_error('Failed to load bplate_config.json. The file may be malformed or not openable.')
    else:
        if not 'name' in config:
            raise click_error('No name entry found in bplate_config.json')
        return BoilerplateInfo(name=config['name'], data_path=data_path, config_data=config)
