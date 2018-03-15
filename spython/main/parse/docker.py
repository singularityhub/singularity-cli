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


import os
import re

from .environment import parse_env
from .recipe import Recipe
from spython.utils import read_file
from spython.logger import bot

class DockerRecipe(Recipe):

    def __init__(self, recipe=None):
        '''a Docker recipe parses a Docker Recipe into the expected fields of
           labels, environment, and install/runtime commands

           Parameters
           ==========
           recipe: the recipe file (Dockerfile) to parse

        '''
        self.name = "docker"
        super().__init__(recipe)


# Setup for each Parser

    def _setup(self, action, line):
        ''' replace the command name from the group, alert the user of content,
            and clean up empty spaces
        '''
        bot.debug('[in]  %s' % line)

        # Replace ACTION at beginning
        line = re.sub('^%s' %action, '', line)

        # Split into components
        return [x for x in self._split_line(line) if x not in ['', None]]


# From Parser

    def _from(self, line):
        ''' get the FROM container image name from a FROM line!

           Parameters
           ==========
           line: the line from the recipe file to parse for FROM

        '''
        self.fromHeader = self._setup('FROM', line)
        bot.debug('FROM %s' %self.fromHeader) 


# Run and Test Parser

    def _run(self, line):
        ''' everything from RUN goes into the install list

           Parameters
           ==========
           line: the line from the recipe file to parse for FROM

        '''
        line = self._setup('RUN', line)
        self.install += line


    def _test(self, line):
        ''' A healthcheck is generally a test command

           Parameters
           ==========
           line: the line from the recipe file to parse for FROM

        '''
        self.test  = self._setup('HEALTHCHECK', line)
        

# Env Parser

    def _env(self, line):
        '''env will parse a line that beings with ENV, indicative of one or
           more environment variables.
 
           Parameters
           ==========
           line: the line from the recipe file to parse for ADD
   
        '''
        line = self._setup('ENV', line)

        # Extract environment (list) from the line
        environ = parse_env(line)

        # Add to global environment, run during install
        self.install += environ

        # Also define for global environment
        self.environ += environ


# Add and Copy Parser


    def _add(self, lines):
        '''parse_add will copy multiple files from one location to another. This likely will need
           tweaking, as the files might need to be mounted from some location before adding to
           the image. The add command is done for an entire directory.
 
           Parameters
           ==========
           line: the line from the recipe file to parse for ADD
   
        '''

        lines = self._setup('ADD', lines)
        
        for line in lines:
            frompath, topath = line.split(" ")

            # Create data structure to iterate over for paths
            paths = dict()
            paths['from'] = frompath
            paths['to'] = topath
        
            for pathtype, path in paths.items():
                if path == ".":
                    paths[pathtype] = os.getcwd()
 
                # Warning if doesn't exist
                if not os.path.exists(path):
                    bot.warning("%s doesn't exist, ensure exists for build" %path)

            # The pair is added to the files as a list
            self.files.append([paths['from'], paths['to']])


    def _copy(self, line):
        '''For now, there isn't significant enough difference to warrant
           different functions. Copy is a wrapper for ADD. This will change
           as needed.
        '''
        return self._add(line)


# Comments and Default

    def _comment(self, line):
        '''Simply add the line to the install as a comment. This function is
           equivalent to default, but added in the case we need future custom
           parsing (meaning a comment is different from a line. 

           Parameters
           ==========
           line: the line from the recipe file to parse to INSTALL

        '''
        self.install.append(line)


    def _default(self, line):
        '''the default action assumes a line that is either a command (a 
           continuation of a previous, for example) or a comment.
          
           Parameters
           ==========
           line: the line from the recipe file to parse to INSTALL
        '''
        if line.strip().startswith('#'):
            return self._comment(line)
        self.install.append(line)
        

