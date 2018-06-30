'''

Copyright (C) 2017 The Board of Trustees of the Leland Stanford Junior
University.
Copyright (C) 2016-2017 Vanessa Sochat.

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''

import os
import re

import json
from spython.logger import bot
import subprocess
import sys


################################################################################
# Local commands and requests
################################################################################


def check_install(software='singularity', quiet=True):
    '''check_install will attempt to run the singularity command, and
       return True if installed. The command line utils will not run 
       without this check.
    '''

    cmd = [software, '--version']
    found = False

    try:
        version = run_command(cmd, quiet=True)
    except: # FileNotFoundError
        return found

    if version is not None:
        if version['return_code'] == 0:
            found = True

        if quiet is False:
            version = version['message']
            bot.info("Found %s version %s" % (software.upper(), version))

    return found


def get_installdir():
    '''get_installdir returns the installation directory of the application
    '''
    return os.path.abspath(os.path.join('..', os.path.dirname(__file__)))


def stream_command(cmd, no_newline_regexp="Progess", sudo=False):
    '''stream a command (yield) back to the user, as each line is available.

       # Example usage:
       results = []
       for line in stream_command(cmd):
           print(line, end="")
           results.append(line)

       Parameters
       ==========
       cmd: the command to send, should be a list for subprocess
       no_newline_regexp: the regular expression to determine skipping a
                          newline. Defaults to finding Progress

    '''
    if sudo is True:
        cmd = ['sudo'] + cmd

    process = subprocess.Popen(cmd, 
                               stdout = subprocess.PIPE, 
                               universal_newlines = True)
    for line in iter(process.stdout.readline, ""):
        if not re.search(no_newline_regexp, line):
            yield line
    process.stdout.close()
    return_code = process.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


def run_command(cmd, 
                sudo=False,
                capture=True,
                no_newline_regexp="Progess",
                quiet=False):

    '''run_command uses subprocess to send a command to the terminal. If
       capture is True, we use the parent stdout, so the progress bar (and
       other commands of interest) are piped to the user. This means we 
       don't return the output to parse.

       Parameters
       ==========
       cmd: the command to send, should be a list for subprocess
       sudo: if needed, add to start of command
       no_newline_regexp: the regular expression to determine skipping a
                          newline. Defaults to finding Progress
       capture: if True, don't set stdout and have it go to console. This
                option can print a progress bar, but won't return the lines
                as output.
    '''

    if sudo is True:
        cmd = ['sudo'] + cmd

    stdout = None
    if capture is True:
        stdout = subprocess.PIPE

    # Use the parent stdout and stderr
    process = subprocess.Popen(cmd, 
                               stderr = subprocess.PIPE, 
                               stdout = stdout)
    lines = ()
    found_match = False

    for line in process.communicate():
        if line:
            if isinstance(line, bytes):
                line = line.decode('utf-8')
            lines = lines + (line,)
            if re.search(no_newline_regexp, line) and found_match is True:
                if quiet is False:
                    sys.stdout.write(line)
                found_match = True
            else:
                if quiet is False:
                    sys.stdout.write(line)
                    print(line.rstrip())
                found_match = False

    output = {'message': lines,
              'return_code': process.returncode }

    return output


################################################################################
# Parsing and Formatting
################################################################################


         

def format_container_name(name, special_characters=None):
    '''format_container_name will take a name supplied by the user,
    remove all special characters (except for those defined by "special-characters"
    and return the new image name.
    '''
    if special_characters is None:
        special_characters = []
    return ''.join(e.lower()
                   for e in name if e.isalnum() or e in special_characters)


def remove_uri(container):
    '''remove_uri will remove docker:// or shub:// from the uri
    '''
    return container.replace('docker://', '').replace('shub://', '')
