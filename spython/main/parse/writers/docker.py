
# Copyright (C) 2017-2019 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.


import re
from spython.logger import bot

from .base import WriterBase

# FROM Validation

# Regular expressions to parse registry, collection, repo, tag and version
_docker_uri = re.compile(
    "(?:(?P<registry>[^/@]+[.:][^/@]*)/)?"
    "(?P<collection>(?:[^:@/]+/)+)?"
    "(?P<repo>[^:@/]+)"
    "(?::(?P<tag>[^:@]+))?"
    "(?:@(?P<version>.+))?"
    "$")

# Reduced to match registry:port/repo or registry.com/repo
_reduced_uri = re.compile(
    "(?:(?P<registry>[^/@]+[.:][^/@]*)/)?"
    "(?P<repo>[^:@/]+)"
    "(?::(?P<tag>[^:@]+))?"
    "(?:@(?P<version>.+))?"
    "$"
    "(?P<collection>.)?")

# Default
_default_uri = re.compile(
    "(?:(?P<registry>[^/@]+)/)?"
    "(?P<collection>(?:[^:@/]+/)+)"
    "(?P<repo>[^:@/]+)"
    "(?::(?P<tag>[^:@]+))?"
    "(?:@(?P<version>.+))?"
    "$")


class DockerWriter(WriterBase):

    name = 'docker'

    def __init__(self, recipe=None): # pylint: disable=useless-super-delegation
        '''a DockerWriter will take a Recipe as input, and write
           to a Dockerfile.

           Parameters
           ==========
           recipe: the Recipe object to write to file.

        '''
        super(DockerWriter, self).__init__(recipe)


    def validate(self):
        '''validate that all (required) fields are included for the Docker
           recipe. We minimimally just need a FROM image, and must ensure
           it's in a valid format. If anything is missing, we exit with error.
        '''
        if self.recipe is None:
            bot.exit('Please provide a Recipe() to the writer first.')

        if self.recipe.fromHeader is None:
            bot.exit("Dockerfile requires a fromHeader.")
            
            # Parse the provided name
            uri_regexes = [_reduced_uri,
                           _default_uri,
                           _docker_uri]

            for r in uri_regexes:
                match = r.match(self.recipe.fromHeader)
                if match:
                    break

            if not match:
                bot.exit('FROM header %s not valid.' % self.recipe.fromHeader)

    def convert(self, runscript="/bin/bash", force=False):
        '''convert is called by the parent class to convert the recipe object
           (at self.recipe) to the output file content to write to file.
        '''
        self.validate()

        recipe = ["FROM %s" % self.recipe.fromHeader]

        # Comments go up front!
        recipe += self.recipe.comments  

        # First add files, labels, environment
        recipe += write_files('ADD', self.recipe.files)
        recipe += write_lines('LABEL', self.recipe.labels)
        recipe += write_lines('ENV', self.recipe.environ)

        # Install routine is added as RUN commands
        recipe += write_lines('RUN', self.recipe.install)

        # Expose ports
        recipe += write_lines('EXPOSE', self.recipe.ports)

        if self.recipe.workdir is not None:
            recipe.append('WORKDIR %s' % self.recipe.workdir)

        # write the command, and entrypoint as is
        if self.recipe.cmd is not None:
            recipe.append('CMD %s' % self.recipe.cmd)

        if self.recipe.entrypoint is not None:
            recipe.append('ENTRYPOINT %s' % self.recipe.entrypoint)

        if self.recipe.test is not None:
            recipe += write_lines('HEALTHCHECK', self.recipe.test)

        # Clean up extra white spaces
        recipe = '\n'.join(recipe).replace('\n\n', '\n')
        return recipe.rstrip()


def write_files(label, lines):
    '''write a list of lines with a header for a section.
    
       Parameters
       ==========
       lines: one or more lines to write, with header appended

    '''
    result = []
    for line in lines:
        if isinstance(line, list):
            result.append('%s %s %s' %(label, line[0], line[1]))            
        else:
            result.append('%s %s' %(label, line))            
    return result

def write_lines(label, lines):
    '''write a list of lines with a header for a section.
    
       Parameters
       ==========
       lines: one or more lines to write, with header appended

    '''
    if not isinstance(lines, list):
        lines = [lines]

    result = []
    continued = False
    for line in lines:

        # Skip comments and empty lines
        if line.strip() == "" or line.strip().startswith('#'):
            continue

        if continued or "USER" in line:
            result.append(line)
        else:
            result.append('%s %s' %(label, line))

        continued = False
        if line.endswith('\\'):
            continued = True
            
    return result
