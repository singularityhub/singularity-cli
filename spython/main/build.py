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

def build(self, recipe=None, image=None, isolated=False, sandbox=False):
    '''build a singularity image, optionally for an isolated build
       (requires sudo).

       Parameters
       ==========

       recipe: the path to the recipe file (or source to build from). If not
                  defined, we look for "Singularity" file in $PWD
       image: the image to build (if None, will use default name)
       isolated: if True, run build with --isolated flag
       sandbox: if True, create a writable sandbox
       writable: if True, use writable ext3 (sandbox takes preference)
   
    '''
    self.check_install()
    cmd = self._init_command('build')

    # No image provided, default to use the client's loaded image
    if recipe is None:
        recipe = self._get_uri()

    # If it's still None, try default build recipe
    if recipe is None:
        recipe = 'Singularity'

        if not os.path.exists(recipe):
            bot.error('Cannot find %s, exiting.' %image)
            sys.exit(1)

    if image is None:
        image = self._get_filename(image, ext)


    if isolated is True:
        cmd.append('--isolated')
    if sandbox is True:
        cmd.append('--sandbox')

    cmd = cmd + [image_path, spec_path]

    output = self.run_command(cmd,sudo=True)
    self.println(output)     
    return image_path
