'''

Copyright (C) 2018 The Board of Trustees of the Leland Stanford Junior
University.
Copyright (C) 2018 Vanessa Sochat.

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

    def execute(self,image_path,command,writable=False,contain=False):
        '''execute: send a command to a container
        :param image_path: full path to singularity image
        :param command: command to send to container
        :param writable: This option makes the file system accessible as read/write
        :param contain: This option disables the automatic sharing of writable
                        filesystems on your host
        '''
        sudo = False    
        if self.debug == True:
            cmd = ["singularity",'--debug',"exec"]
        else:
            cmd = ["singularity",'--quiet',"exec"]

        cmd = self.add_flags(cmd,
                             writable=writable,
                             contain=contain)

        if writable is True:
            sudo = True

        if not isinstance(command,list):
            command = command.split(' ')

        cmd = cmd + [image_path] + command
        return self.run_command(cmd,sudo=sudo)

