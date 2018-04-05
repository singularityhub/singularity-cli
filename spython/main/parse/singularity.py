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
import os
import re
import sys

from spython.logger import bot
from spython.utils import read_file
from spython.main.parse.recipe import Recipe


class SingularityRecipe(Recipe):

    def __init__(self, recipe=None):
        '''a Docker recipe parses a Docker Recipe into the expected fields of
           labels, environment, and install/runtime commands

           Parameters
           ==========
           recipe: the recipe file (Dockerfile) to parse

        '''

        self.name = 'singularity'
        self.filename = "Singularity"
        super(SingularityRecipe, self).__init__(recipe)


# Setup for each Parser

    def _setup(self, lines):
        '''setup required adding content from the host to the rootfs,
           so we try to capture with with ADD.
        '''
        bot.warning('SETUP is error prone, please check output.')

        for line in lines:

            # For all lines, replace rootfs with actual root /
            line = re.sub('[$]{?SINGULARITY_ROOTFS}?', 
                          '', '$SINGULARITY_ROOTFS')

            # If we have nothing left, don't continue
            if line in ['', None]:
                continue

            # If the line starts with copy or move, assume is file from host
            if re.search('(^cp|^mv)', line):
                line = re.sub('(^cp|^mv)', '', line)
                self.files.append(line)

            # If it's a general command, add to install routine
            else:
                self.install.append(line)            


# From Parser

    def _from(self, line):
        ''' get the FROM container image name from a FROM line!

           Parameters
           ==========
           line: the line from the recipe file to parse for FROM

        '''
        self.fromHeader = line
        bot.debug('FROM %s' %self.fromHeader) 


# Run and Test Parser



    def _test(self, lines):
        ''' A healthcheck is generally a test command

           Parameters
           ==========
           line: the line from the recipe file to parse for FROM

        '''
        self._write_script('/tests.sh', lines)
        testrun = "/bin/bash /tests.sh"
        self.test = "/bin/bash /tests.sh"
        

# Env Parser

    def _env(self, lines):
        '''env will parse a list of environment lines and simply remove any
           blank lines, or those with export. Dockerfiles don't usually
           have exports.
 
           Parameters
           ==========
           lines: A list of environment pair lines.

        '''
        environ = [x for x in lines if not x.startswith('export')]        
        self.environ += environ


# Files for container


    def _files(self, lines):
        '''parse_files will simply add the list of files to the correct object
 
           Parameters
           ==========
           lines: pairs of files, one pair per line
   
        '''
        self.files += lines


# Comments and Help

    def _comments(self, lines):
         ''' comments is a wrapper for comment, intended to be given a list
             of comments.

             Parameters
             ==========
             lines: the list of lines to parse

         ''' 
         for line in lines:
             comment = self._comment(line)
             self.comments.append(comment)


    def _comment(self, line):
        '''Simply add the line to the install as a comment. Add an extra # to be
           extra careful. 

           Parameters
           ==========
           line: the line from the recipe file to parse to INSTALL

        '''
        return "# %s" % line.strip().strip('#')


# Runscript Command

    def _run(self, lines):
        '''_parse the runscript to be the Docker CMD. If we have one line,
           call it directly. If not, write the entrypoint into a script. 

           Parameters
           ==========
           lines: the line from the recipe file to parse for CMD

        '''
        lines = [x for x in lines if x not in ['', None]]

        # Default runscript is first index
        runscript = lines[0]

        # Multiple line runscript needs multiple lines written to script
        if len(lines) > 1:

            bot.warning('More than one line detected for runscript!')
            bot.warning('These will be echoed into a single script to call.')
            self._write_script('/entrypoint.sh', lines)
            runscript = "/bin/bash /entrypoint.sh"

        self.cmd = runscript


# Labels

    def _labels(self, lines):
        '''_labels simply adds the labels to the list to save.
           
           Parameters
           ==========
           lines: the lines from the recipe with key,value pairs

        '''
        self.labels += lines


    def _post(self, lines):
        '''the main core of commands, to be added to the install section

           Parameters
           ==========
           lines: the lines from the recipe with install commands

        '''        
        self.install += lines


