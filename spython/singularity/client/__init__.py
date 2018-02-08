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

from spython.utils import run_command
from spython.logger import bot

from .flags import (
    DEBUG,
    QUIET,
    VERBOSE
)

import json
import sys
import os
import re


class Client:

    def __init__(self, verbose=False, debug=False, quiet=False):
       '''the base client for singularity, will have commands added to it.
          upon init, store verbosity requested

          Parameters
          ==========
          debug: associated with --debug flag
          verbose: associated with --verbose flag
          quiet: associated with --quiet flag

       '''

       self.debug = debug
       self.quiet = quiet
       self.verbose = verbose


    def init_cmd(self, action, flags=None):
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
            cmd.insert(1, QUIET)
        if self.debug is True:
            cmd.insert(1, DEBUG)
        elif self.verbose is True:
            cmd.insert(1, VERBOSE)

        return cmd


    def run_command(self, cmd, sudo=False, quiet=False):
        '''run_command is a wrapper for the global run_command, checking first
        for sudo and exiting on error if needed
        :param cmd: the command to run
        :param sudo: does the command require sudo?
        On success, returns result. Otherwise, exists on error
        '''
        result = run_command(cmd,sudo=sudo)
        message = result['message']
        return_code = result['return_code']
        
        if result['return_code'] == 0:
            if isinstance(message,bytes):
                try:
                    message=message.decode('utf-8')
                except UnicodeDecodeError:
                    try:
                        message = unicode(message, errors='replace')
                    except NameError:
                        message = str(message, errors='replace')
            return message
        if quiet is False:
            bot.error("Return Code %s: %s" %(return_code,
                                             message))
        sys.exit(1)


    def println(self,output,quiet=False):
        '''print will print the output, given that quiet is not True. This
        function also serves to convert output in bytes to utf-8
        '''
        if isinstance(output,bytes):
            output = output.decode('utf-8')
        if self.quiet is False and quiet is False:
            print(output)

    def version(self):
        '''return the version of singularity
        '''
        from singularity.build.utils import get_singularity_version
        return get_singularity_version()



    def get_labels(self,image_path):
        '''get_labels will return all labels defined in the image
        '''
        cmd = ['singularity','exec',image_path,'cat','/.singularity.d/labels.json']
        try:
            labels = self.run_command(cmd)
            if len(labels) > 0:
                return json.loads(labels)
        except:
            labels = dict()
        return labels
        

    def get_args(self,image_path):
        '''get_args will return the subset of labels intended to be arguments
        (in format SINGULARITY_RUNSCRIPT_ARG_*
        '''
        args = dict()
        for label,values in labels.items():
            if re.search("^SINGULARITY_RUNSCRIPT_ARG",label):
                vartype = label.split('_')[-1].lower()
                if vartype in ["str","float","int","bool"]:
                    args[vartype] = values.split(',')
        return args


    def add_flags(self,cmd,writable=False,contain=False):
        '''check_args is a general function for adding flags to a command list
        :param writable: adds --writable
        :param contain: adds --contain
        ''' 
        if writable == True:
            cmd.append('--writable')       

        if contain == True:
            cmd.append('--contain')       

        return cmd
