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


def stop(self, name=None, sudo=False):
    '''start an instance. This is done by default when an instance is created.

       Parameters
       ==========
       image: optionally, an image uri (if called as a command from Client)
       name: a name for the instance
       sudo: if the user wants to run the command with sudo

       USAGE: 
       singularity [...] instance.start [...] <container path> <instance name>

    '''        
    from spython.utils import ( check_install, run_command )
    check_install()

    cmd = self._init_command('instance.stop')

    # If name is provided assume referencing an instance
    instance_name = self.name
    if name is not None:
        instance_name = name     
    cmd = cmd + [instance_name]
    
    output = run_command(cmd, sudo=sudo, quiet=True)

    if output['return_code'] != 0:
        message = '%s : return code %s' %(output['message'], 
                                          output['return_code'])
        bot.error(message)
        return output['return_code']

    return output['return_code']
