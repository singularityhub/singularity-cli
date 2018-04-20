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

# Singularity to Dockerfile
# Easier, parsed line by line

def singularity2docker(self, runscript="/bin/bash", force=False):
    '''convert a Singularity recipe to a (best estimated) Dockerfile'''

    recipe = [ "FROM %s" %self.fromHeader ]

    # Comments go up front!
    recipe += self.comments  

    # First add files, labels
    recipe += write_lines('ADD', self.files)
    recipe += write_lines('LABEL', self.labels)
    recipe += write_lines('ENV', self.environ)

    # Install routine is added as RUN commands
    recipe += write_lines('RUN', self.install)

    # Take preference for user, entrypoint, command, then default
    runscript = self._create_runscript(runscript, force)
    recipe.append('CMD %s' %runscript)

    if self.test is not None:
        recipe.append(write_lines('HEALTHCHECK', self.test))

    # Clean up extra white spaces
    return '\n'.join(recipe).replace('\n\n','\n')


def write_lines(label, lines):
    '''write a list of lines with a header for a section.
    
       Parameters
       ==========
       lines: one or more lines to write, with header appended

    '''
    result = []
    continued = False
    for line in lines:
        if continued:
            result.append(line)
        else:
            result.append('%s %s' %(label, line))
        continued = False
        if line.endswith('\\'):
            continued = True
            
    return result


# Dockerfile to Singularity
# Here we deal with "sections" and not individual lines

def create_runscript(self, default="/bin/bash", force=False):
    '''create_entrypoint is intended to create a singularity runscript
       based on a Docker entrypoint or command. We first use the Docker
       ENTRYPOINT, if defined. If not, we use the CMD. If neither is found,
       we use function default.

       Parameters
       ==========
       default: set a default entrypoint, if the container does not have
                an entrypoint or cmd.
       force: If true, use default and ignore Dockerfile settings

    '''
    entrypoint = default

    # Only look at Docker if not enforcing default
    if force is False:
        if self.entrypoint is not None:
            entrypoint = ''.join(self.entrypoint)
        elif self.cmd is not None:
            entrypoint = ''.join(self.cmd)

    # Entrypoint should use exec
    if not entrypoint.startswith('exec'):
        entrypoint = "exec %s" %entrypoint

    # Should take input arguments into account
    if not re.search('"?[$]@"?', entrypoint):
        entrypoint = '%s "$@"' %entrypoint
    return entrypoint


def create_section(self, attribute, name=None):
    '''create a section based on key, value recipe pairs, 
       This is used for files or label

      Parameters
      ==========
      attribute: the name of the data section, either labels or files
      name: the name to write to the recipe file (e.g., %name).
            if not defined, the attribute name is used.

    '''

    # Default section name is the same as attribute
    if name is None:
        name = attribute 

    # Put a space between sections
    section = ['\n']

    # Only continue if we have the section and it's not empty
    try:
        section = getattr(self, attribute)
    except AttributeError:
        bot.debug('Recipe does not have section for %s' %attribute)
        return section

    # if the section is empty, don't print it
    if len(section) == 0:
        return section

    # Files or Labels
    if attribute in ['labels', 'files']:
        return create_keyval_section(section, name)

    # An environment section needs exports
    if attribute in ['environ']:
        return create_env_section(section, name)

    # Post, Setup
    return finish_section(section, name)


def finish_section(section, name):
    '''finish_section will add the header to a section, to finish the recipe
       take a custom command or list and return a section.

       Parameters
       ==========
       section: the section content, without a header
       name: the name of the section for the header

    '''   
    if not isinstance(section, list):
        section = [section]

    header = ['%' + name ]
    return header + section


def create_keyval_section(pairs, name):
    '''create a section based on key, value recipe pairs, 
       This is used for files or label

      Parameters
      ==========
      section: the list of values to return as a parsed list of lines
      name: the name of the section to write (e.g., files)

    '''
    section = ['%' + name ]
    for pair in pairs:
        section.append(' '.join(pair).strip().strip('\\'))
    return section


def create_env_section(pairs, name):
    '''environment key value pairs need to be joined by an equal, and 
       exported at the end.

      Parameters
      ==========
      section: the list of values to return as a parsed list of lines
      name: the name of the section to write (e.g., files)

    '''
    section = ['%' + name ]
    for pair in pairs:
        section.append("export %s" %pair)
    return section


def docker2singularity(self, runscript="/bin/bash", force=False):
    '''docker2singularity will return a Singularity build recipe based on
       a the loaded recipe object. It doesn't take any arguments as the
       recipe object contains the sections, and the calling function 
       determines saving / output logic.
    '''

    recipe = ['Bootstrap: docker']
    recipe += [ "From: %s" %self.fromHeader ]
  
    # Sections with key value pairs
    recipe += self._create_section('files')
    recipe += self._create_section('labels')
    recipe += self._create_section('install', 'post')
    recipe += self._create_section('environ', 'environment')    

    # Take preference for user, entrypoint, command, then default
    runscript = self._create_runscript(runscript, force)
    recipe += finish_section(runscript, 'runscript')

    if self.test is not None:
        recipe += finish_section(self.test, 'test')

    # Clean up extra white spaces
    return '\n'.join(recipe).replace('\n\n','\n')
