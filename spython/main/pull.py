
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
import re
import sys

def pull(self, 
         image=None,
         name=None,
         pull_folder='',
         ext="simg",
         force=False,
         capture=False,
         stream=False):

    '''pull will pull a singularity hub or Docker image
        
       Parameters
       ==========
       image: the complete image uri. If not provided, the client loaded is used
       pull_folder: if not defined, pulls to $PWD (''). If defined, pulls to
                    user specified location instead.

       Docker and Singularity Hub Naming
       ---------------------------------
       name: a custom name to use, to override default
       ext: if no name specified, the default extension to use.

    ''' 
    self.check_install()
    cmd = self._init_command('pull')

    # No image provided, default to use the client's loaded image
    if image is None:
        image = self._get_uri()

    # If it's still None, no go!
    if image is None:
        bot.exit('You must provide an image uri, or use client.load() first.')

    # Singularity Only supports shub and Docker pull
    if not re.search('^(shub|docker)://', image):
        bot.exit("pull only valid for docker and shub. Use sregistry client.")

    # Did the user ask for a custom pull folder?
    if pull_folder:
        self.setenv('SINGULARITY_PULLFOLDER', pull_folder)

    # If we still don't have a custom name, base off of image uri.
    if name is None:
        name = self._get_filename(image, ext)

    cmd = cmd + ["--name", name]

    if force is True:
        cmd = cmd + ["--force"]
   
    cmd.append(image)
    bot.info(' '.join(cmd))

    final_image = os.path.join(pull_folder, name)
    if stream is False:
        self._run_command(cmd, capture=capture)
    else:
        return final_image, stream_command(cmd, sudo=False)

    if os.path.exists(final_image):
        bot.info(final_image)
    return final_image
