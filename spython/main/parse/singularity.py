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

from .recipe import Recipe
from spython.utils import read_file
from spython.logger import bot
from .environment import parse_env


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


# Add adn Copy Parser


    def _add(self, line):
        '''parse_add will copy multiple files from one location to another. This likely will need
           tweaking, as the files might need to be mounted from some location before adding to
           the image. The add command is done for an entire directory.
 
           Parameters
           ==========
           line: the line from the recipe file to parse for ADD
   
        '''

        line = self._setup('ADD', line)
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
        self.files.append(paths['to'], paths['from'])


    def _copy(self, line):
        '''For now, there isn't significant enough difference to warrant
           different functions. Copy is a wrapper for ADD. This will change
           as needed.
        '''
        return self._add(line)

# Comments


    def _comment(self, line):
        '''Simply add the line to the install as a comment. Add an extra # to be
           extra careful. 

           Parameters
           ==========
           line: the line from the recipe file to parse to INSTALL

        '''
        self.install.append( "# %s" %(line))


# Working Directory

    def parse_workdir(self, workdir):
        '''A Docker WORKDIR command simply implies to cd to that location

           Parameters
           ==========
           line: the line from the recipe file to parse for WORKDIR

        '''
        workdir = self._setup('WORKDIR', line)
        line = "cd %s" %(workdir)
        self.install.append(workdir)


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
        self.labels += label


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
            return self._comment

        cmd = line[0].upper()

        mapping = {"ADD": self._add,
                   "COPY": self._copy,
                   "CMD": self._cmd,
                   "ENTRYPOINT": self._entry,
                   "ENV": self._env,
                   "FROM": self._from,
                   "HEALTHCHECK": self._test,
                   "RUN": self._run,
                   "WORKDIR": self._workdir,
                   "MAINTAINER": self._label,
                   "VOLUME": self._comment,
                   "PORT": self._comment,
                   "LABEL": self._label}

        if cmd in mapping:
            return mapping[cmd]
        return self._comment
 

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
           
            # Parse it
            parser(line)






def dockerfile2singularity(self):
    '''dockerfile_to_singularity will return a Singularity build file based on
       a provided Dockerfile. If output directory is not specified, the string
       will be returned. Otherwise, a file called Singularity will be written to 
       output_dir
    :param dockerfile_path: the path to the Dockerfile
    :param output_dir: the output directory to write the Singularity file to
    '''
    build_file = None

    if os.path.basename(dockerfile_path) == "Dockerfile":

        try:
            spec = read_file(dockerfile_path)
            # Use a common mapping
            mapping = get_mapping()  
            # Put into dict of keys (section titles) and list of commands (values)
            sections = organize_sections(lines=spec,
                                         mapping=mapping)
            # We have to, by default, add the Docker bootstrap
            sections["bootstrap"] = ["docker"]
            # Put into one string based on "order" variable in mapping
            build_file = print_sections(sections=sections,
                                        mapping=mapping)
            if output_dir != None:
                write_file("%s/Singularity" %(output_dir),build_file)
                print("Singularity spec written to %s" %(output_dir))
            return build_file

        except:
            bot.logger.error("Error generating Dockerfile from %s.", dockerfile_path)

    # If we make it here, something didn't work
    bot.logger.error("Could not find %s.", dockerfile_path)
    return build_file




def parse_http(url,destination):
    '''parse_http will get the filename of an http address, and return a statement
    to download it to some location
    '''
    file_name = os.path.basename(url)
    download_path = "%s/%s" %(destination,file_name)
    return "curl %s -o %s" %(url,download_path)


def parse_targz(targz,destination):
    '''parse_targz will return a commnd to extract a targz file to a destination.
    '''
    return "tar -xzvf %s %s" %(targz,destination)


def parse_zip(zipfile,destination):
    '''parse_zipfile will return a commnd to unzip a file to a destination.
    '''
    return "unzip %s %s" %(zipfile,destination)


def parse_maintainer(cmd):
    '''parse_maintainer will eventually save the maintainer as metadata.
    For now we return as comment.
    :param cmd: the maintainer line
    '''
    return parse_comment(cmd)



