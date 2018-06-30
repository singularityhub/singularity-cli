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


def generate_instance_commands():
    ''' The Instance client holds the Singularity Instance command group
        The levels of verbosity (debug and quiet) are passed from the main
        client via the environment variable MESSAGELEVEL.

    '''
    from spython.instance import Instance

    from spython.main.base.logger import println
    from spython.main.instances import instances
    from spython.utils import run_command as run_cmd

    # run_command uses run_cmd, but wraps to catch error
    from spython.main.base.command import ( init_command, run_command )
    from spython.main.base.generate import RobotNamer
    from .start import start
    from .stop import stop

    Instance.RobotNamer = RobotNamer()
    Instance._init_command = init_command
    Instance.run_command = run_cmd
    Instance._run_command = run_command
    Instance._list = instances  # list command is used to get metadata
    Instance._println = println
    Instance._start = start     # intended to be called on init, not by user
    Instance.stop = stop

    # Give an instance the ability to breed :)
    Instance.instance = Instance
 
    return Instance

instance_group = generate_instance_commands()
