
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
from spython.utils import stream_command
import os
import sys


def execute(self, 
            image = None, 
            command = None,
            app = None,
            writable = False,
            contain = False,
            bind = None,
            stream = False,
            nv = False):

    ''' execute: send a command to a container
    
        Parameters
        ==========

        image: full path to singularity image
        command: command to send to container
        app: if not None, execute a command in context of an app
        writable: This option makes the file system accessible as read/write
        contain: This option disables the automatic sharing of writable
                 filesystems on your host
        bind: list or single string of bind paths.
             This option allows you to map directories on your host system to
             directories within your container using bind mounts
        nv: if True, load Nvidia Drivers in runtime (default False)
    '''
    from spython.utils import check_install
    check_install()

    cmd = self._init_command('exec')

    # nv option leverages any GPU cards
    if nv is True:
        cmd += ['--nv']
    
    # If the image is given as a list, it's probably the command
    if isinstance(image, list):
        command = image
        image = None

    if command is not None:
        
        # No image provided, default to use the client's loaded image
        if image is None:
            image = self._get_uri()
            self.quiet = True

        # If an instance is provided, grab it's name
        if isinstance(image, self.instance):
            image = image.get_uri()

        # Does the user want to use bind paths option?
        if bind is not None:
            cmd += self._generate_bind_list(bind)

        # Does the user want to run an app?
        if app is not None:
            cmd = cmd + ['--app', app]

        sudo = False
        if writable is True:
            sudo = True

        if not isinstance(command, list):
            command = command.split(' ')

        cmd = cmd + [image] + command
 
        if stream is False:
            return self._run_command(cmd,sudo=sudo)
        return stream_command(cmd, sudo=sudo)


    bot.error('Please include a command (list) to execute.')
