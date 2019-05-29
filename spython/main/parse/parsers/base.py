
# Copyright (C) 2017-2019 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

from spython.logger import bot
from spython.utils import read_file
from ..recipe import Recipe

class ParserBase(object):
    '''a parser Base is intended to provide helper functions for a parser,
       namely to read lines in files, and otherwise interact with outputs.
       Input should be some recipe (text file to describe a container build)
       and output of parse() is a Recipe (spython.main.parse.recipe.Recipe)
       object, which can be used to write to file, etc.
    '''

    lines = []

    def __init__(self, filename=None, load=True):
        '''a generic recipe parser holds the original file, and provides 
           shared functions for interacting with files. If the subclass has
           a parse function defined, we parse the filename

           Parameters
           ==========
           recipe: the recipe file to parse.

        '''
        self.filename = filename
        self._run_checks()
        self.recipe = Recipe(self.filename)

        if self.filename and load is True:

            # Read in the raw lines of the file
            self.lines = read_file(self.filename)

            # If parsing function defined, parse the recipe
            if hasattr(self, 'parse'):
                self.parse()


    def _run_checks(self):
        '''basic sanity checks for the file name (and others if needed) before
           attempting parsing.
        '''
        if self.recipe is not None:

            # Does the recipe provided exist?
            if not os.path.exists(self.recipe):
                bot.exit("Cannot find %s, is the path correct?" % self.recipe)

            # Ensure we carry fullpath
            self.recipe = os.path.abspath(self.recipe)


# Printing

    def __str__(self):
        ''' show the user the recipe object, along with the type. E.g.,
       
            [spython-parser][docker]
            [spython-parser][singularity]

        '''
        base = "[spython-parser]"
        if hasattr(self, 'name'):
            base = "%s[%s]" %(base, self.name)
        return base

    def __repr__(self):
        return self.__str__()


# Lines

    def _split_line(self, line):
        '''clean a line to prepare it for parsing, meaning separation
           of commands. We remove newlines (from ends) along with extra spaces.

           Parameters
           ==========
           line: the string to parse into parts
    
           Returns
           =======
           parts: a list of line pieces, the command is likely first

        '''
        return [x.strip() for x in line.split(' ', 1)]
