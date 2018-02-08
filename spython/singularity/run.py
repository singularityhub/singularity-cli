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

from spython.logger import bot
from client.flags import (
    DEBUG,
    QUIET,
    VERBOSE
)

def run(self, image_path,
              args=None,
              sudo = False,
              writable=False,
              contain=False):
     '''
        run will run the container, with or withour arguments (which
        should be provided in a list)
    
        Parameters
        ==========
        image_path: full path to singularity image
        args: args to include with the run
        
    '''

    # TODO: flags / commands should be parsed separately and give here
    #       (and removed from input args above

    cmd = self.init_cmd('run')

    # If verbose and debug not in the command, make it quiet
    if DEBUG not in cmd and VERBOSE not in cmd:
        cmd.insert(1, QUIET)

    # STOPPED HERE - finish going through commands to update, come up with
    # a strategy to handle this command (before?) or still after?

    cmd = self.add_flags(cmd,writable=writable,
                             contain=contain)

    cmd = cmd + [image_path]

    # Conditions for needing sudo
    if writable is True:
        sudo = True
        
    if args is not None:        
        if not isinstance(args,list):
            args = args.split(' ')
        cmd = cmd + args

    result = self.run_command(cmd,sudo=sudo)
    result = result.strip('\n')
    try:
        result = json.loads(result)
    except:
        pass
    return result
