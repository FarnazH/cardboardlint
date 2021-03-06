# -*- coding: utf-8 -*-
# Cardboardlint is a cheap lint solution for pull requests.
# Copyright (C) 2011-2017 The Cardboardlint Development Team
#
# This file is part of Cardboardlint.
#
# Cardboardlint is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# Cardboardlint is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
# --
"""Linter for import conventions.

This script counts the number of bad imports. The following is not allowed in a package:

* Importing from its own package as follows:

  .. code-block:: python

        from package import foo
"""
from __future__ import print_function

import codecs

from cardboardlint.common import Message, matches_filefilter, flag


__all__ = ['linter_import']


DEFAULT_CONFIG = {
    # Filename filter rules
    'filefilter': ['- */test_*.py', '+ *.py', '+ *.pyx'],
    # Names of python packages in the project (no longer searched automatically).
    'packages': [],
}


@flag(static=True, python=True)
def linter_import(linter_config, files_lines):
    """Linter for checking import statements.

    Parameters
    ----------
    linter_config : dict
        Dictionary that contains the configuration for the linter
    files_lines : dict
        Dictionary of filename to the set of line numbers (that have been modified).
        See `run_diff` function in `carboardlinter`.

    Returns
    -------
    messages : list
        The list of messages generated by the external linter.

    """
    config = DEFAULT_CONFIG.copy()
    config.update(linter_config)

    # Get all relevant filenames
    filenames = [filename for filename in files_lines
                 if matches_filefilter(filename, config['filefilter'])]

    # Loop all python and cython files
    messages = []
    if len(config['packages']) > 0:
        for filename in filenames:
            # Look for bad imports
            with codecs.open(filename, encoding='utf-8') as f:
                for lineno, line in enumerate(f):
                    for package in config['packages']:
                        # skip version import
                        if line == u'from {0} import __version__\n'.format(package):
                            continue
                        if u'from {0} import'.format(package) in line:
                            text = 'Wrong import from {0}'.format(package)
                            messages.append(Message(filename, lineno+1, None, text))
    return messages
