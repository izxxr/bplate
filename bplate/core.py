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

from typing import Optional

import os
import click
import pathlib

__all__ = (
    'DEFAULT_IGNORED_FILES',
    'DEFAULT_IGNORED_INIT_FILES',
    'ensure_bplate_data_dir',
    'click_error',
)


DEFAULT_IGNORED_FILES = (
    '.git',
)
DEFAULT_IGNORED_INIT_FILES = (
    'bplate_config.json',
)


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