# Ports and Volumes

    def _volume(self, line):
        '''We don't have logic for volume for Singularity, so we add as
           a comment in the install, and a metadata value for the recipe 
           object
  
           Parameters
           ==========
           line: the line from the recipe file to parse to INSTALL

        '''
        volumes = self._setup('VOLUME', line)
        if len(volumes) > 0:
            self.volumes += volumes
        return self._comment("# %s" %line)


    def _expose(self, line):
        '''Again, just add to metadata, and comment in install.
  
           Parameters
           ==========
           line: the line from the recipe file to parse to INSTALL

        '''
        ports = self._setup('EXPOSE', line)
        if len(ports) > 0:
            self.ports += ports
        return self._comment("# %s" %line)


# Working Directory

    def _workdir(self, line):
        '''A Docker WORKDIR command simply implies to cd to that location

           Parameters
           ==========
           line: the line from the recipe file to parse for WORKDIR

        '''
        workdir = self._setup('WORKDIR', line)
        line = "cd %s" %(''.join(workdir))
        self.install.append(line)


# Entrypoint and Command

    def _cmd(self, line):
        '''_cmd will parse a Dockerfile CMD command
           
           eg: CMD /code/run_uwsgi.sh --> /code/run_uwsgi.sh.
               The 

           Parameters
           ==========
           line: the line from the recipe file to parse for CMD

        '''
        self.cmd = self._setup('CMD', line)


    def _entry(self, line):
        '''_entrypoint will parse a Dockerfile ENTRYPOINT command
           
           Parameters
           ==========
           line: the line from the recipe file to parse for CMD

        '''
        self.entrypoint = self._setup('ENTRYPOINT', line)


# Labels

    def _label(self, line):
        '''_label will parse a Dockerfile label
           
           Parameters
           ==========
           line: the line from the recipe file to parse for CMD

        '''
        label = self._setup('LABEL', line)
        self.labels += [ label ]


# Main Parsing Functions


    def _split_line(self, line):
        '''clean a line to prepare it for parsing, meaning separation
           of the Docker command (e.g., RUN) from the remainder. We remove
           newlines (from ends) along with extra spaces.

           Parameters
           ==========
           line: the string to parse into parts
    
           Returns
           =======
           parts: a list of line pieces, the command is likely first

        '''
        return [x.strip() for x in line.split(' ', 1)]
        


    def _get_mapping(self, line):
        '''mapping will take the command from a Dockerfile and return a map
           function to add it to the appropriate place. Any lines that don't
           cleanly map are assumed to be comments.

           Parameters
           ==========
           line: the list that has been parsed into parts with _split_line
    
           Returns
           =======
           function: to map a line to its command group

        '''

        # Split the command into cleanly the command and rest
        if not isinstance(line, list):
            line = self._split_line(line)

        # No line we will give function to handle empty line
        if len(line) == 0:
            return None

        cmd = line[0].upper()

        mapping = {"ADD": self._add,
                   "COPY": self._copy,
                   "CMD": self._cmd,
                   "ENTRYPOINT": self._entry,
                   "ENV": self._env,
                   "EXPOSE": self._expose,
                   "FROM": self._from,
                   "HEALTHCHECK": self._test,
                   "RUN": self._run,
                   "WORKDIR": self._workdir,
                   "MAINTAINER": self._label,
                   "VOLUME": self._volume,
                   "LABEL": self._label}

        if cmd in mapping:
            return mapping[cmd]
        return self._default
 

    def _parse(self):
        '''parse is the base function for parsing the Dockerfile, and extracting
           elements into the correct data structures. Everything is parsed into
           lists or dictionaries that can be assembled again on demand. 

           Environment: Since Docker also exports environment as we go, 
                        we add environment to the environment section and 
                        install

           Labels: include anything that is a LABEL, ARG, or (deprecated)
                   maintainer.

           Add/Copy: are treated the same

        '''

        for line in self.lines:

            # Get the correct parsing function
            parser = self._get_mapping(line)
           
            # Parse it, if appropriate
            if parser:
                parser(line)
