# Copyright (C) 2018 The Board of Trustees of the Leland Stanford Junior
# University.
# Copyright (C) 2016-2018 Vanessa Sochat.

# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
# License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import json
import tempfile
import os
import re
import sys

from spython.logger import bot
from spython.utils import ( read_file, write_file )
from spython.main.parse.converters import (
    create_runscript,
    create_section,
    docker2singularity,
    singularity2docker
)


class Recipe(object):
    '''a recipe includes an environment, labels, runscript or command,
       and install sequence. This object is subclassed by a Singularity or
       Docker recipe, and can be used to convert between the two. The user
       can read in one recipe type to convert to another, or provide raw
       commands and metadata for generating a recipe.

       Parameters
       ==========
       recipe: the original recipe file, parsed by the subclass either
               DockerRecipe or SingularityRecipe

    '''

    def __init__(self, recipe=None):
        self.recipe = recipe           # the recipe file
        self._run_checks()             # does the recipe file exist?
        self.parse()


    def __str__(self):
        ''' show the user the recipe object, along with the type. E.g.,
       
            [spython-recipe][docker]
            [spython-recipe][singularity]

        '''

        base = "[spython-recipe]"
        if self.recipe:
            base = "%s[%s]" %(base, self.recipe)
        return base

    def __repr__(self):
        return self.__str__()


    def _run_checks(self):
        '''basic sanity checks for the file name (and others if needed) before
           attempting parsing.
        '''
        if self.recipe is not None:

            # Does the recipe provided exist?
            if not os.path.exists(self.recipe):
                bot.error("Cannot find %s, is the path correct?" %self.recipe)
                sys.exit(1)

            # Ensure we carry fullpath
            self.recipe = os.path.abspath(self.recipe)


# Parse

    def parse(self):
        '''parse is the base function for parsing the recipe, whether it be
           a Dockerfile or Singularity recipe. The recipe is read in as lines,
           and saved to a list if needed for the future. If the client has
           it, the recipe type specific _parse function is called.

           Instructions for making a client subparser:

               It should have a main function _parse that parses a list of lines
               from some recipe text file into the appropriate sections, e.g.,
               
               self.fromHeader
               self.environ
               self.labels
               self.install
               self.files
               self.test
               self.entrypoint

        '''

        self.cmd = None
        self.comments = []
        self.entrypoint = None
        self.environ = []
        self.files = []
        self.install = []
        self.labels = []
        self.ports = []
        self.test = None
        self.volumes = []

        if self.recipe:

            # Read in the raw lines of the file
            self.lines = read_file(self.recipe)

            # If properly instantiated by Docker or Singularity Recipe, parse
            if hasattr(self, '_parse'):
                self._parse()


# Convert and Save


    def save(self, output_file=None, 
                   convert_to=None, 
                   runscript="/bin/bash",
                   force=False):

        '''save will convert a recipe to a specified format (defaults to the
           opposite of the recipe type originally loaded, (e.g., docker-->
           singularity and singularity-->docker) and write to an output file,
           if specified. If not specified, a temporary file is used.

           Parameters
           ==========
           output_file: the file to save to, not required (estimates default)
           convert_to: can be manually forced (docker or singularity)
           runscript: default runscript (entrypoint) to use
           force: if True, override discovery from Dockerfile

        '''

        converted = self.convert(convert_to, runscript, force)
        if output_file is None:
            output_file = self._get_conversion_outfile(convert_to=None)
        bot.info('Saving to %s' %output_file)
        write_file(output_file, converted)
        

    def convert(self, convert_to=None, 
                      runscript="/bin/bash", 
                      force=False):

        '''This is a convenience function for the user to easily call to get
           the most likely desired result, conversion to the opposite format.
           We choose the selection based on the recipe name - meaning that we
           perform conversion with default based on recipe name. If the recipe
           object is DockerRecipe, we convert to Singularity. If the recipe
           object is SingularityRecipe, we convert to Docker. The user can
           override this by setting the variable convert_to

           Parameters
           ==========
           convert_to: can be manually forced (docker or singularity)
           runscript: default runscript (entrypoint) to use
           force: if True, override discovery from Dockerfile

        '''
        converter = self._get_converter(convert_to)
        return converter(runscript=runscript, force=force)



# Internal Helpers


    def _get_converter(self, convert_to=None):
        '''see convert and save. This is a helper function that returns 
           the proper conversion function, but doesn't call it. We do this
           so that in the case of convert, we do the conversion and return
           a string. In the case of save, we save the recipe to file for the 
           user.

           Parameters
           ==========
           convert_to: a string either docker or singularity, if a different

           Returns
           =======
           converter: the function to do the conversion

        '''
        conversion = self._get_conversion_type(convert_to)

        # Perform conversion
        if conversion == "singularity":
            return self.docker2singularity
        return self.singularity2docker



    def _get_conversion_outfile(self, convert_to=None):
        '''a helper function to return a conversion temporary output file
           based on kind of conversion

           Parameters
           ==========
           convert_to: a string either docker or singularity, if a different

        '''
        conversion = self._get_conversion_type(convert_to)
        prefix = "Singularity"
        if conversion == "docker":
            prefix = "Dockerfile"
        suffix = next(tempfile._get_candidate_names())
        return "%s.%s" %(prefix, suffix)



    def _get_conversion_type(self, convert_to=None):
        '''a helper function to return the conversion type based on user 
           preference and input recipe.

           Parameters
           ==========
           convert_to: a string either docker or singularity (default None)

        '''
        acceptable = ['singularity', 'docker']

        # Default is to convert to opposite kind
        conversion = "singularity"
        if self.name == "singularity":
            conversion = "docker"

        # Unless the user asks for a specific type
        if convert_to is not None and convert_to in acceptable:
            conversion = convert_to
        return conversion



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


    def _clean_line(self, line):
        '''clean line will remove comments, and strip the line of newlines 
           or spaces.

           Parameters
           ==========
           line: the string to parse into parts

           Returns
           =======
           line: a cleaned line

        '''
        # A line that is None should return empty string
        line = line or ''
        return line.split('#')[0].strip()


    def _write_script(path, lines, chmod=True):
        '''write a script with some lines content to path in the image. This
           is done by way of adding echo statements to the install section.

           Parameters
           ==========
           path: the path to the file to write
           lines: the lines to echo to the file
           chmod: If true, change permission to make u+x

        '''
        if len(lines) > 0:
            lastline = lines.pop()
        for line in lines:
            self.install.append('echo "%s" >> %s' %path)
        self.install.append(lastline)     

        if chmod is True:
            self.install.append('chmod u+x %s' %path)

Recipe.docker2singularity = docker2singularity
Recipe.singularity2docker = singularity2docker
Recipe._create_section = create_section
Recipe._create_runscript = create_runscript
