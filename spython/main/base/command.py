
# Copyright (C) 2017-2019 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.


from spython.main.base.logger import println
from spython.utils import ( 
    run_command as run_cmd, 
    check_install 
)

from spython.logger import bot

import subprocess
import json
import sys
import os
import re



def init_command(self, action, flags=None):
    '''return the initial Singularity command with any added flags.
        
       Parameters
       ==========
       action: the main action to perform (e.g., build)
       flags: one or more additional flags (e.g, volumes) 
              not implemented yet.
    '''

    if not isinstance(action, list):
        action = [action]      
    cmd = ['singularity'] + action

    if self.quiet is True:
        cmd.insert(1, '--quiet')
    if self.debug is True:
        cmd.insert(1, '--debug')

    return cmd


def generate_bind_list(self, bindlist=None):
    '''generate bind string will take a single string or list of binds, and
       return a list that can be added to an exec or run command. For example,
       the following map as follows:

      ['/host:/container', '/both'] --> ["--bind", "/host:/container","--bind","/both" ]
      ['/both']                     --> ["--bind", "/both"]
      '/host:container'             --> ["--bind", "/host:container"]
       None                         --> []
 
       An empty bind or otherwise value of None should return an empty list.
       The binds are also checked on the host.

       Parameters
       ==========
       bindlist: a string or list of bind mounts

    '''
    binds = []
    
    # Case 1: No binds provided
    if not bindlist:
        return binds

    # Case 2: provides a long string or non list, and must be split
    if not isinstance(bindlist, list):
        bindlist = bindlist.split(' ')

    for bind in bindlist:

        # Still cannot be None
        if bind:
            bot.debug('Adding bind %s' %bind)
            binds += ['--bind', bind]

            # Check that exists on host
            host = bind.split(':')[0]
            if not os.path.exists(host):
                bot.error('%s does not exist on host.' %bind)
                sys.exit(1)

    return binds



def run_command(self, cmd, sudo=False, capture=True):
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
    result = run_cmd(cmd, sudo=sudo, capture=capture, quiet=self.quiet)
    message = result['message']
    return_code = result['return_code']

    if result['return_code'] == 0:
        if len(message) == 1:
            message = message[0]
        return message

    if self.quiet is False:
        bot.error("Return Code %s: %s" %(return_code,
                                         message))