def get_mapping():
    '''get_mapping returns a dictionary mapping from a Dockerfile command to a Singularity
    build spec section. Note - this currently ignores lines that we don't know what to do with
    in the context of Singularity (eg, EXPOSE, LABEL, USER, VOLUME, STOPSIGNAL, escape,
    MAINTAINER)

    :: note

    each KEY of the mapping should be a command start in the Dockerfile (eg, RUN)
    for each corresponding value, there should be a dictionary with the following:

        - section: the Singularity build file section to write the new command to
        - fun: any function to pass the output through before writing to the section (optional)
        - json: Boolean, if the section can optionally have json (eg a list)

    I'm not sure the subtle differences between add and copy, other than copy doesn't support
    external files. It should suffice for our purposes (for now) to use the same function 
    (parse_add) until evidence for a major difference is determined.
    '''

    #  Docker : Singularity
    add_command = {"section": "%post","fun": parse_add, "json": True }
    copy_command = {"section": "%post", "fun": parse_add, "json": True }  
    cmd_command = {"section": "%post", "fun": parse_comment, "json": True }  
    label_command = {"section": "%post", "fun": parse_comment, "json": True }  
    port_command = {"section": "%post", "fun": parse_comment, "json": True }  
    env_command = {"section": "%post", "fun": parse_env, "json": False }
    comment_command = {"section": "%post", "fun": parse_comment, "json": False }
    from_command = {"section": "From", "json": False }
    run_command = {"section": "%post", "json": True}       
    workdir_command = {"section": "%post","fun": parse_workdir, "json": False }  
    entry_command = {"section": "%runscript", "fun": parse_entry, "json": True }

    return {"ADD": add_command,
            "COPY":copy_command,
            "CMD":cmd_command,
            "ENTRYPOINT":entry_command,
            "ENV": env_command,
            "FROM": from_command,
            "RUN":run_command,
            "WORKDIR":workdir_command,
            "MAINTAINER":comment_command,
            "VOLUME":comment_command,
            "PORT":port_command,
            "LABEL":label_command}
           
    



def organize_sections(lines,mapping=None):
    '''organize_sections will break apart lines from a Dockerfile, and put into 
    appropriate Singularity sections.
    :param lines: the raw lines from the Dockerfile
    :mapping: a dictionary mapping Docker commands to Singularity sections
    '''
    if mapping == None:
        mapping = get_mapping()

    sections = dict()
    startre = "|".join(["^%s" %x for x in mapping.keys()])
    command = None
    name = None

    for l in range(0,len(lines)):
        line = lines[l]

        # If it's a newline or comment, just add it to post
        if line == "\n" or re.search("^#",line):
            sections = parse_section(name="%post",
                                     command=line,
                                     mapping=mapping,
                                     sections=sections)
        elif re.search(startre,line):

            # Parse the last section, and start over
            if command != None and name != None:
                sections = parse_section(name=name,
                                         command=command,
                                         mapping=mapping,
                                         sections=sections)
            name,command = line.split(" ",1)
        else:

            # We have a continuation of the last command or an empty line
            command = "%s\n%s" %(command,line)

    return sections

def parse_section(sections,name,command,mapping=None):
    '''parse_section will take a command that has lookup key "name" as a key in "mapping"
    and add a line to the list of each in sections that will be rendered into a Singularity
    build file.
    :param sections: the current sections, a dictionary of keys (singularity section titles)
    and a list of lines.
    :param name: the name of the section to add
    :param command: the command to parse:
    :param mapping: the mapping object to use
    '''
    if mapping == None:
        mapping = get_mapping()

    if name in mapping:
        build_section = mapping[name]['section']

        # Can the command potentially be json (a list?)
        if mapping[name]['json']:
            try:
                command = " ".join(json.loads(command))
            except:
                pass 

        # Do we need to pass it through a function first?
        if 'fun' in mapping[name]:
            command = mapping[name]['fun'](command)

        # Add to our dictionary of sections!
        if build_section not in sections:
            sections[build_section] = [command]
        else:
            sections[build_section].append(command)
    return sections


def print_sections(sections,mapping=None):
    '''print_sections will take a sections object (dict with section names and
    list of commands) and parse into a common string, to output to file or return
    to user.
    :param sections: output from organize_sections
    :mapping: a dictionary mapping Docker commands to Singularity sections
    '''

    if mapping == None:
        mapping = get_mapping()

    finished_spec = None
    ordering = ['bootstrap',"From","%runscript","%post",'%test']

    for section in ordering:

        # Was the section found in the file?
        if section in sections:
            content = "".join(sections[section])

            # A single command, intended to go after a colon (yaml)    
            if not re.search("^%",section):
                content = "%s:%s" %(section,content)
            else:
                # A list of things to join, after the section header
                content = "%s\n%s" %(section,content)

            # Are we adding the first line?
            if finished_spec == None:
                finished_spec = content
            else:
                finished_spec = "%s\n%s" %(finished_spec,content)
    return finished_spec
