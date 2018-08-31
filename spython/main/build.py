
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
import re
import os

def build(self, recipe=None, 
                image=None, 
                isolated=False,
                sandbox=False,
                writable=False,
                build_folder=None,
                robot_name=False,
                ext='simg',
                sudo=True,
                stream=False):

    '''build a singularity image, optionally for an isolated build
       (requires sudo). If you specify to stream, expect the image name
       and an iterator to be returned.
       
       image, builder = Client.build(...)

       Parameters
       ==========

       recipe: the path to the recipe file (or source to build from). If not
                  defined, we look for "Singularity" file in $PWD
       image: the image to build (if None, will use arbitary name
       isolated: if True, run build with --isolated flag
       sandbox: if True, create a writable sandbox
       writable: if True, use writable ext3 (sandbox takes preference)
       build_folder: where the container should be built.
       ext: the image extension to use.
       robot_name: boolean, default False. if you don't give your image a 
                   name (with "image") then a fun robot name will be generated
                   instead. Highly recommended :) 
       sudo: give sudo to the command (or not) default is True for build
    
    '''
    from spython.utils import check_install
    check_install()

    cmd = self._init_command('build')

    # No image provided, default to use the client's loaded image
    if recipe is None:
        recipe = self._get_uri()

    # If it's still None, try default build recipe
    if recipe is None:
        recipe = 'Singularity'

        if not os.path.exists(recipe):
            bot.exit('Cannot find %s, exiting.' %image)

    if image is None:
        if re.search('(docker|shub)://', recipe) and robot_name is False:
            image = self._get_filename(recipe, ext)
        else:
            image = "%s.%s" %(self.RobotNamer.generate(), ext)

    # Does the user want a custom build folder?
    if build_folder is not None:
        if not os.path.exists(build_folder):
            bot.exit('%s does not exist!' % build_folder)

        image = "%s/%s" %(build_folder, image)
        

    # The user wants to run an isolated build
    if isolated is True:
        cmd.append('--isolated')

    if sandbox is True:
        cmd.append('--sandbox')
    elif sandbox is True:
        cmd.append('--writable')

    cmd = cmd + [image, recipe]

    if stream is False:
        output = self._run_command(cmd, sudo=sudo, capture=False)
    else:
        # Here we return the expected image, and an iterator! 
        # The caller must iterate over
        return image, stream_command(cmd, sudo=sudo)

    if os.path.exists(image):
        return image
