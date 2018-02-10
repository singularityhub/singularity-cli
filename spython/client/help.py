'''

Copyright (C) 2017 The Board of Trustees of the Leland Stanford Junior
University.
Copyright (C) 2017-2018 Vanessa Sochat.

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

from spython.logger import bot
import sys
import os


def main(args, options):
    '''call the client to print Singularity help. If a command is provided,
       print help specific to it and exit.
    
       Parameters
       ==========
       args.command: one of the main entry point commands to print, to show help

    '''
    # If the command isn't help, it's what help is needed for
    command = args.command
    if command == 'help':
        command=None

        # Given the help command, the action is from options
        if len(options) > 0:
            command=options[0]

    from spython.main import Client
    return Client.help(command=command, stdout=True)
