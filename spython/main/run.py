
# Copyright (C) 2018 The Board of Trustees of the Leland Stanford Junior
# University.
# Copyright (C) 2017-2018 Vanessa Sochat.

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


from spython.logger import bot
import json
from itertools import chain

def run(self, 
        image=None,
        args = None,
        app = None,
        sudo = False,
        writable = False,
        contain = False,
        bind = None):

    '''
    run will run the container, with or withour arguments (which
    should be provided in a list)
    
    Parameters
    ==========
    image: full path to singularity image
    args: args to include with the run
        
   '''

    self.check_install()
    cmd = self._init_command('run')

    # No image provided, default to use the client's loaded image
    if image is None:
        image = self._get_uri()

    # Does the user want to use bind paths option?
    if bind is not None:
        cmd = bind_string(cmd,bind)

    # Does the user want to run an app?
    if app is not None:
        cmd = cmd + ['--app', app]

    cmd = cmd + [image]

    # Conditions for needing sudo
    if writable is True:
        sudo = True
        
    if args is not None:        
        if not isinstance(args, list):
            args = args.split(' ')
        cmd = cmd + args

    result = self._run_command(cmd, sudo=sudo)
    result = result.strip('\n')
    try:
        result = json.loads(result)
    except:
        pass
    return result

def bind_string(cmd,bind):
    if isinstance(bind,list):
        cmd = cmd + list(chain.from_iterable(zip(["--bind"]*len(bind),bind)))
    elif isinstance(bind,str):
        bind = [x.strip() for x in bind.split(" ")]
        cmd = cmd + list(chain.from_iterable(zip(["--bind"]*len(bind),bind)))
    else:
        bot.error('The type of bind must be a list or str.')
    return cmd
