
# Copyright (C) 2017-2019 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.


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

    # If Singularity version > 3.0, we have sif format
    if 'version 3' in self.version():
        ext = 'sif'

    # No image provided, default to use the client's loaded image
    if image is None:
        image = self._get_uri()

    # If it's still None, no go!
    if image is None:
        bot.exit('You must provide an image uri, or use client.load() first.')

    # Singularity Only supports shub and Docker pull
    if not re.search('^(shub|docker)://', image):
        bot.exit("pull only valid for docker and shub. Use sregistry client.")

    # If we still don't have a custom name, base off of image uri.
    if name is None:
        name = self._get_filename(image, ext)

    print('name is %s' % name)        

    # Regression Singularity 3.* onward, PULLFOLDER not honored
    # https://github.com/sylabs/singularity/issues/2788
    if pull_folder and 'version 3' in self.version():
        final_image = os.path.join(pull_folder, os.path.basename(name))
        cmd = cmd + ["--name", final_image]          
    else:
        final_image = name
        cmd = cmd + ["--name", name]

    if force is True:
        cmd = cmd + ["--force"]
   
    cmd.append(image)
    bot.info(' '.join(cmd))

    # If name is still None, make empty string
    if name is None:
        name = ''

    # Option 1: Streaming we just run to show user
    if stream is False:
        self._run_command(cmd, capture=capture)

    # Option 3: A custom name we can predict (not commit/hash) and can also show
    else:
        return final_image, stream_command(cmd, sudo=False)

    if os.path.exists(final_image):
        bot.info(final_image)
    return final_image
