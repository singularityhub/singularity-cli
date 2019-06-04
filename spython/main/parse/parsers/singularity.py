
# Copyright (C) 2017-2019 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.


import re

from spython.logger import bot
from .base import ParserBase


class SingularityParser(ParserBase):

    name = 'singularity'

    def __init__(self, filename="Singularity", load=True):
        '''a SingularityParser parses a Singularity file into expected fields of
           labels, environment, and install/runtime commands. The base class
           ParserBase will instantiate an empty Recipe() object to populate,
           and call parse() here on the recipe.

           Parameters
           ==========
           filename: the recipe file (Singularity) to parse
           load: load and parse the recipe (defaults to True)

        '''
        super(SingularityParser, self).__init__(filename, load)


    def parse(self):
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

        return self.recipe


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
        self.recipe.fromHeader = line
        bot.debug('FROM %s' % self.recipe.fromHeader) 


# Run and Test Parser

    def _test(self, lines):
        ''' A healthcheck is generally a test command

           Parameters
           ==========
           line: the line from the recipe file to parse for FROM

        '''
        self._write_script('/tests.sh', lines)
        self.recipe.test = "/bin/bash /tests.sh"
        

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
        self.recipe.environ += environ


# Files for container


    def _files(self, lines):
        '''parse_files will simply add the list of files to the correct object
 
           Parameters
           ==========
           lines: pairs of files, one pair per line
   
        '''
        self.recipe.files += lines


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
            self.recipe.comments.append(comment)


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

        self.recipe.cmd = runscript


# Labels

    def _labels(self, lines):
        '''_labels simply adds the labels to the list to save.
           
           Parameters
           ==========
           lines: the lines from the recipe with key,value pairs

        '''
        self.recipe.labels += lines


    def _post(self, lines):
        '''the main core of commands, to be added to the install section

           Parameters
           ==========
           lines: the lines from the recipe with install commands

        '''
        self.recipe.install += lines


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
 

# Loading Functions

    def _load_from(self, line):
        '''load the From section of the recipe for the Dockerfile.
        '''
        # Remove any comments
        line = line.split('#', 1)[0] 
        line = re.sub('(F|f)(R|r)(O|o)(M|m):', '', line).strip()
        self.config['from'] = line


    def _load_bootstrap(self, line):
        '''load bootstrap checks that the bootstrap is Docker, otherwise we
           exit on fail (there is no other option to convert to Dockerfile!
        '''
        if 'docker' not in line.lower():
            raise NotImplementedError('docker not detected as Bootstrap!')


    def _load_section(self, lines, section):
        '''read in a section to a list, and stop when we hit the next section
        '''
        members = []

        while True:

            if not lines:
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
        if members:
            if section is not None:
                self.config[section] += members


    def load_recipe(self):
        '''load_recipe will return a loaded in singularity recipe. The idea
           is that these sections can then be parsed into a Dockerfile,
           or printed back into their original form.

           Returns
           =======
           config: a parsed recipe Singularity recipe
        '''

        # Comments between sections, add to top of file
        lines = self.lines[:]
        comments = []

        # Start with a fresh config!
        self.config = dict()
     
        section = None

        while lines:

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
        line = line.split('#', 1)[0].strip()

        # Is there a section name?
        parts = line.split(' ')         
        section = re.sub(r'[%]|(\s+)', '', parts[0]).lower()

        if section not in self.config: 
            self.config[section] = []
            bot.debug("Adding section %s" % section)

        return section


    def _write_script(self, path, lines, chmod=True):
        '''write a script with some lines content to path in the image. This
           is done by way of adding echo statements to the install section.

           Parameters
           ==========
           path: the path to the file to write
           lines: the lines to echo to the file
           chmod: If true, change permission to make u+x

        '''
        for line in lines:
            self.recipe.install.append('echo "%s" >> %s' % (line, path))

        if chmod:
            self.recipe.install.append('chmod u+x %s' % path)
