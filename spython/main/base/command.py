'''

Copyright (C) 2017-2018 The Board of Trustees of the Leland Stanford Junior
University.
Copyright (C) 2016-2018 Vanessa Sochat.

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

from spython.utils import ( 
    run_command as run_cmd, 
    check_install 
)
from spython.image import Image
from spython.logger import bot

import json
import sys
import os
import re


def init_command(self, action, flags=None):
    '''
        return the initial Singularity command with any added flags.
        
        Parameters
        ==========
        action: the main action to perform (e.g., build)
        flags: one or more additional flags (e.g, volumes) 
               not implemented yet.

    '''

    cmd = ['singularity', action ]

    if self.quiet is True:
        cmd.insert(1, '--quiet')
    if self.debug is True:
        cmd.insert(1, '--debug')

    return cmd


def run_command(self, cmd, sudo=False, quiet=False, capture=True):
    '''run_command is a wrapper for the global run_command, checking first
       for sudo and exiting on error if needed. The message is returned as
       a list of lines for the calling function to parse, and stdout uses
       the parent process so it appears for the user.

       Parameters
       ==========
       cmd: the command to run
       sudo: does the command require sudo?
       On success, returns result. Otherwise, exists on error
    
    '''

    result = run_cmd(cmd, sudo=sudo, capture=capture)
    message = result['message']
    return_code = result['return_code']
        
    if result['return_code'] == 0:
        return message

    if quiet is False:
        bot.error("Return Code %s: %s" %(return_code,
                                         message))