# Main Parsing Functions


    def _get_mapping(self, section):
        '''mapping will take the section name from a Singularity recipe 
           and return a map function to add it to the appropriate place. 
           Any lines that don't cleanly map are assumed to be comments.

           Parameters
           ==========
           section: the name of the Singularity recipe section
    
           Returns
           =======
           function: to map a line to its command group (e.g., install)

        '''

        # Ensure section is lowercase
        section = section.lower()

        mapping = {"environment": self._env,
                   "comments": self._comments,
                   "runscript": self._run,
                   "labels": self._labels,
                   "setup": self._setup,
                   "files": self._files,
                   "from": self._from,
                   "post": self._post,
                   "test": self._test,
                   "help": self._comments}

        if section in mapping:
            return mapping[section]
        return self._comments
 

    def _parse(self):
        '''parse is the base function for parsing the recipe, and extracting
           elements into the correct data structures. Everything is parsed into
           lists or dictionaries that can be assembled again on demand. 
    
           Singularity: we parse files/labels first, then install. 
                        cd first in a line is parsed as WORKDIR

        '''
        # If the recipe isn't loaded, load it
        if not hasattr(self, 'config'):
            self.load_recipe()

        # Parse each section
        for section, lines in self.config.items():
            bot.debug(section)

            # Get the correct parsing function
            parser = self._get_mapping(section)
           
            # Parse it, if appropriate
            if parser:
                parser(lines)



# Loading Functions

    def _load_from(self, line):
        '''load the From section of the recipe for the Dockerfile.
        '''
        # Remove any comments
        line = line.split('#',1)[0]        
        line = re.sub('(F|f)(R|r)(O|o)(M|m):','', line).strip()
        bot.info('FROM %s' %line)
        self.config['from'] = line


    def _load_bootstrap(self, line):
        '''load bootstrap checks that the bootstrap is Docker, otherwise we
           exit on fail (there is no other option to convert to Dockerfile!
        '''
        if 'docker' not in line.lower():
            bot.error('docker not detected as Bootstrap!')
            sys.exit(1)


    def _load_section(self, lines, section):
        '''read in a section to a list, and stop when we hit the next section
        '''
        members = []

        while True:

            if len(lines) == 0:
                break
            next_line = lines[0]                

            # The end of a section
            if next_line.strip().startswith("%"):
                break

            # Still in current section!
            else:
                new_member = lines.pop(0).strip()
                if new_member not in ['', None]:
                    members.append(new_member)

        # Add the list to the config
        if len(members) > 0:
            if section is not None:
                self.config[section] += members


    def load_recipe(self):
        '''load will return a loaded in singularity recipe. The idea
           is that these sections can then be parsed into a Dockerfile,
           or printed back into their original form.

           Returns
           =======
           config: a parsed recipe Singularity recipe
        '''

        # Comments between sections, add to top of file
        lines = self.lines.copy()
        comments = []

        # Start with a fresh config!
        self.config = dict()
     
        section = None
        name = None

        while len(lines) > 0:

            # Clean up white trailing/leading space
            line = lines.pop(0)
            stripped = line.strip()

            # Bootstrap Line
            if re.search('(b|B)(o|O){2}(t|T)(s|S)(t|T)(r|R)(a|A)(p|P)', line):
                self._load_bootstrap(stripped)

            # From Line
            if re.search('(f|F)(r|R)(O|o)(m|M)', stripped):
                self._load_from(stripped)

            # Comment
            if stripped.startswith("#"):
                comments.append(stripped)
                continue

            # Section
            elif stripped.startswith('%'):
                section = self._add_section(stripped)
                bot.debug("Adding section title %s" %section)

            # If we have a section, and are adding it
            elif section is not None:
                lines = [line] + lines
                self._load_section(lines=lines,
                                   section=section)

            self.config['comments'] = comments


    def _add_section(self, line, section=None):
        '''parse a line for a section, and return the parsed section (if not
           None)

           Parameters
           ==========
           line: the line to parse
           section: the current (or previous) section

           Resulting data structure is:
           config['post'] (in lowercase)

        '''
        # Remove any comments
        line = line.split('#',1)[0].strip()

        # Is there a section name?
        parts = line.split(' ')
        if len(parts) > 1:
            name = ' '.join(parts[1:])          
        section = re.sub('[%]|(\s+)','',parts[0]).lower()

        if section not in self.config: 
            self.config[section] = []
            bot.debug("Adding section %s" %section)

        return section
