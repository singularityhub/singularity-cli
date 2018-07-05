
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
from spython.utils import check_install

import json
import sys
import os
import re


from .command import ( generate_bind_list, init_command, run_command )
from .flags import parse_verbosity
from .sutils import ( get_uri, load, setenv, get_filename )
from .logger import ( println,  init_level )
from .generate import RobotNamer

class Client:

    def __str__(self):
        base = "[singularity-python]"
        if hasattr(self, 'simage'):
            if self.simage.image not in [None,'']:
                base = "%s[%s]" %(base, self.simage)
        return base

    def __repr__(self):
        return self.__str__()


    def __init__(self):
       '''the base client for singularity, will have commands added to it.
          upon init, store verbosity requested in environment MESSAGELEVEL.
       '''
       self._init_level()


    def version(self):
        '''return the version of singularity
        '''

        if not check_install():
            bot.warning("Singularity version not found, so it's likely not installed.")
        else:
            cmd = ['singularity','--version']
            version = self._run_command(cmd).strip('\n')
            bot.debug("Singularity %s being used." % version)  
            return version


    def _check_install(self):
        '''ensure that singularity is installed, and exit if not.
        '''
        if check_install() is not True:
            bot.error("Cannot find Singularity! Is it installed?")
            sys.exit(1)



# Image Utils
Client.load = load
Client._get_filename = get_filename
Client._get_uri = get_uri
Client.setenv = setenv

# Commands
Client._generate_bind_list = generate_bind_list
Client._init_command = init_command
Client._run_command = run_command

# Flags and Logger
Client._parse_verbosity = parse_verbosity
Client._println = println
Client._init_level = init_level
Client.RobotNamer = RobotNamer()
