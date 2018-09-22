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
import sys

def start(self, image=None, name=None, sudo=False, options=[], capture=False):
    '''start an instance. This is done by default when an instance is created.

       Parameters
       ==========
       image: optionally, an image uri (if called as a command from Client)
       name: a name for the instance
       sudo: if the user wants to run the command with sudo
       capture: capture output, default is False. With True likely to hang.
       options: a list of tuples, each an option to give to the start command
                [("--bind", "/tmp"),...]

       USAGE: 
       singularity [...] instance.start [...] <container path> <instance name>

    '''        
    from spython.utils import ( run_command, check_install )
    check_install()

    # If no name provided, give it an excellent one!
    if name is None:
        name = self.RobotNamer.generate()
    self.name = name.replace('-','_')

    # If an image isn't provided, we have an initialized instance
    if image is None:

        # Not having this means it was called as a command, without an image
        if not hasattr(self, "_image"):
            bot.error('Please provide an image, or create an Instance first.')
            sys.exit(1)

        image = self._image

    cmd = self._init_command('instance.start')

    # Add options, if they are provided
    if not isinstance(options, list):
        options = options.split(' ')

    # Assemble the command!
    cmd = cmd + options + [image, self.name]

    # Save the options and cmd, if the user wants to see them later
    self.options = options
    self.cmd = cmd

    output = run_command(cmd, sudo=sudo, quiet=True, capture=capture)

    if output['return_code'] == 0:
        self._update_metadata()

    else:
        message = '%s : return code %s' %(output['message'], 
                                          output['return_code'])
        bot.error(message)

    return self
