
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

import requests
import shutil
import sys
import os


def help(self, command=None):
    '''help prints the general function help, or help for a specific command

        Parameters
        ==========   
        command: the command to get help for, if none, prints general help

    '''
    from spython.utils import check_install
    check_install()

    cmd = ['singularity','--help']
    if command != None:
        cmd.append(command)
    help = self._run_command(cmd)
    return help
