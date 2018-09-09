
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
import shutil
import sys
import tempfile

def pull(self, 
         image=None,
         name=None,
         pull_folder='',
         ext="simg",
         force=False,
         capture=False,
         name_by_commit=False,
         name_by_hash=False,
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
    from spython.utils import check_install
    check_install()

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
    # Determine how to tell client to name the image, preference to hash

    if name_by_hash is True:
        cmd.append('--hash')

    elif name_by_commit is True:
        cmd.append('--commit')

    elif name is None:
        name = self._get_filename(image, ext)
        
    # Only add name if we aren't naming by hash or commit
    if not name_by_commit and not name_by_hash:
        cmd = cmd + ["--name", name]

    if force is True:
        cmd = cmd + ["--force"]
   
    cmd.append(image)
    bot.info(' '.join(cmd))

    # If name is still None, make empty string
    if name is None:
        name = ''

    final_image = os.path.join(pull_folder, name)

    # Option 1: For hash or commit, need return value to get final_image
    if name_by_commit or name_by_hash:

        # Set pull to temporary location
        tmp_folder = tempfile.mkdtemp()
        self.setenv('SINGULARITY_PULLFOLDER', tmp_folder)
        self._run_command(cmd, capture=capture)

        try:
            tmp_image = os.path.join(tmp_folder, os.listdir(tmp_folder)[0])
            final_image = os.path.join(pull_folder, os.path.basename(tmp_image))
            shutil.move(tmp_image, final_image)
            shutil.rmtree(tmp_folder)

        except:
            bot.error('Issue pulling image with commit or hash, try without?')

    # Option 2: Streaming we just run to show user
    elif stream is False:
        self._run_command(cmd, capture=capture)

    # Option 3: A custom name we can predict (not commit/hash) and can also show
    else:
        return final_image, stream_command(cmd, sudo=False)

    if os.path.exists(final_image):
        bot.info(final_image)
    return final_image
